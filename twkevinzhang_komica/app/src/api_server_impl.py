import requests

import extension_api_pb2 as pb2
import extension_api_pb2_grpc as pb2_grpc
import parse_boards
from parse_thread_infos import parse_thread_infos_html

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

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
        response = requests.get(f"{b.url}", headers=HEADERS)
        response.encoding = 'utf-8'
        response.raise_for_status()
        thread_infos = parse_thread_infos_html(response.text)
        return pb2.GetThreadInfosRes(
            thread_infos=thread_infos,
            page=pb2.PaginationRes(
                current_page=1,
                total_page=1,
            )
        )

    async def GetThread(self, req: pb2.GetThreadReq, context) -> pb2.GetThreadRes:
        pass

    async def GetRegardingPosts(self, req: pb2.GetRegardingPostsReq, context) -> pb2.GetRegardingPostsRes:
        pass

    async def GetPost(self, req: pb2.GetPostReq, context) -> pb2.GetPostRes:
        pass

    async def GetComments(self, req: pb2.GetCommentsReq, context) -> pb2.GetThreadInfosRes:
        pass
