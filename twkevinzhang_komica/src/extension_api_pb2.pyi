from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ParagraphType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PARAGRAPH_TYPE_UNSPECIFIED: _ClassVar[ParagraphType]
    PARAGRAPH_TYPE_QUOTE: _ClassVar[ParagraphType]
    PARAGRAPH_TYPE_REPLY_TO: _ClassVar[ParagraphType]
    PARAGRAPH_TYPE_TEXT: _ClassVar[ParagraphType]
    PARAGRAPH_TYPE_NEW_LINE: _ClassVar[ParagraphType]
    PARAGRAPH_TYPE_IMAGE: _ClassVar[ParagraphType]
    PARAGRAPH_TYPE_LINK: _ClassVar[ParagraphType]
    PARAGRAPH_TYPE_VIDEO: _ClassVar[ParagraphType]
PARAGRAPH_TYPE_UNSPECIFIED: ParagraphType
PARAGRAPH_TYPE_QUOTE: ParagraphType
PARAGRAPH_TYPE_REPLY_TO: ParagraphType
PARAGRAPH_TYPE_TEXT: ParagraphType
PARAGRAPH_TYPE_NEW_LINE: ParagraphType
PARAGRAPH_TYPE_IMAGE: ParagraphType
PARAGRAPH_TYPE_LINK: ParagraphType
PARAGRAPH_TYPE_VIDEO: ParagraphType

class PaginationReq(_message.Message):
    __slots__ = ("page", "page_size", "limit", "prev_cursor", "next_cursor")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PREV_CURSOR_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    limit: int
    prev_cursor: str
    next_cursor: str
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., limit: _Optional[int] = ..., prev_cursor: _Optional[str] = ..., next_cursor: _Optional[str] = ...) -> None: ...

