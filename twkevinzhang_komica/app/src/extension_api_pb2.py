# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: extension_api.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'extension_api.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x65xtension_api.proto\x12\x02pb\"\xc3\x01\n\rPaginationReq\x12\x11\n\x04page\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x16\n\tpage_size\x18\x03 \x01(\x05H\x01\x88\x01\x01\x12\x12\n\x05limit\x18\x02 \x01(\x05H\x02\x88\x01\x01\x12\x18\n\x0bprev_cursor\x18\x04 \x01(\tH\x03\x88\x01\x01\x12\x18\n\x0bnext_cursor\x18\x05 \x01(\tH\x04\x88\x01\x01\x42\x07\n\x05_pageB\x0c\n\n_page_sizeB\x08\n\x06_limitB\x0e\n\x0c_prev_cursorB\x0e\n\x0c_next_cursor\"\xdd\x01\n\rPaginationRes\x12\x17\n\ntotal_page\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x19\n\x0c\x63urrent_page\x18\x02 \x01(\x05H\x01\x88\x01\x01\x12\x16\n\tpage_size\x18\x03 \x01(\x05H\x02\x88\x01\x01\x12\x18\n\x0bprev_cursor\x18\x04 \x01(\tH\x03\x88\x01\x01\x12\x18\n\x0bnext_cursor\x18\x05 \x01(\tH\x04\x88\x01\x01\x42\r\n\x0b_total_pageB\x0f\n\r_current_pageB\x0c\n\n_page_sizeB\x0e\n\x0c_prev_cursorB\x0e\n\x0c_next_cursor\"\x07\n\x05\x45mpty\"$\n\nGetSiteRes\x12\x16\n\x04site\x18\x01 \x01(\x0b\x32\x08.pb.Site\"P\n\x04Site\x12\n\n\x02id\x18\x04 \x01(\t\x12\x0c\n\x04icon\x18\x05 \x01(\t\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x0b\n\x03url\x18\x03 \x01(\t\"N\n\x0cGetBoardsReq\x12\x0f\n\x07site_id\x18\x01 \x01(\t\x12$\n\x04page\x18\x02 \x01(\x0b\x32\x11.pb.PaginationReqH\x00\x88\x01\x01\x42\x07\n\x05_page\"J\n\x0cGetBoardsRes\x12\x19\n\x06\x62oards\x18\x01 \x03(\x0b\x32\t.pb.Board\x12\x1f\n\x04page\x18\x02 \x01(\x0b\x32\x11.pb.PaginationRes\"\x8d\x01\n\x05\x42oard\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07site_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0c\n\x04icon\x18\x04 \x01(\t\x12\x1b\n\x13large_welcome_image\x18\x05 \x01(\t\x12\x0b\n\x03url\x18\x06 \x01(\t\x12!\n\x19supported_threads_sorting\x18\x07 \x03(\t\"\xab\x01\n\x11GetThreadInfosReq\x12\x0f\n\x07site_id\x18\x01 \x01(\t\x12\x10\n\x08\x62oard_id\x18\x02 \x01(\t\x12$\n\x04page\x18\x03 \x01(\x0b\x32\x11.pb.PaginationReqH\x00\x88\x01\x01\x12\x14\n\x07sort_by\x18\x04 \x01(\tH\x01\x88\x01\x01\x12\x15\n\x08keywords\x18\x05 \x01(\tH\x02\x88\x01\x01\x42\x07\n\x05_pageB\n\n\x08_sort_byB\x0b\n\t_keywords\"Z\n\x11GetThreadInfosRes\x12$\n\x0cthread_infos\x18\x01 \x03(\x0b\x32\x0e.pb.ThreadInfo\x12\x1f\n\x04page\x18\x02 \x01(\x0b\x32\x11.pb.PaginationRes\"\xef\x01\n\nThreadInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08\x62oard_id\x18\x04 \x01(\t\x12\x0f\n\x07site_id\x18\x05 \x01(\t\x12\x0b\n\x03url\x18\x0b \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x61uthor_name\x18\x03 \x01(\t\x12\x12\n\ncreated_at\x18\x06 \x01(\x03\x12(\n latest_regarding_post_created_at\x18\x07 \x01(\x03\x12\x1c\n\x14regarding_post_count\x18\x08 \x01(\x05\x12\x17\n\x0fpreview_content\x18\t \x01(\t\x12\x0c\n\x04tags\x18\n \x03(\t\"=\n\x0cGetThreadReq\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07site_id\x18\x02 \x01(\t\x12\x10\n\x08\x62oard_id\x18\x03 \x01(\t\"*\n\x0cGetThreadRes\x12\x1a\n\x06thread\x18\x01 \x01(\x0b\x32\n.pb.Thread\"\xbb\x01\n\x06Thread\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07site_id\x18\x02 \x01(\t\x12\x10\n\x08\x62oard_id\x18\x03 \x01(\t\x12\x0b\n\x03url\x18\x08 \x01(\t\x12(\n latest_regarding_post_created_at\x18\x04 \x01(\x03\x12\x1c\n\x14regarding_post_count\x18\x05 \x01(\x05\x12\x0c\n\x04tags\x18\x06 \x03(\t\x12\x1f\n\roriginal_post\x18\x07 \x01(\x0b\x32\x08.pb.Post\"\x95\x01\n\x14GetRegardingPostsReq\x12\x0f\n\x07site_id\x18\x01 \x01(\t\x12\x10\n\x08\x62oard_id\x18\x02 \x01(\t\x12\x11\n\tthread_id\x18\x03 \x01(\t\x12\x18\n\x10original_post_id\x18\x05 \x01(\t\x12$\n\x04page\x18\x04 \x01(\x0b\x32\x11.pb.PaginationReqH\x00\x88\x01\x01\x42\x07\n\x05_page\"Z\n\x14GetRegardingPostsRes\x12!\n\x0fregarding_posts\x18\x01 \x03(\x0b\x32\x08.pb.Post\x12\x1f\n\x04page\x18\x02 \x01(\x0b\x32\x11.pb.PaginationRes\"N\n\nGetPostReq\x12\x0f\n\x07site_id\x18\x01 \x01(\t\x12\x10\n\x08\x62oard_id\x18\x02 \x01(\t\x12\x11\n\tthread_id\x18\x03 \x01(\t\x12\n\n\x02id\x18\x04 \x01(\t\"$\n\nGetPostRes\x12\x16\n\x04post\x18\x01 \x01(\x0b\x32\x08.pb.Post\"\x96\x02\n\tParagraph\x12\x1f\n\x04type\x18\x01 \x01(\x0e\x32\x11.pb.ParagraphType\x12#\n\x05image\x18\x02 \x01(\x0b\x32\x12.pb.ImageParagraphH\x00\x12#\n\x05video\x18\x03 \x01(\x0b\x32\x12.pb.VideoParagraphH\x00\x12!\n\x04text\x18\x04 \x01(\x0b\x32\x11.pb.TextParagraphH\x00\x12#\n\x05quote\x18\x05 \x01(\x0b\x32\x12.pb.QuoteParagraphH\x00\x12(\n\x08reply_to\x18\x06 \x01(\x0b\x32\x14.pb.ReplyToParagraphH\x00\x12!\n\x04link\x18\x07 \x01(\x0b\x32\x11.pb.LinkParagraphH\x00\x42\t\n\x07\x63ontent\";\n\x0eImageParagraph\x12\x12\n\x05thumb\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x0b\n\x03raw\x18\x02 \x01(\tB\x08\n\x06_thumb\";\n\x0eVideoParagraph\x12\x12\n\x05thumb\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x0b\n\x03url\x18\x02 \x01(\tB\x08\n\x06_thumb\" \n\rTextParagraph\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\"!\n\x0eQuoteParagraph\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\"\x1e\n\x10ReplyToParagraph\x12\n\n\x02id\x18\x01 \x01(\t\" \n\rLinkParagraph\x12\x0f\n\x07\x63ontent\x18\x01 \x01(\t\"\xa5\x02\n\x04Post\x12\n\n\x02id\x18\x01 \x01(\t\x12\x1b\n\x0eorigin_post_id\x18\n \x01(\tH\x00\x88\x01\x01\x12\x11\n\tthread_id\x18\x02 \x01(\t\x12\x10\n\x08\x62oard_id\x18\x03 \x01(\t\x12\x0f\n\x07site_id\x18\x04 \x01(\t\x12\x10\n\x08\x61uthorId\x18\x0b \x01(\t\x12\x13\n\x0b\x61uthor_name\x18\x05 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x06 \x01(\t\x12\x12\n\ncreated_at\x18\x07 \x01(\x03\x12\r\n\x05title\x18\t \x01(\t\x12\x0c\n\x04like\x18\x0c \x01(\x05\x12\x0f\n\x07\x64islike\x18\r \x01(\x05\x12\x10\n\x08\x63omments\x18\x0e \x01(\x05\x12\x1f\n\x08\x63ontents\x18\x0f \x03(\x0b\x32\r.pb.ParagraphB\x11\n\x0f_origin_post_id\"\x86\x01\n\x0eGetCommentsReq\x12\x0f\n\x07site_id\x18\x01 \x01(\t\x12\x10\n\x08\x62oard_id\x18\x02 \x01(\t\x12\x11\n\tthread_id\x18\x03 \x01(\t\x12\x0f\n\x07post_id\x18\x04 \x01(\t\x12$\n\x04page\x18\x05 \x01(\x0b\x32\x11.pb.PaginationReqH\x00\x88\x01\x01\x42\x07\n\x05_page\"P\n\x0eGetCommentsRes\x12\x1d\n\x08\x63omments\x18\x01 \x03(\x0b\x32\x0b.pb.Comment\x12\x1f\n\x04page\x18\x02 \x01(\x0b\x32\x11.pb.PaginationRes\"\xb9\x01\n\x07\x43omment\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07post_id\x18\x02 \x01(\t\x12\x11\n\tthread_id\x18\x03 \x01(\t\x12\x10\n\x08\x62oard_id\x18\x04 \x01(\t\x12\x0f\n\x07site_id\x18\x05 \x01(\t\x12\x11\n\tauthor_id\x18\x06 \x01(\t\x12\x13\n\x0b\x61uthor_name\x18\n \x01(\t\x12\x1f\n\x08\x63ontents\x18\x0b \x03(\x0b\x32\r.pb.Paragraph\x12\x12\n\ncreated_at\x18\x08 \x01(\x03*\xcc\x01\n\rParagraphType\x12\x1e\n\x1aPARAGRAPH_TYPE_UNSPECIFIED\x10\x00\x12\x18\n\x14PARAGRAPH_TYPE_QUOTE\x10\x01\x12\x1b\n\x17PARAGRAPH_TYPE_REPLY_TO\x10\x02\x12\x17\n\x13PARAGRAPH_TYPE_TEXT\x10\x03\x12\x18\n\x14PARAGRAPH_TYPE_IMAGE\x10\x04\x12\x17\n\x13PARAGRAPH_TYPE_LINK\x10\x05\x12\x18\n\x14PARAGRAPH_TYPE_VIDEO\x10\x06\x32\x8f\x03\n\x0c\x45xtensionApi\x12&\n\x07GetSite\x12\t.pb.Empty\x1a\x0e.pb.GetSiteRes\"\x00\x12\x31\n\tGetBoards\x12\x10.pb.GetBoardsReq\x1a\x10.pb.GetBoardsRes\"\x00\x12@\n\x0eGetThreadInfos\x12\x15.pb.GetThreadInfosReq\x1a\x15.pb.GetThreadInfosRes\"\x00\x12\x31\n\tGetThread\x12\x10.pb.GetThreadReq\x1a\x10.pb.GetThreadRes\"\x00\x12I\n\x11GetRegardingPosts\x12\x18.pb.GetRegardingPostsReq\x1a\x18.pb.GetRegardingPostsRes\"\x00\x12+\n\x07GetPost\x12\x0e.pb.GetPostReq\x1a\x0e.pb.GetPostRes\"\x00\x12\x37\n\x0bGetComments\x12\x12.pb.GetCommentsReq\x1a\x12.pb.GetCommentsRes\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'extension_api_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PARAGRAPHTYPE']._serialized_start=3287
  _globals['_PARAGRAPHTYPE']._serialized_end=3491
  _globals['_PAGINATIONREQ']._serialized_start=28
  _globals['_PAGINATIONREQ']._serialized_end=223
  _globals['_PAGINATIONRES']._serialized_start=226
  _globals['_PAGINATIONRES']._serialized_end=447
  _globals['_EMPTY']._serialized_start=449
  _globals['_EMPTY']._serialized_end=456
  _globals['_GETSITERES']._serialized_start=458
  _globals['_GETSITERES']._serialized_end=494
  _globals['_SITE']._serialized_start=496
  _globals['_SITE']._serialized_end=576
  _globals['_GETBOARDSREQ']._serialized_start=578
  _globals['_GETBOARDSREQ']._serialized_end=656
  _globals['_GETBOARDSRES']._serialized_start=658
  _globals['_GETBOARDSRES']._serialized_end=732
  _globals['_BOARD']._serialized_start=735
  _globals['_BOARD']._serialized_end=876
  _globals['_GETTHREADINFOSREQ']._serialized_start=879
  _globals['_GETTHREADINFOSREQ']._serialized_end=1050
  _globals['_GETTHREADINFOSRES']._serialized_start=1052
  _globals['_GETTHREADINFOSRES']._serialized_end=1142
  _globals['_THREADINFO']._serialized_start=1145
  _globals['_THREADINFO']._serialized_end=1384
  _globals['_GETTHREADREQ']._serialized_start=1386
  _globals['_GETTHREADREQ']._serialized_end=1447
  _globals['_GETTHREADRES']._serialized_start=1449
  _globals['_GETTHREADRES']._serialized_end=1491
  _globals['_THREAD']._serialized_start=1494
  _globals['_THREAD']._serialized_end=1681
  _globals['_GETREGARDINGPOSTSREQ']._serialized_start=1684
  _globals['_GETREGARDINGPOSTSREQ']._serialized_end=1833
  _globals['_GETREGARDINGPOSTSRES']._serialized_start=1835
  _globals['_GETREGARDINGPOSTSRES']._serialized_end=1925
  _globals['_GETPOSTREQ']._serialized_start=1927
  _globals['_GETPOSTREQ']._serialized_end=2005
  _globals['_GETPOSTRES']._serialized_start=2007
  _globals['_GETPOSTRES']._serialized_end=2043
  _globals['_PARAGRAPH']._serialized_start=2046
  _globals['_PARAGRAPH']._serialized_end=2324
  _globals['_IMAGEPARAGRAPH']._serialized_start=2326
  _globals['_IMAGEPARAGRAPH']._serialized_end=2385
  _globals['_VIDEOPARAGRAPH']._serialized_start=2387
  _globals['_VIDEOPARAGRAPH']._serialized_end=2446
  _globals['_TEXTPARAGRAPH']._serialized_start=2448
  _globals['_TEXTPARAGRAPH']._serialized_end=2480
  _globals['_QUOTEPARAGRAPH']._serialized_start=2482
  _globals['_QUOTEPARAGRAPH']._serialized_end=2515
  _globals['_REPLYTOPARAGRAPH']._serialized_start=2517
  _globals['_REPLYTOPARAGRAPH']._serialized_end=2547
  _globals['_LINKPARAGRAPH']._serialized_start=2549
  _globals['_LINKPARAGRAPH']._serialized_end=2581
  _globals['_POST']._serialized_start=2584
  _globals['_POST']._serialized_end=2877
  _globals['_GETCOMMENTSREQ']._serialized_start=2880
  _globals['_GETCOMMENTSREQ']._serialized_end=3014
  _globals['_GETCOMMENTSRES']._serialized_start=3016
  _globals['_GETCOMMENTSRES']._serialized_end=3096
  _globals['_COMMENT']._serialized_start=3099
  _globals['_COMMENT']._serialized_end=3284
  _globals['_EXTENSIONAPI']._serialized_start=3494
  _globals['_EXTENSIONAPI']._serialized_end=3893
# @@protoc_insertion_point(module_scope)
