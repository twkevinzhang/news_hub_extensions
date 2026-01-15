import logging
import time

from . import mock_api_pb2 as pb2
from . import mock_domain_models_pb2 as domain_pb2
from . import salt
from .domain import Post, Comment


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
        keywords = req.keywords or ""

        # 特殊情境：如果關鍵字是 "empty"，回傳空列表
        if keywords.lower() == "empty":
            return pb2.GetThreadsRes(
                threads=[],
                page=domain_pb2.PaginationRes(current_page=1, total_page=0),
            )

        all_threads = []
        now = int(time.time())
        
        # 產生較多資料以利測試分頁與排序 (產生 100 條)
        for i in range(1, 101):
            tid = f"thread_{board_id}_{i}"
            # 模擬關鍵字搜尋：如果有關鍵字，則標題包含它
            display_title = f"Mock Thread {i} in {board_id}"
            if keywords:
                display_title = f"[{keywords}] {display_title}"
            
            # 建立不同數值以利排序測試
            # latest: created_at (降序)
            # hot: liked (降序)
            # commented: comments (降序)
            all_threads.append(Post(
                id=tid,
                thread_id=tid,
                board_id=board_id,
                author_id=f"user_{i}",
                author_name=f"Mock Author {i}",
                created_at=now - (i * 3600), # 每隔一小時
                title=display_title,
                liked=i * 7 % 100, # 隨機性數值
                disliked=i % 10,
                comments=i * 3 % 50,
                image=domain_pb2.ImageParagraph(
                    raw=f"https://picsum.photos/seed/{tid}/400/300",
                    thumb=f"https://picsum.photos/seed/{tid}/200/150"
                ),
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content=f"Simulation content for {keywords} in thread {i}. ")
                    )
                ],
                tags=["Mock", board_id],
                latest_reply_created_at=now - (i * 1800),
                replies_count=i * 3 % 50,
                url=f"https://example.com/mock/{board_id}/{tid}"
            ))

        # 執行 Mock 排序
        if sorting == "hot":
            all_threads.sort(key=lambda x: x.liked, reverse=True)
        elif sorting == "commented":
            all_threads.sort(key=lambda x: x.comments, reverse=True)
        else: # latest
            all_threads.sort(key=lambda x: x.created_at, reverse=True)

        current_page = 1
        total_page = 1
        threads_to_return = all_threads
        
        if req.page:
            threads_to_return, page_res = pagination(req.page, all_threads)
            current_page = page_res.current_page
            total_page = page_res.total_page

        return pb2.GetThreadsRes(
            threads=[thread.toSaltPb2('single_image_post') for thread in threads_to_return],
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

        comments = [
            Comment(
                id=f"comment_{post_id}_{i}",
                post_id=post_id,
                thread_id=thread_id,
                board_id=board_id,
                author_id=f"cm_user_{i}",
                author_name=f"Commenter {i}",
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content=f"這是一則 Mock 留言 {i}")
                    )
                ],
                created_at=now - (i * 300)
            ) for i in range(1, 4)
        ]
        
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
            url=f"https://example.com/mock/{board_id}/{thread_id}",
            top_5_comments=comments
        )
        
        return pb2.GetOriginalPostRes(
            original_post=thread.toSaltPb2('article_post'),
        )

    def GetReplies(self, req: pb2.GetRepliesReq, context) -> pb2.GetRepliesRes:
        """
        產生窮舉的回覆樹測試資料，涵蓋以下場景:
        - 多層級回覆樹 (最深 3 層)
        - 不同的 replies_count (0, 1, 多個)
        - 有/無圖片的回覆
        - 有/無引用 (REPLY_TO) 的回覆
        - 分頁測試
        """
        board_id = salt.decode(req.board_id)
        thread_id = salt.decode(req.thread_id)
        parent_id = salt.decode(req.parent_id) if req.HasField('parent_id') else None
        
        # Debug logging
        logging.info(f"GetReplies called: board_id={board_id}, thread_id={thread_id}, parent_id={parent_id}")
        
        now = int(time.time())
        posts = []
        
        # === 第一層回覆 (直接回覆 OriginalPost) ===
        if parent_id is None:
            # Reply 1: 有 3 個子回覆 (replies_count=3)，帶圖片
            posts.append(Post(
                id=f"reply_{thread_id}_1",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_reply_1",
                author_name="第一層回覆者 A",
                created_at=now - 5000,
                title="",
                liked=10,
                disliked=1,
                comments=0,
                image=domain_pb2.ImageParagraph(
                    raw=f"https://picsum.photos/seed/reply1/600/400",
                    thumb=f"https://picsum.photos/seed/reply1/200/133"
                ),
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是第一層回覆 #1，有圖片，且有 3 個子回覆。")
                    )
                ],
                tags=["測試", "有子回覆"],
                latest_reply_created_at=now - 2000,
                replies_count=3,  # 有 3 個子回覆
                url=f"https://example.com/mock/{board_id}/{thread_id}/reply1"
            ))
            
            # Reply 2: 有 1 個子回覆 (replies_count=1)，帶引用
            posts.append(Post(
                id=f"reply_{thread_id}_2",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_reply_2",
                author_name="第一層回覆者 B",
                created_at=now - 4500,
                title="",
                liked=5,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_REPLY_TO,
                        reply_to=domain_pb2.ReplyToParagraph(
                            id=salt.encode(f"reply_{thread_id}_1"),
                            author_name="第一層回覆者 A",
                            preview="這是第一層回覆 #1，有圖片..."
                        )
                    ),
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="我引用了 Reply #1，且我有 1 個子回覆。")
                    )
                ],
                tags=["引用測試"],
                latest_reply_created_at=now - 3000,
                replies_count=1,  # 有 1 個子回覆
                url=f"https://example.com/mock/{board_id}/{thread_id}/reply2"
            ))
            
            # Reply 3: 沒有子回覆 (replies_count=0)，純文字葉節點
            posts.append(Post(
                id=f"reply_{thread_id}_3",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_reply_3",
                author_name="第一層回覆者 C",
                created_at=now - 4000,
                title="",
                liked=2,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是第一層回覆 #3，沒有子回覆 (葉節點)。")
                    )
                ],
                tags=["葉節點"],
                latest_reply_created_at=0,
                replies_count=0,  # 葉節點
                url=f"https://example.com/mock/{board_id}/{thread_id}/reply3"
            ))
            
            # Reply 4: 有 2 個子回覆，帶多段內容 (文字 + 圖片 + 文字)
            posts.append(Post(
                id=f"reply_{thread_id}_4",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_reply_4",
                author_name="第一層回覆者 D",
                created_at=now - 3500,
                title="",
                liked=8,
                disliked=1,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是第一層回覆 #4，內容較豐富。")
                    ),
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_IMAGE,
                        image=domain_pb2.ImageParagraph(
                            raw=f"https://picsum.photos/seed/reply4/800/600",
                        )
                    ),
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="圖片後的文字，有 2 個子回覆。")
                    )
                ],
                tags=["多段內容"],
                latest_reply_created_at=now - 1500,
                replies_count=2,  # 有 2 個子回覆
                url=f"https://example.com/mock/{board_id}/{thread_id}/reply4"
            ))
            
            # Reply 5: 沒有子回覆，帶影片
            posts.append(Post(
                id=f"reply_{thread_id}_5",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_reply_5",
                author_name="第一層回覆者 E",
                created_at=now - 3000,
                title="",
                liked=15,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是第一層回覆 #5，帶影片，無子回覆。")
                    ),
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_VIDEO,
                        video=domain_pb2.VideoParagraph(
                            url="https://www.w3schools.com/html/mov_bbb.mp4",
                            thumb="https://picsum.photos/seed/video5/400/300"
                        )
                    )
                ],
                tags=["影片測試", "葉節點"],
                latest_reply_created_at=0,
                replies_count=0,  # 葉節點
                url=f"https://example.com/mock/{board_id}/{thread_id}/reply5"
            ))
        
        # === 第二層回覆 (回覆第一層的回覆) ===
        elif parent_id and parent_id.startswith("reply_") and parent_id.endswith("_1") and not parent_id.startswith("subreply_"):
            # Reply 1 的 3 個子回覆
            # SubReply 1.1: 有 2 個子回覆 (第三層)
            posts.append(Post(
                id=f"subreply_{parent_id}_1",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_subreply_1_1",
                author_name="第二層回覆者 1.1",
                created_at=now - 2500,
                title="",
                liked=3,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_REPLY_TO,
                        reply_to=domain_pb2.ReplyToParagraph(
                            id=salt.encode(parent_id),
                            author_name="第一層回覆者 A",
                            preview="這是第一層回覆 #1..."
                        )
                    ),
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是 Reply #1 的第 1 個子回覆，我還有 2 個子回覆 (第三層)。")
                    )
                ],
                tags=["第二層", "有第三層"],
                latest_reply_created_at=now - 1000,
                replies_count=2,  # 有第三層
                url=None
            ))
            
            # SubReply 1.2: 沒有子回覆 (葉節點)
            posts.append(Post(
                id=f"subreply_{parent_id}_2",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_subreply_1_2",
                author_name="第二層回覆者 1.2",
                created_at=now - 2300,
                title="",
                liked=1,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是 Reply #1 的第 2 個子回覆 (葉節點)。")
                    )
                ],
                tags=["第二層", "葉節點"],
                latest_reply_created_at=0,
                replies_count=0,  # 葉節點
                url=None
            ))
            
            # SubReply 1.3: 帶圖片，沒有子回覆
            posts.append(Post(
                id=f"subreply_{parent_id}_3",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_subreply_1_3",
                author_name="第二層回覆者 1.3",
                created_at=now - 2000,
                title="",
                liked=5,
                disliked=0,
                comments=0,
                image=domain_pb2.ImageParagraph(
                    raw=f"https://picsum.photos/seed/subreply13/500/300",
                    thumb=f"https://picsum.photos/seed/subreply13/200/120"
                ),
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是 Reply #1 的第 3 個子回覆，帶圖片 (葉節點)。")
                    )
                ],
                tags=["第二層", "圖片", "葉節點"],
                latest_reply_created_at=0,
                replies_count=0,  # 葉節點
                url=None
            ))
        
        elif parent_id and parent_id.startswith("reply_") and parent_id.endswith("_2") and not parent_id.startswith("subreply_"):
            # Reply 2 的 1 個子回覆 (葉節點)
            posts.append(Post(
                id=f"subreply_{parent_id}_1",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_subreply_2_1",
                author_name="第二層回覆者 2.1",
                created_at=now - 2800,
                title="",
                liked=2,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_REPLY_TO,
                        reply_to=domain_pb2.ReplyToParagraph(
                            id=salt.encode(parent_id),
                            author_name="第一層回覆者 B",
                            preview="我引用了 Reply #1..."
                        )
                    ),
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是 Reply #2 的唯一子回覆 (葉節點)。")
                    )
                ],
                tags=["第二層", "葉節點"],
                latest_reply_created_at=0,
                replies_count=0,  # 葉節點
                url=None
            ))
        
        elif parent_id and parent_id.startswith("reply_") and parent_id.endswith("_4") and not parent_id.startswith("subreply_"):
            # Reply 4 的 2 個子回覆
            # SubReply 4.1: 葉節點
            posts.append(Post(
                id=f"subreply_{parent_id}_1",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_subreply_4_1",
                author_name="第二層回覆者 4.1",
                created_at=now - 1800,
                title="",
                liked=1,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是 Reply #4 的第 1 個子回覆 (葉節點)。")
                    )
                ],
                tags=["第二層", "葉節點"],
                latest_reply_created_at=0,
                replies_count=0,  # 葉節點
                url=None
            ))
            
            # SubReply 4.2: 葉節點，帶引用
            posts.append(Post(
                id=f"subreply_{parent_id}_2",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_subreply_4_2",
                author_name="第二層回覆者 4.2",
                created_at=now - 1500,
                title="",
                liked=3,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_REPLY_TO,
                        reply_to=domain_pb2.ReplyToParagraph(
                            id=salt.encode(f"subreply_{parent_id}_1"),
                            author_name="第二層回覆者 4.1",
                            preview="這是 Reply #4 的第 1 個子回覆..."
                        )
                    ),
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是 Reply #4 的第 2 個子回覆，引用了 SubReply 4.1 (葉節點)。")
                    )
                ],
                tags=["第二層", "引用", "葉節點"],
                latest_reply_created_at=0,
                replies_count=0,  # 葉節點
                url=None
            ))
        
        # === 第三層回覆 (最深層) ===
        elif parent_id and parent_id.startswith("subreply_reply_") and parent_id.endswith("_1_1"):
            # SubReply 1.1 的 2 個子回覆 (都是葉節點)
            posts.append(Post(
                id=f"subreply_{parent_id}_1",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_subreply_1_1_1",
                author_name="第三層回覆者 1.1.1",
                created_at=now - 900,
                title="",
                liked=1,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是第三層回覆 1.1.1 (最深層葉節點)。")
                    )
                ],
                tags=["第三層", "葉節點"],
                latest_reply_created_at=0,
                replies_count=0,  # 葉節點
                url=None
            ))
            
            posts.append(Post(
                id=f"subreply_{parent_id}_2",
                thread_id=thread_id,
                board_id=board_id,
                author_id="user_subreply_1_1_2",
                author_name="第三層回覆者 1.1.2",
                created_at=now - 800,
                title="",
                liked=0,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_REPLY_TO,
                        reply_to=domain_pb2.ReplyToParagraph(
                            id=salt.encode(f"subreply_{parent_id}_1"),
                            author_name="第三層回覆者 1.1.1",
                            preview="這是第三層回覆 1.1.1..."
                        )
                    ),
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content="這是第三層回覆 1.1.2，引用了 1.1.1 (最深層葉節點)。")
                    )
                ],
                tags=["第三層", "引用", "葉節點"],
                latest_reply_created_at=0,
                replies_count=0,  # 葉節點
                url=None
            ))

        # 處理分頁
        current_page = 1
        total_page = 1
        if req.page:
            posts, page_res = pagination(req.page, posts)
            current_page = page_res.current_page
            total_page = page_res.total_page

        return pb2.GetRepliesRes(
            replies=[post.toSaltPb2('article_post') for post in posts],
            page=domain_pb2.PaginationRes(
                current_page=current_page,
                total_page=total_page,
            ),
        )

    def GetComments(self, req: pb2.GetCommentsReq, context) -> pb2.GetCommentsRes:
        board_id = salt.decode(req.board_id)
        thread_id = salt.decode(req.thread_id)
        post_id = salt.decode(req.post_id)
        
        now = int(time.time())
        comments = [
            Comment(
                id=f"full_comment_{post_id}_{i}",
                post_id=post_id,
                thread_id=thread_id,
                board_id=board_id,
                author_id=f"cm_user_{i}",
                author_name=f"Commenter {i}",
                contents=[
                    domain_pb2.Paragraph(
                        type=domain_pb2.ParagraphType.PARAGRAPH_TYPE_TEXT,
                        text=domain_pb2.TextParagraph(content=f"這是一則完整加載的留言 {i}")
                    )
                ],
                created_at=now - (i * 300)
            ) for i in range(1, 11)
        ]
        
        return pb2.GetCommentsRes(
            comments=[c.toSaltPb2() for c in comments],
            page=domain_pb2.PaginationRes(
                current_page=1,
                total_page=1,
            ),
        )

    def GetBoardSortOptions(self, req: pb2.GetBoardSortOptionsReq, context) -> pb2.GetBoardSortOptionsRes:
        # Mock board sort options mapping
        mock_sort_options = {
            "board_1": ["latest", "hot"],
            "board_2": ["newest", "recommend"],
            "board_3": ["latest", "commented"],
        }
        
        results = []
        for encoded_bid in req.board_ids:
            try:
                board_id = salt.decode(encoded_bid)
                if board_id in mock_sort_options:
                    results.append(pb2.BoardSortOption(
                        board_id=encoded_bid,
                        options=mock_sort_options[board_id]
                    ))
            except Exception:
                continue
                
        return pb2.GetBoardSortOptionsRes(options=results)
        