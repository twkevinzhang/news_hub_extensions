from collections.abc import Callable
from datetime import datetime

from lxml import html
from lxml.etree import _Element

import extension_api_pb2 as pb2
import paragraph


def parse_thread_infos_html(html_content, site_id: str, board: pb2.Board) -> list[pb2.Post]:
    tree = html.fromstring(html_content)
    thread_infos = []

    for thread_div in tree.xpath('//div[@class="thread"]'):
        # print(html.tostring(thread_div, encoding="unicode", pretty_print=True))
        thread_info = _parse_thread(thread_div)
        thread_info.site_id = site_id
        thread_info.board_id = board.id
        thread_info.thread_id = thread_info.id
        prefix = board.url.removesuffix("/index.htm")
        thread_info.url = f'{prefix}/pixmicat.php?res={thread_info.id}'
        thread_infos.append(thread_info)
    return thread_infos


def parse_thread_html(html_content, site_id: str, board: pb2.Board) -> pb2.Post:
    tree = html.fromstring(html_content)
    thread = _parse_thread(tree)
    thread.site_id = site_id
    thread.board_id = board.id
    thread.thread_id = thread.id
    prefix = board.url.removesuffix("/index.htm")
    thread.url = f'{prefix}/pixmicat.php?res={thread.id}'
    return thread


def parse_regarding_posts_html(html_content, site_id: str, board_id: str, thread_id: str) -> list[pb2.Post]:
    tree = html.fromstring(html_content)

    # 計算每個回覆的回覆數
    regarding_posts_count_map: dict[str, int] = {}
    latest_regarding_post_created_at_map: dict[str, int] = {}
    for post_div in tree.xpath('//div[@class="post reply"]'):
        post = _parse_post(post_div, lambda x: "")
        for c in post.contents:
            if c.type == pb2.PARAGRAPH_TYPE_REPLY_TO:
                no = c.reply_to.id
                regarding_posts_count_map[no] = regarding_posts_count_map.get(no, 0) + 1
                latest_regarding_post_created_at_map[no] = max(latest_regarding_post_created_at_map.get(no, 0), post.created_at)

    regarding_posts = []
    def get_preview(no: str):
        contents: list[pb2.Paragraph] = next(iter([x.contents for x in regarding_posts if x.id == no]), None)
        if contents is None:
            return ""
        preview = ""
        for c in contents:
            if c.type == pb2.ParagraphType.PARAGRAPH_TYPE_TEXT:
                preview += c.text.content
            if c.type == pb2.ParagraphType.PARAGRAPH_TYPE_IMAGE:
                preview += "[圖片]"
            if c.type == pb2.ParagraphType.PARAGRAPH_TYPE_LINK:
                preview += "[連結]"
            if c.type == pb2.ParagraphType.PARAGRAPH_TYPE_VIDEO:
                preview += f"[影片]"
        return preview
    for post_div in tree.xpath('//div[@class="post reply"]'):
        post = _parse_post(post_div, get_preview)
        post.thread_id = thread_id
        if post.id != thread_id:
            post.origin_post_id = thread_id
        post.site_id = site_id
        post.board_id = board_id
        post.regarding_posts_count = regarding_posts_count_map.get(post.id, 0)
        post.latest_regarding_post_created_at = latest_regarding_post_created_at_map.get(post.id, 0)
        regarding_posts.append(post)
    return regarding_posts


def _parse_datetime(date_str, time_str):
    """
    解析時間格式，例如 '2025/02/25(二) 05:24:44.001' 轉換為 timestamp
    """
    date_str = (date_str
                .replace('日', 'Sun')
                .replace('一', 'Mon')
                .replace('二', 'Tue')
                .replace('三', 'Wed')
                .replace('四', 'Thu')
                .replace('五', 'Fri')
                .replace('六', 'Sat')
                )
    try:
        dt_str = f"{date_str} {time_str}"
        dt_obj = datetime.strptime(dt_str, "%Y/%m/%d(%a) %H:%M:%S.%f")
        return int(dt_obj.timestamp())
    except ValueError:
        return 0


