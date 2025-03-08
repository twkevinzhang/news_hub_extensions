import asyncio
import logging

import requests

import extension_api_pb2 as pb2
import extension_api_pb2_grpc as pb2_grpc
import parse_boards
import salt
from parse_threads import parse_thread_infos_html, parse_regarding_posts_html, parse_thread_html
from requester import Requester, Result
from nullable import is_zero_map
from domain import board_id_to_url_prefix

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}


def get(url: str):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    content_type = response.headers.get('Content-Type')
    if content_type and 'charset=' in content_type:
        encoding = content_type.split('charset=')[-1].strip()
    else:
        encoding = response.apparent_encoding
        if encoding is None:
            encoding = 'utf-8'
    logging.debug(f"{url} Encoding: {encoding}")
    html_content = response.content.decode(encoding, errors='ignore')
    return html_content


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


class ApiServerImpl(pb2_grpc.ExtensionApiServicer):
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
        site_id = salt.decode(req.site_id)
        urls_board_id = {} # url -> "gita/00b"
        if not is_zero_map(req.boards_sorting):
            for encoded_id, sorting in req.boards_sorting.items():
                board_id = salt.decode(encoded_id)
                prefix = board_id_to_url_prefix(board_id)
                urls_board_id[f"{prefix}/index.htm"] = board_id
        else:
            urls_board_id[f"https://gita.komica1.org/00b/index.htm"] = "gita/00b"
        requester = Requester()
        results: list[Result] = asyncio.run(requester.crawl(urls_board_id.keys()))
        thread_infos = []
        for result in results:
            if result.is_failed():
                logging.error(f"Failed to fetch {result.url}")
                logging.exception(result.error)
            else:
                board_id = urls_board_id[result.url]
                # TODO: Implement Pagination
                thread_infos += parse_thread_infos_html(result.html, site_id, board_id)

        page = None
        if req.page is not None:
            thread_infos, page = pagination(req.page, thread_infos)

        return pb2.GetThreadInfosRes(
            thread_infos=[thread.toSaltPb2() for thread in thread_infos],
            page=page,
        )

    def GetThreadPost(self, req: pb2.GetThreadPostReq, context) -> pb2.GetThreadPostRes:
        site_id = salt.decode(req.site_id)
        board_id = salt.decode(req.board_id)
        thread_id = salt.decode(req.thread_id)
        post_id = salt.decode(req.post_id)
        prefix = board_id_to_url_prefix(board_id)
        response = get(f'{prefix}/pixmicat.php?res={thread_id}')
        thread = parse_thread_html(response, site_id, board_id, thread_id, post_id)
        return pb2.GetThreadPostRes(
            thread_post=thread.toSaltPb2(),
        )

    def GetRegardingPosts(self, req: pb2.GetRegardingPostsReq, context) -> pb2.GetRegardingPostsRes:
        site_id = salt.decode(req.site_id)
        board_id = salt.decode(req.board_id)
        thread_id = salt.decode(req.thread_id)
        reply_to_id = salt.decode(req.reply_to_id)
        prefix = board_id_to_url_prefix(board_id)
        response = get(f'{prefix}/pixmicat.php?res={thread_id}')

        posts, page = parse_regarding_posts_html(response, site_id, board_id, thread_id, reply_to_id), None
        if req.page is not None:
            posts, page = pagination(req.page, posts)

        return pb2.GetRegardingPostsRes(
            regarding_posts=[post.toSaltPb2() for post in posts],
            page=page,
        )

    def GetComments(self, req: pb2.GetCommentsReq, context) -> pb2.GetThreadInfosRes:
        pass
