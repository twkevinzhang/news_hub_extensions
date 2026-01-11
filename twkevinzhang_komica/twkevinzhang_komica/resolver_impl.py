import asyncio
import logging

from . import komica_api_pb2 as pb2
from . import komica_domain_models_pb2 as domain_pb2
from . import parse_boards
from . import salt
from .domain import board_id_to_url_prefix, OverPageError
from .parse_threads import parse_threads_html, parse_replies_html, parse_original_post_html
from .requester import Requester
from .utilities import is_zero


def pagination(req: domain_pb2.PaginationReq, items) -> (list, domain_pb2.PaginationRes):
    page_size = req.page_size if req.page_size is not None and req.page_size > 0 else 20  # default page size is 20
    page = req.page if req.page is not None and req.page > 0 else 1  # default page is 1
    start_index = (page - 1) * page_size
    end_index = min(start_index + page_size, len(items))
    total_page = (len(items) + page_size - 1) // page_size
    return (
        items[start_index:end_index],
        domain_pb2.PaginationRes(
            current_page=page,
            total_page=total_page,
        ))


class ResolverImpl:
    def __init__(self):
        pass

    def GetBoards(self, req: pb2.GetBoardsReq, context) -> pb2.GetBoardsRes:
        boards, page = parse_boards.list(), None
        if req.page is not None:
            boards, page = pagination(req.page, boards)

        return pb2.GetBoardsRes(
            boards=[
                domain_pb2.Board(
                    id=salt.encode(x.id),
                    name=x.name,
                    icon=x.icon,
                    large_welcome_image=x.large_welcome_image,
                    url=x.url,
                    supported_threads_sorting=x.supported_threads_sorting,
                    pkg_name=x.pkg_name,
                ) for x in boards
            ],
            page=page,
        )

    def GetThreads(self, req: pb2.GetThreadsReq, context) -> pb2.GetThreadsRes:
        urls = {}
        board_id = salt.decode(req.board_id) if req.board_id else "gita/00b"
        
        if req.page is not None and not is_zero(req.page.page):
            if req.page.page < 10:
                urls[board_id] = board_id_to_url_prefix(board_id) + f'/{req.page.page + 1}.htm'
            else:
                urls[board_id] = board_id_to_url_prefix(board_id) + f'/pixmicat.php?page_num={req.page.page + 1}'
        else:
            urls[board_id] = board_id_to_url_prefix(board_id) + '/index.htm'

        total_page = 0
        requester = Requester()
        results = asyncio.run(requester.crawl(urls))
        threads = []
        for result in results:
            if result.is_failed():
                logging.error(f"Failed to fetch {result.url}")
                logging.exception(result.error)
            else:
                try:
                    board_id = result.key
                    items, _, total = parse_threads_html(result.html, board_id)
                    threads += items
                    total_page = max(total_page, total)
                except OverPageError:
                    logging.warning(f"{result.url} is over page")
                except Exception as e:
                    logging.error(f"{result.url} has parse error")
                    raise e

        current_page = 1
        if req.page is not None:
            if not is_zero(req.page.page):
                current_page = req.page.page
        return pb2.GetThreadsRes(
            threads=[thread.toSaltPb2('single_image_post') for thread in threads],
            page=domain_pb2.PaginationRes(
                current_page=current_page,
                total_page=total_page,
            ),
        )

    def GetOriginalPost(self, req: pb2.GetOriginalPostReq, context) -> pb2.GetOriginalPostRes:
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
        thread = None
        try:
            thread = parse_original_post_html(result.html, board_id, thread_id, post_id)
        except Exception as e:
            logging.error(f"{result.url} has parse error")
            raise e
        return pb2.GetOriginalPostRes(
            original_post=thread.toSaltPb2('article_post'),
        )

    def GetReplies(self, req: pb2.GetRepliesReq, context) -> pb2.GetRepliesRes:
        if req.page and req.page.page > 1:
            return pb2.GetRepliesRes(
                replies=[],
                page=domain_pb2.PaginationRes(
                    current_page=1,
                    total_page=1,
                ),
            )
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
        posts = []
        try:
            posts = parse_replies_html(result.html, board_id, thread_id, reply_to_id)
        except Exception as e:
            logging.error(f"{result.url} has parse error")
            raise e
        return pb2.GetRepliesRes(
            replies=[post.toSaltPb2('article_post') for post in posts],
            page=domain_pb2.PaginationRes(
                current_page=1,
                total_page=1,
            ),
        )

    def GetComments(self, req: pb2.GetCommentsReq, context) -> pb2.GetThreadsRes:
        return pb2.GetThreadsRes()

    def GetBoardSortOptions(self, req: pb2.GetBoardSortOptionsReq, context) -> pb2.GetBoardSortOptionsRes:
        results = []
        for encoded_bid in req.board_ids:
            try:
                board_id = salt.decode(encoded_bid)
                board = parse_boards.get(board_id)
                if board:
                    results.append(pb2.BoardSortOption(
                        board_id=encoded_bid,
                        options=list(board.supported_threads_sorting)
                    ))
            except Exception:
                continue
        return pb2.GetBoardSortOptionsRes(options=results)
