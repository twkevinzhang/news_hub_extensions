import mock_domain_models_pb2 as _mock_domain_models_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetBoardsReq(_message.Message):
    __slots__ = ("pkg_name", "page")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    page: _mock_domain_models_pb2.PaginationReq
    def __init__(self, pkg_name: _Optional[str] = ..., page: _Optional[_Union[_mock_domain_models_pb2.PaginationReq, _Mapping]] = ...) -> None: ...

class GetBoardsRes(_message.Message):
    __slots__ = ("boards", "page")
    BOARDS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    boards: _containers.RepeatedCompositeFieldContainer[_mock_domain_models_pb2.Board]
    page: _mock_domain_models_pb2.PaginationRes
    def __init__(self, boards: _Optional[_Iterable[_Union[_mock_domain_models_pb2.Board, _Mapping]]] = ..., page: _Optional[_Union[_mock_domain_models_pb2.PaginationRes, _Mapping]] = ...) -> None: ...

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
    page: _mock_domain_models_pb2.PaginationReq
    keywords: str
    def __init__(self, pkg_name: _Optional[str] = ..., board_id: _Optional[str] = ..., sort: _Optional[str] = ..., page: _Optional[_Union[_mock_domain_models_pb2.PaginationReq, _Mapping]] = ..., keywords: _Optional[str] = ...) -> None: ...

class GetThreadsRes(_message.Message):
    __slots__ = ("threads", "page")
    THREADS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    threads: _containers.RepeatedCompositeFieldContainer[_mock_domain_models_pb2.Post]
    page: _mock_domain_models_pb2.PaginationRes
    def __init__(self, threads: _Optional[_Iterable[_Union[_mock_domain_models_pb2.Post, _Mapping]]] = ..., page: _Optional[_Union[_mock_domain_models_pb2.PaginationRes, _Mapping]] = ...) -> None: ...

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
    original_post: _mock_domain_models_pb2.Post
    def __init__(self, original_post: _Optional[_Union[_mock_domain_models_pb2.Post, _Mapping]] = ...) -> None: ...

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
    page: _mock_domain_models_pb2.PaginationReq
    def __init__(self, pkg_name: _Optional[str] = ..., board_id: _Optional[str] = ..., thread_id: _Optional[str] = ..., reply_to_id: _Optional[str] = ..., page: _Optional[_Union[_mock_domain_models_pb2.PaginationReq, _Mapping]] = ...) -> None: ...

class GetRepliesRes(_message.Message):
    __slots__ = ("replies", "page")
    REPLIES_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    replies: _containers.RepeatedCompositeFieldContainer[_mock_domain_models_pb2.Post]
    page: _mock_domain_models_pb2.PaginationRes
    def __init__(self, replies: _Optional[_Iterable[_Union[_mock_domain_models_pb2.Post, _Mapping]]] = ..., page: _Optional[_Union[_mock_domain_models_pb2.PaginationRes, _Mapping]] = ...) -> None: ...

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
    page: _mock_domain_models_pb2.PaginationReq
    def __init__(self, pkg_name: _Optional[str] = ..., board_id: _Optional[str] = ..., thread_id: _Optional[str] = ..., post_id: _Optional[str] = ..., page: _Optional[_Union[_mock_domain_models_pb2.PaginationReq, _Mapping]] = ...) -> None: ...

class GetCommentsRes(_message.Message):
    __slots__ = ("comments", "page")
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    comments: _containers.RepeatedCompositeFieldContainer[_mock_domain_models_pb2.Comment]
    page: _mock_domain_models_pb2.PaginationRes
    def __init__(self, comments: _Optional[_Iterable[_Union[_mock_domain_models_pb2.Comment, _Mapping]]] = ..., page: _Optional[_Union[_mock_domain_models_pb2.PaginationRes, _Mapping]] = ...) -> None: ...

class ListInstalledExtensionsRes(_message.Message):
    __slots__ = ("extensions",)
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    extensions: _containers.RepeatedCompositeFieldContainer[_mock_domain_models_pb2.Extension]
    def __init__(self, extensions: _Optional[_Iterable[_Union[_mock_domain_models_pb2.Extension, _Mapping]]] = ...) -> None: ...

class GetInstalledExtensionReq(_message.Message):
    __slots__ = ("pkg_name",)
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    def __init__(self, pkg_name: _Optional[str] = ...) -> None: ...

class GetInstalledExtensionRes(_message.Message):
    __slots__ = ("extension",)
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    extension: _mock_domain_models_pb2.Extension
    def __init__(self, extension: _Optional[_Union[_mock_domain_models_pb2.Extension, _Mapping]] = ...) -> None: ...

class InstallExtensionReq(_message.Message):
    __slots__ = ("pkg_name", "repo_url")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    REPO_URL_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    repo_url: str
    def __init__(self, pkg_name: _Optional[str] = ..., repo_url: _Optional[str] = ...) -> None: ...

class UninstallExtensionReq(_message.Message):
    __slots__ = ("pkg_name",)
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    def __init__(self, pkg_name: _Optional[str] = ...) -> None: ...

class GetInstallProgressReq(_message.Message):
    __slots__ = ("pkg_name",)
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    def __init__(self, pkg_name: _Optional[str] = ...) -> None: ...

