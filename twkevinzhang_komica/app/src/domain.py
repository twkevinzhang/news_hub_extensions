import extension_api_pb2 as pb2
import salt


class Post:
    def __init__(self,
                 id: str,
                 thread_id: str | None,
                 board_id: str | None,
                 site_id: str | None,
                 author_id: str,
                 author_name: str,
                 created_at: int,
                 title: str,
                 liked: int,
                 disliked: int,
                 comments: int,
                 contents: list[pb2.Paragraph],
                 tags: list[str],
                 latest_regarding_post_created_at: int,
                 regarding_posts_count: int,
                 url: str | None,
                 ):
        self.id = id
        self.thread_id = thread_id
        self.board_id = board_id
        self.site_id = site_id
        self.author_id = author_id
        self.author_name = author_name
        self.created_at = created_at
        self.title = title
        self.liked = liked
        self.disliked = disliked
        self.comments = comments
        self.contents = contents
        self.tags = tags
        self.latest_regarding_post_created_at = latest_regarding_post_created_at
        self.regarding_posts_count = regarding_posts_count
        self.url = url

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Post({self.__dict__})"

    def toSaltPb2(self) -> pb2.Post:
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

        return pb2.Post(
            id=salt.encode(self.id),
            thread_id=salt.encode(self.thread_id),
            board_id=salt.encode(self.board_id),
            site_id=salt.encode(self.site_id),
            author_id=salt.encode(self.author_id),
            author_name=self.author_name,
            created_at=self.created_at,
            title=self.title,
            liked=self.liked,
            disliked=self.disliked,
            comments=self.comments,
            contents=new_contents,
            tags=self.tags,
            latest_regarding_post_created_at=self.latest_regarding_post_created_at,
            regarding_posts_count=self.regarding_posts_count,
            url=self.url
        )

def board_id_to_url_prefix(board_id: str) -> str:
    [subdomain, id] = board_id.split("/")
    return f"https://{subdomain}.komica1.org/{id}"

class OverPageError(Exception):
    pass
