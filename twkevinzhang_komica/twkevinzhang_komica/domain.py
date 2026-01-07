from . import extension_api_pb2 as pb2
from . import salt


pkg_name = "twkevinzhang_komica"


class Post:
    def __init__(self,
                 id: str,
                 thread_id: str | None,
                 board_id: str | None,
                 author_id: str,
                 author_name: str,
                 created_at: int,
                 title: str,
                 liked: int,
                 disliked: int,
                 comments: int,
                 image: pb2.ImageParagraph | None,
                 contents: list[pb2.Paragraph],
                 tags: list[str],
                 latest_reply_created_at: int,
                 replies_count: int,
                 url: str | None,
                 ):
        self.pkg_name = pkg_name
        self.board_id = board_id
        self.thread_id = thread_id
        self.id = id
        self.author_id = author_id
        self.author_name = author_name
        self.created_at = created_at
        self.title = title
        self.liked = liked
        self.disliked = disliked
        self.comments = comments
        self.image = image
        self.contents = contents
        self.tags = tags
        self.latest_reply_created_at = latest_reply_created_at
        self.replies_count = replies_count
        self.url = url

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Post({self.__dict__})"

    def toSaltPb2(
            self,
            ui_layout: 'article_post' or 'single_image_post',
    ) -> pb2.Post:
        new_contents = []
        for content in self.contents:
            if content.type == pb2.ParagraphType.PARAGRAPH_TYPE_REPLY_TO:
                new_contents.append(pb2.Paragraph(
                    type=pb2.ParagraphType.PARAGRAPH_TYPE_REPLY_TO,
                    reply_to=pb2.ReplyToParagraph(
                        id=salt.encode(content.reply_to.id),
                        author_name=content.reply_to.author_name,
                        preview=content.reply_to.preview
                    )
                ))
            else:
                new_contents.append(content)
        if ui_layout == 'article_post':
            return pb2.Post(
                pkg_name=self.pkg_name,
                id=salt.encode(self.id),
                thread_id=salt.encode(self.thread_id),
                board_id=salt.encode(self.board_id),
                article_post = pb2.ArticlePost(
                    author_id=salt.encode(self.author_id),
                    author_name=self.author_name,
                    created_at=self.created_at,
                    title=self.title,
                    liked=self.liked,
                    disliked=self.disliked,
                    contents=new_contents,
                    tags=self.tags,
                    latest_reply_created_at=self.latest_reply_created_at,
                    replies_count=self.replies_count,
                    url=self.url
                ),
            )
        elif ui_layout == 'single_image_post':
            return pb2.Post(
                pkg_name=self.pkg_name,
                id=salt.encode(self.id),
                thread_id=salt.encode(self.thread_id),
                board_id=salt.encode(self.board_id),
                single_image_post = pb2.SingleImagePost(
                    author_id=salt.encode(self.author_id),
                    author_name=self.author_name,
                    created_at=self.created_at,
                    title=self.title,
                    liked=self.liked,
                    disliked=self.disliked,
                    contents=new_contents,
                    image=self.image,
                    tags=self.tags,
                    latest_reply_created_at=self.latest_reply_created_at,
                    replies_count=self.replies_count,
                    url=self.url
                ),
            )

def board_id_to_url_prefix(board_id: str) -> str:
    [subdomain, id] = board_id.split("/")
    return f"https://{subdomain}.komica1.org/{id}"

class OverPageError(Exception):
    pass