class GetInstallProgressRes(_message.Message):
    __slots__ = ("progress",)
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    progress: int
    def __init__(self, progress: _Optional[int] = ...) -> None: ...

class ListRemoteExtensionsReq(_message.Message):
    __slots__ = ("keyword",)
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    keyword: str
    def __init__(self, keyword: _Optional[str] = ...) -> None: ...

class ListRemoteExtensionsRes(_message.Message):
    __slots__ = ("extensions",)
    EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    extensions: _containers.RepeatedCompositeFieldContainer[_mock_domain_models_pb2.RemoteExtension]
    def __init__(self, extensions: _Optional[_Iterable[_Union[_mock_domain_models_pb2.RemoteExtension, _Mapping]]] = ...) -> None: ...

class ListExtensionReposRes(_message.Message):
    __slots__ = ("repos",)
    REPOS_FIELD_NUMBER: _ClassVar[int]
    repos: _containers.RepeatedCompositeFieldContainer[_mock_domain_models_pb2.ExtensionRepo]
    def __init__(self, repos: _Optional[_Iterable[_Union[_mock_domain_models_pb2.ExtensionRepo, _Mapping]]] = ...) -> None: ...

class AddExtensionRepoReq(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class AddExtensionRepoRes(_message.Message):
    __slots__ = ("url", "added_at", "display_name", "website", "signing_key_fingerprint", "icon")
    URL_FIELD_NUMBER: _ClassVar[int]
    ADDED_AT_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    SIGNING_KEY_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    url: str
    added_at: int
    display_name: str
    website: str
    signing_key_fingerprint: str
    icon: str
    def __init__(self, url: _Optional[str] = ..., added_at: _Optional[int] = ..., display_name: _Optional[str] = ..., website: _Optional[str] = ..., signing_key_fingerprint: _Optional[str] = ..., icon: _Optional[str] = ...) -> None: ...

class RemoveExtensionRepoReq(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class HealthCheckReq(_message.Message):
    __slots__ = ("service",)
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    service: str
    def __init__(self, service: _Optional[str] = ...) -> None: ...

class HealthCheckRes(_message.Message):
    __slots__ = ("status", "message")
    class ServingStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNKNOWN: _ClassVar[HealthCheckRes.ServingStatus]
        SERVING: _ClassVar[HealthCheckRes.ServingStatus]
        NOT_SERVING: _ClassVar[HealthCheckRes.ServingStatus]
        SERVICE_UNKNOWN: _ClassVar[HealthCheckRes.ServingStatus]
    UNKNOWN: HealthCheckRes.ServingStatus
    SERVING: HealthCheckRes.ServingStatus
    NOT_SERVING: HealthCheckRes.ServingStatus
    SERVICE_UNKNOWN: HealthCheckRes.ServingStatus
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: HealthCheckRes.ServingStatus
    message: str
    def __init__(self, status: _Optional[_Union[HealthCheckRes.ServingStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class WatchLogsReq(_message.Message):
    __slots__ = ("min_level", "logger_filter")
    MIN_LEVEL_FIELD_NUMBER: _ClassVar[int]
    LOGGER_FILTER_FIELD_NUMBER: _ClassVar[int]
    min_level: _mock_domain_models_pb2.LogLevel
    logger_filter: str
    def __init__(self, min_level: _Optional[_Union[_mock_domain_models_pb2.LogLevel, str]] = ..., logger_filter: _Optional[str] = ...) -> None: ...

class GetLogsReq(_message.Message):
    __slots__ = ("start_time", "end_time", "min_level", "logger_filter", "limit")
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    MIN_LEVEL_FIELD_NUMBER: _ClassVar[int]
    LOGGER_FILTER_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    start_time: int
    end_time: int
    min_level: _mock_domain_models_pb2.LogLevel
    logger_filter: str
    limit: int
    def __init__(self, start_time: _Optional[int] = ..., end_time: _Optional[int] = ..., min_level: _Optional[_Union[_mock_domain_models_pb2.LogLevel, str]] = ..., logger_filter: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class GetLogsRes(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[_mock_domain_models_pb2.LogEntry]
    def __init__(self, entries: _Optional[_Iterable[_Union[_mock_domain_models_pb2.LogEntry, _Mapping]]] = ...) -> None: ...

class SetLogLevelReq(_message.Message):
    __slots__ = ("level",)
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    level: _mock_domain_models_pb2.LogLevel
    def __init__(self, level: _Optional[_Union[_mock_domain_models_pb2.LogLevel, str]] = ...) -> None: ...

class BoardSortOption(_message.Message):
    __slots__ = ("board_id", "options")
    BOARD_ID_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    board_id: str
    options: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, board_id: _Optional[str] = ..., options: _Optional[_Iterable[str]] = ...) -> None: ...

class GetBoardSortOptionsReq(_message.Message):
    __slots__ = ("pkg_name", "board_ids")
    PKG_NAME_FIELD_NUMBER: _ClassVar[int]
    BOARD_IDS_FIELD_NUMBER: _ClassVar[int]
    pkg_name: str
    board_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, pkg_name: _Optional[str] = ..., board_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetBoardSortOptionsRes(_message.Message):
    __slots__ = ("options",)
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    options: _containers.RepeatedCompositeFieldContainer[BoardSortOption]
    def __init__(self, options: _Optional[_Iterable[_Union[BoardSortOption, _Mapping]]] = ...) -> None: ...
