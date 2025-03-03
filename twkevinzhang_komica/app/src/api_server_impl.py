import logging

import requests

import extension_api_pb2 as pb2
import extension_api_pb2_grpc as pb2_grpc
import parse_boards
from parse_threads import parse_thread_infos_html, parse_regarding_posts_html, parse_thread_html

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

class ApiServerImpl(pb2_grpc.ExtensionApiServicer):
    def __init__(self):
        pass

    def GetSite(self, req: pb2.Empty, context) -> pb2.GetSiteRes:
        return pb2.GetSiteRes(
            site=pb2.Site(
                id="komica",
                icon="https://komica1.org/favicon.ico",
                name="komica1.org",
                description="A description of komica1.org",
                url="https://komica1.org",
            )
        )

    def GetBoards(self, req: pb2.GetBoardsReq, context) -> pb2.GetBoardsRes:
        l = parse_boards.list()
        return pb2.GetBoardsRes(boards=l)

    def GetThreadInfos(self, req: pb2.GetThreadInfosReq, context) -> pb2.GetThreadInfosRes:
        b = parse_boards.get(req.board_id)
        response = get(f"{b.url}")
        thread_infos = parse_thread_infos_html(response, req.site_id, req.board_id)
        return pb2.GetThreadInfosRes(
            thread_infos=thread_infos,
            page=pb2.PaginationRes(
                current_page=1,
                total_page=1,
            )
        )

    def GetThread(self, req: pb2.GetThreadReq, context) -> pb2.GetThreadRes:
        b = parse_boards.get(req.board_id)
        prefix = b.url.removesuffix("/index.htm")
        response = get(f"{prefix}/pixmicat.php?res={req.id}")
        thread = parse_thread_html(response, req.site_id, req.board_id)
        return pb2.GetThreadRes(
            thread=thread,
        )

    def GetRegardingPosts(self, req: pb2.GetRegardingPostsReq, context) -> pb2.GetRegardingPostsRes:
        b = parse_boards.get(req.board_id)
        prefix = b.url.removesuffix("/index.htm")
        response = get(f"{prefix}/pixmicat.php?res={req.thread_id}")
        posts = parse_regarding_posts_html(response, req.site_id, req.board_id, req.thread_id)
        return pb2.GetRegardingPostsRes(
            regarding_posts=posts
        )

    def GetPost(self, req: pb2.GetPostReq, context) -> pb2.GetPostRes:
        pass

    def GetComments(self, req: pb2.GetCommentsReq, context) -> pb2.GetThreadInfosRes:
        pass