class PaginationRes(_message.Message):
    __slots__ = ("total_page", "current_page", "page_size", "prev_cursor", "next_cursor")
    TOTAL_PAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PREV_CURSOR_FIELD_NUMBER: _ClassVar[int]
    NEXT_CURSOR_FIELD_NUMBER: _ClassVar[int]
    total_page: int
    current_page: int
    page_size: int
    prev_cursor: str
    next_cursor: str
    def __init__(self, total_page: _Optional[int] = ..., current_page: _Optional[int] = ..., page_size: _Optional[int] = ..., prev_cursor: _Optional[str] = ..., next_cursor: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSiteReq(_message.Message):
    __slots__ = ("pkg_name",)
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    def __init__(self, pkg_name: _Optional[str] = ...) -> None: ...

class GetSiteRes(_message.Message):
    __slots__ = ("site",)
    SITE_FIELD_NUMBER: _ClassVar[int]
    site: Site
    def __init__(self, site: _Optional[_Union[Site, _Mapping]] = ...) -> None: ...

class Site(_message.Message):
    __slots__ = ("pkg_name", "id", "icon", "name", "description", "url")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    id: str
    icon: str
    name: str
    description: str
    url: str
    def __init__(self, pkg_name: _Optional[str] = ..., id: _Optional[str] = ..., icon: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class GetBoardsReq(_message.Message):
    __slots__ = ("pkg_name", "site_id", "page")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    site_id: str
    page: PaginationReq
    def __init__(self, pkg_name: _Optional[str] = ..., site_id: _Optional[str] = ..., page: _Optional[_Union[PaginationReq, _Mapping]] = ...) -> None: ...

class GetBoardsRes(_message.Message):
    __slots__ = ("boards", "page")
    BOARDS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    boards: _containers.RepeatedCompositeFieldContainer[Board]
    page: PaginationRes
    def __init__(self, boards: _Optional[_Iterable[_Union[Board, _Mapping]]] = ..., page: _Optional[_Union[PaginationRes, _Mapping]] = ...) -> None: ...

class Board(_message.Message):
    __slots__ = ("pkg_name", "site_id", "id", "name", "icon", "large_welcome_image", "url", "supported_threads_sorting")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    LARGE_WELCOME_IMAGE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    SUPPORTED_THREADS_SORTING_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    site_id: str
    id: str
    name: str
    icon: str
    large_welcome_image: str
    url: str
    supported_threads_sorting: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, pkg_name: _Optional[str] = ..., site_id: _Optional[str] = ..., id: _Optional[str] = ..., name: _Optional[str] = ..., icon: _Optional[str] = ..., large_welcome_image: _Optional[str] = ..., url: _Optional[str] = ..., supported_threads_sorting: _Optional[_Iterable[str]] = ...) -> None: ...

class GetThreadInfosReq(_message.Message):
    __slots__ = ("pkg_name", "site_id", "boards_sorting", "page", "keywords")
    class BoardsSortingEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    BOARDS_SORTING_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    site_id: str
    boards_sorting: _containers.ScalarMap[str, str]
    page: PaginationReq
    keywords: str
    def __init__(self, pkg_name: _Optional[str] = ..., site_id: _Optional[str] = ..., boards_sorting: _Optional[_Mapping[str, str]] = ..., page: _Optional[_Union[PaginationReq, _Mapping]] = ..., keywords: _Optional[str] = ...) -> None: ...

class GetThreadInfosRes(_message.Message):
    __slots__ = ("thread_infos", "page")
    THREAD_INFOS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    thread_infos: _containers.RepeatedCompositeFieldContainer[Post]
    page: PaginationRes
    def __init__(self, thread_infos: _Optional[_Iterable[_Union[Post, _Mapping]]] = ..., page: _Optional[_Union[PaginationRes, _Mapping]] = ...) -> None: ...

class GetThreadPostReq(_message.Message):
    __slots__ = ("pkg_name", "site_id", "board_id", "thread_id", "post_id")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    BOARD_ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    site_id: str
    board_id: str
    thread_id: str
    post_id: str
    def __init__(self, pkg_name: _Optional[str] = ..., site_id: _Optional[str] = ..., board_id: _Optional[str] = ..., thread_id: _Optional[str] = ..., post_id: _Optional[str] = ...) -> None: ...

class GetThreadPostRes(_message.Message):
    __slots__ = ("thread_post",)
    THREAD_POST_FIELD_NUMBER: _ClassVar[int]
    thread_post: Post
    def __init__(self, thread_post: _Optional[_Union[Post, _Mapping]] = ...) -> None: ...

class GetRegardingPostsReq(_message.Message):
    __slots__ = ("pkg_name", "site_id", "board_id", "thread_id", "reply_to_id", "page")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    BOARD_ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    site_id: str
    board_id: str
    thread_id: str
    reply_to_id: str
    page: PaginationReq
    def __init__(self, pkg_name: _Optional[str] = ..., site_id: _Optional[str] = ..., board_id: _Optional[str] = ..., thread_id: _Optional[str] = ..., reply_to_id: _Optional[str] = ..., page: _Optional[_Union[PaginationReq, _Mapping]] = ...) -> None: ...

class GetRegardingPostsRes(_message.Message):
    __slots__ = ("regarding_posts", "page")
    REGARDING_POSTS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    regarding_posts: _containers.RepeatedCompositeFieldContainer[Post]
    page: PaginationRes
    def __init__(self, regarding_posts: _Optional[_Iterable[_Union[Post, _Mapping]]] = ..., page: _Optional[_Union[PaginationRes, _Mapping]] = ...) -> None: ...

class Paragraph(_message.Message):
    __slots__ = ("type", "image", "video", "text", "new_line", "quote", "reply_to", "link")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    VIDEO_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    NEW_LINE_FIELD_NUMBER: _ClassVar[int]
    QUOTE_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    type: ParagraphType
    image: ImageParagraph
    video: VideoParagraph
    text: TextParagraph
    new_line: NewLineParagraph
    quote: QuoteParagraph
    reply_to: ReplyToParagraph
    link: LinkParagraph
    def __init__(self, type: _Optional[_Union[ParagraphType, str]] = ..., image: _Optional[_Union[ImageParagraph, _Mapping]] = ..., video: _Optional[_Union[VideoParagraph, _Mapping]] = ..., text: _Optional[_Union[TextParagraph, _Mapping]] = ..., new_line: _Optional[_Union[NewLineParagraph, _Mapping]] = ..., quote: _Optional[_Union[QuoteParagraph, _Mapping]] = ..., reply_to: _Optional[_Union[ReplyToParagraph, _Mapping]] = ..., link: _Optional[_Union[LinkParagraph, _Mapping]] = ...) -> None: ...

class ImageParagraph(_message.Message):
    __slots__ = ("thumb", "raw")
    THUMB_FIELD_NUMBER: _ClassVar[int]
    RAW_FIELD_NUMBER: _ClassVar[int]
    thumb: str
    raw: str
    def __init__(self, thumb: _Optional[str] = ..., raw: _Optional[str] = ...) -> None: ...

class VideoParagraph(_message.Message):
    __slots__ = ("thumb", "url")
    THUMB_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    thumb: str
    url: str
    def __init__(self, thumb: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class TextParagraph(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: str
    def __init__(self, content: _Optional[str] = ...) -> None: ...

class NewLineParagraph(_message.Message):
    __slots__ = ("symbol",)
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    def __init__(self, symbol: _Optional[str] = ...) -> None: ...

class QuoteParagraph(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: str
    def __init__(self, content: _Optional[str] = ...) -> None: ...

class ReplyToParagraph(_message.Message):
    __slots__ = ("id", "author_name", "preview")
    ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_NAME_FIELD_NUMBER: _ClassVar[int]
    PREVIEW_FIELD_NUMBER: _ClassVar[int]
    id: str
    author_name: str
    preview: str
    def __init__(self, id: _Optional[str] = ..., author_name: _Optional[str] = ..., preview: _Optional[str] = ...) -> None: ...

class LinkParagraph(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: str
    def __init__(self, content: _Optional[str] = ...) -> None: ...

class Post(_message.Message):
    __slots__ = ("pkg_name", "site_id", "board_id", "thread_id", "id", "author_id", "author_name", "created_at", "title", "liked", "disliked", "comments", "contents", "tags", "latest_regarding_post_created_at", "regarding_posts_count", "url")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    BOARD_ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    LIKED_FIELD_NUMBER: _ClassVar[int]
    DISLIKED_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    LATEST_REGARDING_POST_CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    REGARDING_POSTS_COUNT_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    site_id: str
    board_id: str
    thread_id: str
    id: str
    author_id: str
    author_name: str
    created_at: int
    title: str
    liked: int
    disliked: int
    comments: int
    contents: _containers.RepeatedCompositeFieldContainer[Paragraph]
    tags: _containers.RepeatedScalarFieldContainer[str]
    latest_regarding_post_created_at: int
    regarding_posts_count: int
    url: str
    def __init__(self, pkg_name: _Optional[str] = ..., site_id: _Optional[str] = ..., board_id: _Optional[str] = ..., thread_id: _Optional[str] = ..., id: _Optional[str] = ..., author_id: _Optional[str] = ..., author_name: _Optional[str] = ..., created_at: _Optional[int] = ..., title: _Optional[str] = ..., liked: _Optional[int] = ..., disliked: _Optional[int] = ..., comments: _Optional[int] = ..., contents: _Optional[_Iterable[_Union[Paragraph, _Mapping]]] = ..., tags: _Optional[_Iterable[str]] = ..., latest_regarding_post_created_at: _Optional[int] = ..., regarding_posts_count: _Optional[int] = ..., url: _Optional[str] = ...) -> None: ...

class GetCommentsReq(_message.Message):
    __slots__ = ("pkg_name", "site_id", "board_id", "thread_id", "post_id", "page")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    BOARD_ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    site_id: str
    board_id: str
    thread_id: str
    post_id: str
    page: PaginationReq
    def __init__(self, pkg_name: _Optional[str] = ..., site_id: _Optional[str] = ..., board_id: _Optional[str] = ..., thread_id: _Optional[str] = ..., post_id: _Optional[str] = ..., page: _Optional[_Union[PaginationReq, _Mapping]] = ...) -> None: ...

class GetCommentsRes(_message.Message):
    __slots__ = ("comments", "page")
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    comments: _containers.RepeatedCompositeFieldContainer[Comment]
    page: PaginationRes
    def __init__(self, comments: _Optional[_Iterable[_Union[Comment, _Mapping]]] = ..., page: _Optional[_Union[PaginationRes, _Mapping]] = ...) -> None: ...

class Comment(_message.Message):
    __slots__ = ("pkg_name", "site_id", "board_id", "thread_id", "post_id", "id", "author_id", "author_name", "contents", "created_at")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    SITE_ID_FIELD_NUMBER: _ClassVar[int]
    BOARD_ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTENTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    site_id: str
    board_id: str
    thread_id: str
    post_id: str
    id: str
    author_id: str
    author_name: str
    contents: _containers.RepeatedCompositeFieldContainer[Paragraph]
    created_at: int
    def __init__(self, pkg_name: _Optional[str] = ..., site_id: _Optional[str] = ..., board_id: _Optional[str] = ..., thread_id: _Optional[str] = ..., post_id: _Optional[str] = ..., id: _Optional[str] = ..., author_id: _Optional[str] = ..., author_name: _Optional[str] = ..., contents: _Optional[_Iterable[_Union[Paragraph, _Mapping]]] = ..., created_at: _Optional[int] = ...) -> None: ...
