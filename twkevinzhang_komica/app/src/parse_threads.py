import logging
from collections.abc import Callable
from datetime import datetime

from lxml import html
from lxml.etree import _Element

import extension_api_pb2 as pb2
import paragraph
import domain
from domain import OverPageError
from nullable import is_zero_str, is_zero_list
from utilities import is_youtube, is_image, is_video

def check_page_error(tree: _Element):
    error_elements = tree.xpath('//div[@id="error"]//span/text()')
    if not error_elements:
        return

    error_message = error_elements[0].strip()
    if error_message == "對不起，您所要求的頁數並不存在":
        raise OverPageError


def parse_thread_infos_html(html_content: str, site_id: str, board_id: str) -> (list[domain.Post], int, int):
    """
    :param html_content:
    :param site_id:
    :param board_id:
    :return: items, current_page, total_page
    """
    tree = html.document_fromstring(html_content, parser=html.HTMLParser(encoding='utf-8'))
    check_page_error(tree)
    thread_infos = []

    for thread_div in tree.xpath('//div[@class="thread"]'):
        # print(html.tostring(thread_div, encoding="unicode", pretty_print=True))
        thread_info = _parse_thread(thread_div)
        thread_info.site_id = site_id
        thread_info.board_id = board_id
        thread_info.thread_id = thread_info.id
        prefix = domain.board_id_to_url_prefix(board_id)
        thread_info.url = f"{prefix}/pixmicat.php?res={thread_info.id}"
        thread_infos.append(thread_info)

    # 找出當前頁數（bold <b> 標籤內的數字）
    current_page = int(tree.xpath('//div[@id="page_switch"]//b/text()')[0])

    # 找出所有 <a> 標籤內的數字，過濾掉 "..." 的 <a>，最後一個就是 total_page
    page_numbers = [int(a.text) for a in tree.xpath('//div[@id="page_switch"]//a') if a.text.isdigit()]
    total_page = max(page_numbers) if page_numbers else None
    return thread_infos, current_page, total_page


def parse_thread_html(html_content: str, site_id: str, board_id: str, thread_id: str, post_id: str | None) -> domain.Post:
    tree = html.document_fromstring(html_content, parser=html.HTMLParser(encoding='utf-8'))
    if is_zero_str(post_id) or post_id == thread_id:
        thread = _parse_thread(tree)
        thread.site_id = site_id
        thread.board_id = board_id
        thread.thread_id = thread_id
        prefix = domain.board_id_to_url_prefix(board_id)
        thread.url = f"{prefix}/pixmicat.php?res={thread_id}"
        return thread
    else:
        all_posts = parse_regarding_posts_html(html_content, site_id, board_id, thread_id, None)
        return next(iter([x for x in all_posts if x.id == post_id]), None)


def parse_regarding_posts_html(html_content: str, site_id: str, board_id: str, thread_id: str, reply_to_id: str | None) -> list[domain.Post]:
    tree = html.document_fromstring(html_content, parser=html.HTMLParser(encoding='utf-8'))

    # 計算回覆數
    regarding_posts_count_map: dict[str, int] = {}
    latest_regarding_post_created_at_map: dict[str, int] = {}
    for post_div in tree.xpath('//div[@class="post reply"]'):
        post = _parse_post(post_div, lambda x: "")
        for c in post.contents:
            if c.type == pb2.PARAGRAPH_TYPE_REPLY_TO:
                no = c.reply_to.id
                regarding_posts_count_map[no] = regarding_posts_count_map.get(no, 0) + 1
                latest_regarding_post_created_at_map[no] = max(latest_regarding_post_created_at_map.get(no, 0), post.created_at)

    # 解析所有回覆
    regarding_posts = []
    def get_preview(no: str):
        contents: list[pb2.Paragraph] = next(iter([x.contents for x in regarding_posts if x.id == no]), None)
        if is_zero_list(contents):
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
        post.site_id = site_id
        post.board_id = board_id
        post.url = None
        post.regarding_posts_count = regarding_posts_count_map.get(post.id, 0)
        post.latest_regarding_post_created_at = latest_regarding_post_created_at_map.get(post.id, 0)
        regarding_posts.append(post)

    # 根據 reply to post id 篩選回覆
    if not is_zero_str(reply_to_id) and reply_to_id != thread_id:
        filtered_posts = []
        for post in regarding_posts:
            for c in post.contents:
                if c.type == pb2.PARAGRAPH_TYPE_REPLY_TO and c.reply_to.id == reply_to_id:
                    filtered_posts.append(post)
        return filtered_posts

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