def _parse_post(post_div: _Element, get_preview: Callable[[str], str]) -> pb2.Post:
    post_id = post_div.get("data-no")

    # 解析發文時間
    datetime_element = post_div.find('.//span[@class="now"]')
    datetime_str = ''.join(datetime_element.itertext())
    datetime_arr = datetime_str.split(' ')
    created_at = _parse_datetime(datetime_arr[0], datetime_arr[1])

    # 解析作者名稱
    author_id = datetime_arr[2]
    author_name = post_div.xpath('.//span[@class="name"]/text()')
    author_name = author_name[0] if author_name else "無名"

    # 解析內容
    contents = _parse_post_content(post_div, get_preview)

    return pb2.Post(
        id=post_id,
        origin_post_id=None,
        thread_id=None,
        board_id=None,
        site_id=None,
        author_id=author_id,
        author_name=author_name,
        created_at=created_at,
        title="無題",
        liked=0,
        disliked=0,
        comments=0,
        contents=contents,
        tags=[],
        latest_regarding_post_created_at = 0,
        regarding_posts_count=0,
        url=None,
    )


def _parse_thread(tree) -> pb2.Post:
    threadpost_div = tree.xpath('.//div[@class="post threadpost"]')[0]
    thread_id = threadpost_div.get("data-no")

    post = _parse_post(threadpost_div, lambda x: "")

    # 解析 title
    title = threadpost_div.xpath('.//span[@class="title"]/text()')
    title = title[0] if title else "無題"
    post.title = title

    # 解析帖子
    regarding_posts = []
    for post_div in tree.xpath('.//div[@class="post reply"]'):
        regarding_post = _parse_post(post_div, lambda x: "")
        if regarding_post.id != thread_id:
            regarding_post.origin_post_id = thread_id
        regarding_posts.append(regarding_post)

    # 取得回覆數
    post.regarding_posts_count = len(regarding_posts)

    # 取得最新回覆時間
    post.latest_regarding_post_created_at = max((post.created_at for post in regarding_posts), default=post.created_at)

    return post

def _parse_post_content(post_div: _Element, get_preview: Callable[[str], str]) -> list[pb2.Paragraph]:
    """解析貼文內容，返回 Paragraph 列表"""

    # Extract the quote content
    contents = []
    quote_div = post_div.find(".//div[@class='quote']")
    if quote_div is not None:
        for element in quote_div.iterchildren():
             if element.tag == "span" and element.get("class") == "resquote":
                 qlink_a = element.find(".//a[@class='qlink']")
                 if qlink_a is not None:
                     no = qlink_a.get("href")[2:]
                     contents.append(paragraph.reply_to(s=no, preview=get_preview(no)))
             elif element.tag == "a":
                 link_url = element.get("href")
                 contents.append(paragraph.link(link_url))

             else:
                 text = element.tail
                 if text and text.strip():
                     contents.append(paragraph.text(text.strip()))

        if quote_div.text and quote_div.text.strip():
            contents.insert(0, paragraph.text(quote_div.text.strip()))
    else:
        # if no quote div, it might be "無本文"
        quote = post_div.find(".//div[@class='quote']")
        if quote is not None and quote.text == "無本文":
            contents.append(paragraph.text("無本文"))

    # Extract image information
    file_text_div = post_div.find(".//div[@class='file-text']")
    image_link = None
    image_thumb = None
    if file_text_div is not None:
        image_link_element = file_text_div.find(".//a")
        if image_link_element is not None:
            image_link = image_link_element.get("href")
            image_thumb_element = post_div.find(".//a[@class='file-thumb']/img")
            if image_thumb_element is not None:
                 image_thumb = image_thumb_element.get("src")

            if image_link and image_thumb:
                if image_link.startswith("//"):
                    image_link = "https:" + image_link
                if image_thumb.startswith("//"):
                    image_thumb = "https:" + image_thumb
                contents.insert(0, paragraph.image(s=image_link, thumb=image_thumb))

    return contents
