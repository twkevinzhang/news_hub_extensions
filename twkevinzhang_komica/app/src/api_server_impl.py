import extension_api_pb2 as pb2
import extension_api_pb2_grpc as pb2_grpc
from get_boards import get_boards


class ApiServerImpl(pb2_grpc.ExtensionApiServicer):
    def __init__(self):
        pass

    def GetSite(self, request, context):
        return pb2.GetSiteRes(
            site=pb2.Site(
                id="1",
                icon="https://komica1.org/favicon.ico",
                name="komica1.org",
                description="A description of komica1.org",
                url="https://komica1.org"
            )
        )

    def GetBoards(self, request, context):
        boards = get_boards()
        return pb2.GetBoardsRes(boards=boards)