def _parse_post(post_div: _Element, get_preview: Callable[[str], str]) -> domain.Post:
    post_id = post_div.get("data-no")

    # 解析發文時間
    datetime_element = post_div.find('.//span[@class="now"]')
    datetime_str = ''.join(datetime_element.itertext())
    datetime_arr = datetime_str.split(' ')
    created_at = _parse_datetime(datetime_arr[0], datetime_arr[1])

    # 解析作者名稱
    author_id = datetime_arr[2]
    # author_name = post_div.xpath('.//span[@class="name"]/text()')
    # author_name = author_name[0] if author_name else "無名"
    author_name = post_id

    # 解析內容
    contents = _parse_post_content(post_div, get_preview)

    return domain.Post(
        id=post_id,
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


def _parse_thread(tree) -> domain.Post:
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
        regarding_posts.append(_parse_post(post_div, lambda x: ""))

    # 取得回覆數
    post.regarding_posts_count = len(regarding_posts)

    # 取得最新回覆時間
    post.latest_regarding_post_created_at = max((post.created_at for post in regarding_posts), default=0)

    return post


def _parse_post_content(post_div: _Element, get_preview: Callable[[str], str]) -> list[pb2.Paragraph]:
    """解析貼文內容，返回 Paragraph 列表"""

    # Extract the quote content
    contents = []
    quote_div = post_div.find(".//div[@class='quote']")
    if quote_div is not None:
        # 處理 quote_div 的文本內容
        if quote_div.text and quote_div.text.strip():
            contents.append(paragraph.text(quote_div.text.strip()))

        # 使用 etree.tostring 轉換HTML為字符串，以便處理 <br> 標籤
        # 然後使用解析函數處理所有元素
        for child in quote_div:
            # 處理 <br> 標籤
            if child.tag == 'br':
                contents.append(paragraph.newLine())
                # 檢查 br 後是否有文本
                if child.tail and child.tail.strip():
                    contents.append(paragraph.text(child.tail.strip()))
            # 處理引用的回覆
            elif child.tag == "span" and child.get("class") == "resquote":
                qlink_a = child.find(".//a[@class='qlink']")
                if qlink_a is not None:
                    no = qlink_a.get("href")[2:]
                    contents.append(paragraph.reply_to(id=no, preview=get_preview(no)))
                # 檢查 span 後是否有文本
                if child.tail and child.tail.strip():
                    contents.append(paragraph.text(child.tail.strip()))
            # 處理連結
            elif child.tag == "a":
                link_url = child.get("href")
                if is_youtube(link_url):
                    contents.append(paragraph.youtube_video(link_url))
                else:
                    contents.append(paragraph.link(link_url))
                # 檢查連結後是否有文本
                if child.tail and child.tail.strip():
                    contents.append(paragraph.text(child.tail.strip()))
            # 處理其他元素
            else:
                # 獲取元素文本
                if child.text and child.text.strip():
                    contents.append(paragraph.text(child.text.strip()))
                # 處理子元素中的 <br> 標籤
                for subelem in child.iter():
                    if subelem.tag == 'br':
                        contents.append(paragraph.newLine())
                # 檢查元素後是否有文本
                if child.tail and child.tail.strip():
                    contents.append(paragraph.text(child.tail.strip()))
    else:
        # if no quote div, it might be "無本文"
        quote = post_div.find(".//div[@class='quote']")
        if quote is not None and quote.text == "無本文":
            contents.append(paragraph.text("無本文"))

    # Extract image information
    file_thumb = post_div.find(".//a[@class='file-thumb']")

    if file_thumb is not None:
        href = file_thumb.get("href")
        if is_image(href):
            image_link = href
            image_thumb = None
            thumb_element = file_thumb.find("img")
            if thumb_element is not None:
                image_thumb = thumb_element.get("src")
            if image_link and image_thumb:
                if image_link.startswith("//"):
                    image_link = "https:" + image_link
                if image_thumb.startswith("//"):
                    image_thumb = "https:" + image_thumb
                contents.insert(0, paragraph.image(s=image_link, thumb=image_thumb))
        if is_video(href):
            video_link = href
            if video_link:
                if video_link.startswith("//"):
                    video_link = "https:" + video_link
                contents.insert(0, paragraph.video(video_link))
    return contents