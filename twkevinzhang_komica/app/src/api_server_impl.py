import aiohttp
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

    def GetSite(self, req: pb2.Empty, context):
        return pb2.GetSiteRes(
            site=pb2.Site(
                id="komica",
                icon="https://komica1.org/favicon.ico",
                name="komica1.org",
                description="A description of komica1.org",
                url="https://komica1.org",
            )
        )

    def GetBoards(self, req: pb2.GetBoardsReq, context):
        l = parse_boards.list()
        return pb2.GetBoardsRes(boards=l)

    async def GetThreadInfos(self, req: pb2.GetThreadInfosReq, context):
        b = parse_boards.get(req.board_id)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{b.url}", headers=HEADERS) as response:
                response.raise_for_status()
                return parse_thread_infos_html(await response.text())

    async def GetThread(self, req: pb2.GetThreadReq, context):
        pass

    async def GetRegardingPosts(self, req: pb2.GetRegardingPostsReq, context):
        pass

    async def GetPost(self, req: pb2.GetPostReq, context):
        pass

    async def GetComments(self, req: pb2.GetCommentsReq, context):
        pass
