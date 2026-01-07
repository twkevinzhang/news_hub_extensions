import komica_domain_models_pb2 as _komica_domain_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetBoardsReq(_message.Message):
    __slots__ = ("pkg_name", "page")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    page: _komica_domain_models_pb2.PaginationReq
    def __init__(self, pkg_name: _Optional[str] = ..., page: _Optional[_Union[_komica_domain_models_pb2.PaginationReq, _Mapping]] = ...) -> None: ...

class GetBoardsRes(_message.Message):
    __slots__ = ("boards", "page")
    BOARDS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    boards: _containers.RepeatedCompositeFieldContainer[_komica_domain_models_pb2.Board]
    page: _komica_domain_models_pb2.PaginationRes
    def __init__(self, boards: _Optional[_Iterable[_Union[_komica_domain_models_pb2.Board, _Mapping]]] = ..., page: _Optional[_Union[_komica_domain_models_pb2.PaginationRes, _Mapping]] = ...) -> None: ...

class GetThreadsReq(_message.Message):
    __slots__ = ("pkg_name", "board_id", "sort", "page", "keywords")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    BOARD_ID_FIELD_NUMBER: _ClassVar[int]
    SORT_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    board_id: str
    sort: str
    page: _komica_domain_models_pb2.PaginationReq
    keywords: str
    def __init__(self, pkg_name: _Optional[str] = ..., board_id: _Optional[str] = ..., sort: _Optional[str] = ..., page: _Optional[_Union[_komica_domain_models_pb2.PaginationReq, _Mapping]] = ..., keywords: _Optional[str] = ...) -> None: ...

class GetThreadsRes(_message.Message):
    __slots__ = ("threads", "page")
    THREADS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    threads: _containers.RepeatedCompositeFieldContainer[_komica_domain_models_pb2.Post]
    page: _komica_domain_models_pb2.PaginationRes
    def __init__(self, threads: _Optional[_Iterable[_Union[_komica_domain_models_pb2.Post, _Mapping]]] = ..., page: _Optional[_Union[_komica_domain_models_pb2.PaginationRes, _Mapping]] = ...) -> None: ...

class GetOriginalPostReq(_message.Message):
    __slots__ = ("pkg_name", "board_id", "thread_id", "post_id")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    BOARD_ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    board_id: str
    thread_id: str
    post_id: str
    def __init__(self, pkg_name: _Optional[str] = ..., board_id: _Optional[str] = ..., thread_id: _Optional[str] = ..., post_id: _Optional[str] = ...) -> None: ...

class GetOriginalPostRes(_message.Message):
    __slots__ = ("original_post",)
    ORIGINAL_POST_FIELD_NUMBER: _ClassVar[int]
    original_post: _komica_domain_models_pb2.Post
    def __init__(self, original_post: _Optional[_Union[_komica_domain_models_pb2.Post, _Mapping]] = ...) -> None: ...

class GetRepliesReq(_message.Message):
    __slots__ = ("pkg_name", "board_id", "thread_id", "reply_to_id", "page")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    BOARD_ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    REPLY_TO_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    board_id: str
    thread_id: str
    reply_to_id: str
    page: _komica_domain_models_pb2.PaginationReq
    def __init__(self, pkg_name: _Optional[str] = ..., board_id: _Optional[str] = ..., thread_id: _Optional[str] = ..., reply_to_id: _Optional[str] = ..., page: _Optional[_Union[_komica_domain_models_pb2.PaginationReq, _Mapping]] = ...) -> None: ...

class GetRepliesRes(_message.Message):
    __slots__ = ("replies", "page")
    REPLIES_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    replies: _containers.RepeatedCompositeFieldContainer[_komica_domain_models_pb2.Post]
    page: _komica_domain_models_pb2.PaginationRes
    def __init__(self, replies: _Optional[_Iterable[_Union[_komica_domain_models_pb2.Post, _Mapping]]] = ..., page: _Optional[_Union[_komica_domain_models_pb2.PaginationRes, _Mapping]] = ...) -> None: ...

class GetCommentsReq(_message.Message):
    __slots__ = ("pkg_name", "board_id", "thread_id", "post_id", "page")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    BOARD_ID_FIELD_NUMBER: _ClassVar[int]
    THREAD_ID_FIELD_NUMBER: _ClassVar[int]
    POST_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    board_id: str
    thread_id: str
    post_id: str
    page: _komica_domain_models_pb2.PaginationReq
    def __init__(self, pkg_name: _Optional[str] = ..., board_id: _Optional[str] = ..., thread_id: _Optional[str] = ..., post_id: _Optional[str] = ..., page: _Optional[_Union[_komica_domain_models_pb2.PaginationReq, _Mapping]] = ...) -> None: ...

class GetCommentsRes(_message.Message):
    __slots__ = ("comments", "page")
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    comments: _containers.RepeatedCompositeFieldContainer[_komica_domain_models_pb2.Comment]
    page: _komica_domain_models_pb2.PaginationRes
    def __init__(self, comments: _Optional[_Iterable[_Union[_komica_domain_models_pb2.Comment, _Mapping]]] = ..., page: _Optional[_Union[_komica_domain_models_pb2.PaginationRes, _Mapping]] = ...) -> None: ...
