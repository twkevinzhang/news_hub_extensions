import logging
import time

from . import extension_api_pb2 as pb2
from . import extension_api_pb2_grpc as pb2_grpc
from . import salt
from .domain import Post


def pagination(req: pb2.PaginationReq, items) -> (list, pb2.PaginationRes):
    page_size = req.page_size if req.page_size is not None and req.page_size > 0 else 20
    page = req.page if req.page is not None and req.page > 0 else 1
    start_index = (page - 1) * page_size
    end_index = min(start_index + page_size, len(items))
    total_page = (len(items) + page_size - 1) // page_size
    return (
        items[start_index:end_index],
        pb2.PaginationRes(
            current_page=page,
            total_page=total_page,
        ))


class ResolverImpl(pb2_grpc.ExtensionApiServicer):
    def __init__(self):
        self.site_id = "mock_site"
        self.pkg_name = "twkevinzhang_mock"

    def GetSite(self, req: pb2.Empty, context) -> pb2.GetSiteRes:
        return pb2.GetSiteRes(
            site=pb2.Site(
                id=salt.encode(self.site_id),
                icon="https://img.icons8.com/color/96/test-partial-passed.png",
                name="Mock Site",
                description="A mock site for testing purposes",
                url="https://example.com/mock",
            )
        )

    def GetBoards(self, req: pb2.GetBoardsReq, context) -> pb2.GetBoardsRes:
        boards = [
            pb2.Board(
                id=salt.encode("board_1"),
                site_id=salt.encode(self.site_id),
                name="General Discussion",
                icon="https://img.icons8.com/color/48/chat--v1.png",
                url="https://example.com/mock/board1",
                pkg_name=self.pkg_name,
            ),
            pb2.Board(
                id=salt.encode("board_2"),
                site_id=salt.encode(self.site_id),
                name="Tech News",
                icon="https://img.icons8.com/color/48/electronics.png",
                url="https://example.com/mock/board2",
                pkg_name=self.pkg_name,
            ),
            pb2.Board(
                id=salt.encode("board_3"),
                site_id=salt.encode(self.site_id),
                name="Anime & Manga",
                icon="https://img.icons8.com/color/48/anime.png",
                url="https://example.com/mock/board3",
                pkg_name=self.pkg_name,
            ),
        ]
        
        page_res = None
        if req.page:
            boards, page_res = pagination(req.page, boards)
            
        return pb2.GetBoardsRes(
            boards=boards,
            page=page_res,
        )

    def GetThreadInfos(self, req: pb2.GetThreadInfosReq, context) -> pb2.GetThreadInfosRes:
        site_id = salt.decode(req.site_id)
        
        # Determine which boards to generate data for
        boards_to_process = []
        if req.boards_sorting:
            for encoded_id in req.boards_sorting.keys():
                boards_to_process.append(salt.decode(encoded_id))
        else:
            boards_to_process = ["board_1"]

        thread_infos = []
        now = int(time.time())
        
        for board_id in boards_to_process:
            for i in range(1, 11):
                tid = f"thread_{board_id}_{i}"
                thread_infos.append(Post(
                    id=tid,
                    thread_id=tid,
                    board_id=board_id,
                    site_id=site_id,
                    author_id="user_123",
                    author_name=f"Mock Author {i}",
                    created_at=now - (i * 3600),
                    title=f"Mock Thread Title {i} in {board_id}",
                    liked=i * 10,
                    disliked=i,
                    comments=i * 5,
                    image=pb2.ImageParagraph(
                        raw=f"https://picsum.photos/seed/{tid}/400/300",
                        thumb=f"https://picsum.photos/seed/{tid}/200/150"
                    ),
                    contents=[
                        pb2.Paragraph(
                            type=pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                            text=pb2.TextParagraph(content=f"This is the preview text for mock thread {i}. ")
                        )
                    ],
                    tags=["Mock", board_id],
                    latest_regarding_post_created_at=now - (i * 1800),
                    regarding_posts_count=i * 5,
                    url=f"https://example.com/mock/{board_id}/{tid}"
                ))

        current_page = 1
        total_page = 1
        if req.page:
            thread_infos, page_res = pagination(req.page, thread_infos)
            current_page = page_res.current_page
            total_page = page_res.total_page

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
        
        now = int(time.time())
        
        thread = Post(
            id=post_id,
            thread_id=thread_id,
            board_id=board_id,
            site_id=site_id,
            author_id="user_123",
            author_name="Mock Author Original",
            created_at=now - 86400,
            title="Mock Thread Full Detail",
            liked=100,
            disliked=5,
            comments=50,
            image=None,
            contents=[
                pb2.Paragraph(
                    type=pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                    text=pb2.TextParagraph(content="This is the full content of the mock thread.")
                ),
                pb2.Paragraph(
                    type=pb2.ParagraphType.PARAGRAPH_TYPE_IMAGE,
                    image=pb2.ImageParagraph(
                        raw=f"https://picsum.photos/seed/{thread_id}/800/600",
                    )
                ),
                pb2.Paragraph(
                    type=pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                    text=pb2.TextParagraph(content="More text after the image to simulate a real post structure.")
                )
            ],
            tags=["Mock", "Detail"],
            latest_regarding_post_created_at=now - 3600,
            regarding_posts_count=50,
            url=f"https://example.com/mock/{board_id}/{thread_id}"
        )
        
        return pb2.GetThreadPostRes(
            thread_post=thread.toSaltPb2('article_post'),
        )

    def GetRegardingPosts(self, req: pb2.GetRegardingPostsReq, context) -> pb2.GetRegardingPostsRes:
        site_id = salt.decode(req.site_id)
        board_id = salt.decode(req.board_id)
        thread_id = salt.decode(req.thread_id)
        reply_to_id = salt.decode(req.reply_to_id)
        
        now = int(time.time())
        posts = []
        
        for i in range(1, 6):
            pid = f"reply_{thread_id}_{i}"
            posts.append(Post(
                id=pid,
                thread_id=thread_id,
                board_id=board_id,
                site_id=site_id,
                author_id=f"user_{i}",
                author_name=f"Replier {i}",
                created_at=now - (6-i) * 600,
                title="",
                liked=i * 2,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    pb2.Paragraph(
                        type=pb2.ParagraphType.PARAGRAPH_TYPE_REPLY_TO,
                        reply_to=pb2.ReplyToParagraph(
                            id=reply_to_id,
                            author_name="Original Author",
                            preview="Previous content..."
                        )
                    ),
                    pb2.Paragraph(
                        type=pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=pb2.TextParagraph(content=f"This is mock reply {i}.")
                    )
                ],
                tags=[],
                latest_regarding_post_created_at=0,
                regarding_posts_count=0,
                url=None
            ))

        return pb2.GetRegardingPostsRes(
            regarding_posts=[post.toSaltPb2('article_post') for post in posts],
            page=pb2.PaginationRes(
                current_page=1,
                total_page=1,
            ),
        )

    def GetComments(self, req: pb2.GetCommentsReq, context) -> pb2.GetThreadInfosRes:
        return pb2.GetThreadInfosRes()
