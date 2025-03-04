import logging

import requests

import extension_api_pb2 as pb2
import extension_api_pb2_grpc as pb2_grpc
import parse_boards
import salt
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
                id=salt.encode("komica"),
                icon="https://komica1.org/favicon.ico",
                name="komica1.org",
                description="A description of komica1.org",
                url="https://komica1.org",
            )
        )

    def GetBoards(self, req: pb2.GetBoardsReq, context) -> pb2.GetBoardsRes:
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
                ) for x in parse_boards.list()
            ]
        )

    def GetThreadInfos(self, req: pb2.GetThreadInfosReq, context) -> pb2.GetThreadInfosRes:
        site_id = salt.decode(req.site_id)
        board_id = salt.decode(req.board_id)
        [subdomain, board_sub_id] = board_id.split("/")
        response = get(f'https://{subdomain}.komica1.org/{board_sub_id}/index.htm')
        thread_infos = parse_thread_infos_html(response, site_id, board_id)
        return pb2.GetThreadInfosRes(
            thread_infos=[ thread.toSaltPb2() for thread in thread_infos ],
            page=pb2.PaginationRes(
                current_page=1,
                total_page=1,
            )
        )

    def GetThreadPost(self, req: pb2.GetThreadPostReq, context) -> pb2.GetThreadPostRes:
        site_id = salt.decode(req.site_id)
        board_id = salt.decode(req.board_id)
        thread_id = salt.decode(req.id)
        post_id = salt.decode(req.post_id)
        [subdomain, board_sub_id] = board_id.split("/")
        response = get(f'https://{subdomain}.komica1.org/{board_sub_id}/pixmicat.php?res={thread_id}')
        thread = parse_thread_html(response, site_id, board_id, thread_id, post_id)
        return pb2.GetThreadPostRes(
            thread_post=thread.toSaltPb2(),
        )

    def GetRegardingPosts(self, req: pb2.GetRegardingPostsReq, context) -> pb2.GetRegardingPostsRes:
        site_id = salt.decode(req.site_id)
        board_id = salt.decode(req.board_id)
        thread_id = salt.decode(req.thread_id)
        post_id = salt.decode(req.post_id)
        [subdomain, board_sub_id] = board_id.split("/")
        response = get(f'https://{subdomain}.komica1.org/{board_sub_id}/pixmicat.php?res={thread_id}')
        posts = parse_regarding_posts_html(response, site_id, board_id, thread_id, post_id)
        return pb2.GetRegardingPostsRes(
            regarding_posts=[ post.toSaltPb2() for post in posts ],
        )

    def GetComments(self, req: pb2.GetCommentsReq, context) -> pb2.GetThreadInfosRes:
        pass
