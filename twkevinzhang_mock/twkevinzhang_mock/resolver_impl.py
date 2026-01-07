import logging
import time

from . import mock_api_pb2 as pb2
from . import mock_domain_models_pb2 as domain_pb2
from . import salt
from .domain import Post


def pagination(req: domain_pb2.PaginationReq, items) -> (list, domain_pb2.PaginationRes):
    page_size = req.page_size if req.page_size is not None and req.page_size > 0 else 20
    page = req.page if req.page is not None and req.page > 0 else 1
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
        self.pkg_name = "twkevinzhang_mock"

    def GetBoards(self, req: pb2.GetBoardsReq, context) -> pb2.GetBoardsRes:
        boards = [
            domain_pb2.Board(
                id=salt.encode("board_1"),
                name="General Discussion",
                icon="https://img.icons8.com/color/48/chat--v1.png",
                url="https://example.com/mock/board1",
                pkg_name=self.pkg_name,
            ),
            domain_pb2.Board(
                id=salt.encode("board_2"),
                name="Tech News",
                icon="https://img.icons8.com/color/48/electronics.png",
                url="https://example.com/mock/board2",
                pkg_name=self.pkg_name,
            ),
            domain_pb2.Board(
                id=salt.encode("board_3"),
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

    def GetThreads(self, req: pb2.GetThreadsReq, context) -> pb2.GetThreadsRes:
        # Determine which boards to generate data for
        board_id = salt.decode(req.board_id) if req.board_id else "board_1"
        sorting = req.sort or "latest"

        threads = []
        now = int(time.time())
        
        # In mock, we just generate 10 threads for the single board
        for i in range(1, 11):
            tid = f"thread_{board_id}_{i}"
            threads.append(Post(
                id=tid,
                thread_id=tid,
                board_id=board_id,
                author_id="user_123",
                author_name=f"Mock Author {i}",
                created_at=now - (i * 3600),
                title=f"Mock Thread Title {i} in {board_id} ({sorting})",
                liked=i * 10,
                disliked=i,
                comments=i * 5,
                image=domain_pb2.ImageParagraph(
                    raw=f"https://picsum.photos/seed/{tid}/400/300",
                    thumb=f"https://picsum.photos/seed/{tid}/200/150"
                ),
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content=f"This is the preview text for mock thread {i}. ")
                    )
                ],
                tags=["Mock", board_id],
                latest_reply_created_at=now - (i * 1800),
                replies_count=i * 5,
                url=f"https://example.com/mock/{board_id}/{tid}"
            ))

        current_page = 1
        total_page = 1
        if req.page:
            threads, page_res = pagination(req.page, threads)
            current_page = page_res.current_page
            total_page = page_res.total_page

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
        
        now = int(time.time())
        
        thread = Post(
            id=post_id,
            thread_id=thread_id,
            board_id=board_id,
            author_id="user_123",
            author_name="Mock Author Original",
            created_at=now - 86400,
            title="Mock Thread Full Detail",
            liked=100,
            disliked=5,
            comments=50,
            image=None,
            contents=[
                domain_pb2.Paragraph(
                    type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                    text=domain_pb2.TextParagraph(content="This is the full content of the mock thread.")
                ),
                domain_pb2.Paragraph(
                    type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_IMAGE,
                    image=domain_pb2.ImageParagraph(
                        raw=f"https://picsum.photos/seed/{thread_id}/800/600",
                    )
                ),
                domain_pb2.Paragraph(
                    type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                    text=domain_pb2.TextParagraph(content="More text after the image to simulate a real post structure.")
                )
            ],
            tags=["Mock", "Detail"],
            latest_reply_created_at=now - 3600,
            replies_count=50,
            url=f"https://example.com/mock/{board_id}/{thread_id}"
        )
        
        return pb2.GetOriginalPostRes(
            original_post=thread.toSaltPb2('article_post'),
        )

    def GetReplies(self, req: pb2.GetRepliesReq, context) -> pb2.GetRepliesRes:
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
                author_id=f"user_{i}",
                author_name=f"Replier {i}",
                created_at=now - (6-i) * 600,
                title="",
                liked=i * 2,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_REPLY_TO,
                        reply_to=domain_pb2.ReplyToParagraph(
                            id=reply_to_id,
                            author_name="Original Author",
                            preview="Previous content..."
                        )
                    ),
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content=f"This is mock reply {i}.")
                    )
                ],
                tags=[],
                latest_reply_created_at=0,
                replies_count=0,
                url=None
            ))

        return pb2.GetRepliesRes(
            replies=[post.toSaltPb2('article_post') for post in posts],
            page=domain_pb2.PaginationRes(
                current_page=1,
                total_page=1,
            ),
        )

    def GetComments(self, req: pb2.GetCommentsReq, context) -> pb2.GetThreadsRes:
        return pb2.GetThreadsRes()
