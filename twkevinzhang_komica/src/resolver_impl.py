import asyncio
import logging

import extension_api_pb2 as pb2
import extension_api_pb2_grpc as pb2_grpc
import parse_boards
import salt
from domain import board_id_to_url_prefix, OverPageError
from parse_threads import parse_thread_infos_html, parse_regarding_posts_html, parse_thread_html
from requester import Requester
from utilities import is_zero


def pagination(req: pb2.PaginationReq, items) -> (list, pb2.PaginationRes):
    page_size = req.page_size if req.page_size is not None and req.page_size > 0 else 20  # default page size is 20
    page = req.page if req.page is not None and req.page > 0 else 1  # default page is 1
    start_index = (page - 1) * page_size
    end_index = min(start_index + page_size, len(items))
    total_page = (len(items) + page_size - 1) // page_size
    return (
        items[start_index:end_index],
        pb2.PaginationRes(
            current_page=req.page,
            total_page=total_page,
        ))


class ResolverImpl(pb2_grpc.ExtensionApiServicer):
    def __init__(self):
        pass

    def GetSite(self, req: pb2.Empty, context) -> pb2.GetSiteRes:
        return pb2.GetSiteRes(
            site=pb2.Site(
                id=salt.encode("komica"),
                icon="https://komica1.org/favicon.ico",
                name="komica1.org",
                description="A description of komica1.org",
                url="https://komica1.org",
            )
        )

    def GetBoards(self, req: pb2.GetBoardsReq, context) -> pb2.GetBoardsRes:
        boards, page = parse_boards.list(), None
        if req.page is not None:
            boards, page = pagination(req.page, boards)

        return pb2.GetBoardsRes(
            boards=[
                pb2.Board(
                    id=salt.encode(x.id),
                    site_id=salt.encode(x.site_id),
                    name=x.name,
                    icon=x.icon,
                    large_welcome_image=x.large_welcome_image,
                    url=x.url,
                    supported_threads_sorting=x.supported_threads_sorting,
                ) for x in boards
            ],
            page=page,
        )

    def GetThreadInfos(self, req: pb2.GetThreadInfosReq, context) -> pb2.GetThreadInfosRes:
        """
        取得貼文資訊。

        Args:
            req (pb2.GetThreadInfosReq): 討論串請求物件，包含：
                page (PageReq): 分頁相關資訊：
                    page_size (int): **無效**，由解析器決定實際大小。
                    page (int): 要請求的頁碼。
            context (grpc.ServicerContext): gRPC 服務端的請求上下文。

        Returns:
            pb2.GetThreadInfosRes: 討論串資訊回應物件，包含：
                thread_infos (list[ThreadInfo]): 討論串資訊列表。
                page (PageRes): 分頁資訊：
                    current_page (int): 當前頁碼。
                    total_page (int): 總頁數。
        """
        site_id = salt.decode(req.site_id)
        urls = {}
        boards_sorting = req.boards_sorting
        if is_zero(req.boards_sorting):
            boards_sorting = {
                salt.encode("gita/00b"): "latest_replied",
            }
        for encoded_id, sorting in boards_sorting.items():
            board_id = salt.decode(encoded_id)
            if req.page is not None:
                urls[board_id] = board_id_to_url_prefix(board_id) + f'/{req.page.page + 1}.htm'
            else:
                urls[board_id] = board_id_to_url_prefix(board_id) + '/index.htm'

        total_page = 0
        requester = Requester()
        results = asyncio.run(requester.crawl(urls))
        thread_infos = []
        for result in results:
            if result.is_failed():
                logging.error(f"Failed to fetch {result.url}")
                logging.exception(result.error)
            else:
                try:
                    board_id = result.key
                    items, _, total = parse_thread_infos_html(result.html, site_id, board_id)
                    thread_infos += items
                    total_page = max(total_page, total)
                except OverPageError:
                    logging.warning(f"{result.url} is over page")
                except Exception as e:
                    raise e

        current_page = 1
        if req.page is not None:
            if not is_zero(req.page.page):
                current_page = req.page.page
        return pb2.GetThreadInfosRes(
            thread_infos=[thread.toSaltPb2('single_image_post') for thread in thread_infos],
            page=pb2.PaginationRes(
                current_page=current_page,
                total_page=total_page,
            ),
        )

    def GetThreadPost(self, req: pb2.GetThreadPostReq, context) -> pb2.GetThreadPostRes:
        site_id = salt.decode(req.site_id)
        board_id = salt.decode(req.board_id)
        thread_id = salt.decode(req.thread_id)
        post_id = salt.decode(req.post_id)
        prefix = board_id_to_url_prefix(board_id)
        requester = Requester()
        result = asyncio.run(requester.single_crawl(f'{prefix}/pixmicat.php?res={thread_id}'))
        if result.is_failed():
            logging.error(f"Failed to fetch {result.url}")
            logging.exception(result.error)
            raise result.error
        thread = parse_thread_html(result.html, site_id, board_id, thread_id, post_id)
        return pb2.GetThreadPostRes(
            thread_post=thread.toSaltPb2('article_post'),
        )

    def GetRegardingPosts(self, req: pb2.GetRegardingPostsReq, context) -> pb2.GetRegardingPostsRes:
        """
        取得貼文討論串。

        Args:
            req (pb2.GetRegardingPostsReq): 討論串請求物件，包含：
                page (PageReq): 分頁相關資訊：
                    page_size (int): **無效**，由解析器決定實際大小。
                    page (int): **無效**，如果輸入大於 1 將回傳空結果，因為永遠只有一頁。
            context (grpc.ServicerContext): gRPC 服務端的請求上下文。

        Returns:
            pb2.GetRegardingPostsRes: 討論串資訊回應物件，包含：
                thread_infos (list[ThreadInfo]): 討論串資訊列表。
                page (PageRes): 分頁資訊：
                    current_page (int): 永遠只有第一頁。
                    total_page (int): 永遠只有一頁。
        """
        if req.page and req.page.page > 1:
            return pb2.GetRegardingPostsRes(
                regarding_posts=[],
                page=pb2.PaginationRes(
                    current_page=1,
                    total_page=1,
                ),
            )
        site_id = salt.decode(req.site_id)
        board_id = salt.decode(req.board_id)
        thread_id = salt.decode(req.thread_id)
        reply_to_id = salt.decode(req.reply_to_id)
        prefix = board_id_to_url_prefix(board_id)
        requester = Requester()
        result = asyncio.run(requester.single_crawl(f'{prefix}/pixmicat.php?res={thread_id}'))
        if result.is_failed():
            logging.error(f"Failed to fetch {result.url}")
            logging.exception(result.error)
            raise result.error
        posts, page = parse_regarding_posts_html(result.html, site_id, board_id, thread_id, reply_to_id), 1
        return pb2.GetRegardingPostsRes(
            regarding_posts=[post.toSaltPb2('article_post') for post in posts],
            page=pb2.PaginationRes(
                current_page=1,
                total_page=1,
            ),
        )

    def GetComments(self, req: pb2.GetCommentsReq, context) -> pb2.GetThreadInfosRes:
        pass
