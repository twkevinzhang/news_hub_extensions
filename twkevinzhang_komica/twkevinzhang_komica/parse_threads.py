from collections.abc import Callable
from datetime import datetime

from bs4 import BeautifulSoup, Tag
from . import extension_api_pb2 as pb2
from . import paragraph
from . import domain
from .domain import OverPageError
from .paragraph import youtube_video, image
from .utilities import is_youtube, is_image, is_video, is_zero


def to_soup(html_content) -> BeautifulSoup:
    """使用 BeautifulSoup 解析 HTML 內容"""
    soup = BeautifulSoup(html_content, 'lxml')
    return soup


def check_page_error(soup):
    """檢查頁面是否存在錯誤"""
    error_div = soup.select_one('div#error')
    if not error_div:
        return

    error_span = error_div.select_one('span')
    if error_span and error_span.get_text().strip() == "對不起，您所要求的頁數並不存在":
        raise OverPageError


def parse_threads_html(html_content: str, board_id: str) -> (list[domain.Post], int, int):
    """
    解析討論串資訊 HTML
    :param html_content: HTML 內容
    :param board_id: 看板 ID
    :return: 討論串資訊列表, 當前頁碼, 總頁數
    """
    soup = to_soup(html_content)
    check_page_error(soup)
    threads = []

    for thread_div in soup.find_all('div', class_='thread'):
        thread = _parse_thread(thread_div)
        thread.board_id = board_id
        thread.thread_id = thread.id
        prefix = domain.board_id_to_url_prefix(board_id)
        thread.url = f"{prefix}/pixmicat.php?res={thread.id}"
        threads.append(thread)

    # 找出當前頁碼（粗體 <b> 標籤內的數字）
    page_switch = soup.select_one('div#page_switch')
    current_page = 1
    if page_switch and page_switch.select_one('b'):
        current_page = int(page_switch.select_one('b').get_text())

    # 找出所有 <a> 標籤內的數字，過濾掉 "..." 的 <a>，最大的就是總頁數
    page_numbers = []
    if page_switch:
        for a in page_switch.find_all('a'):
            if a.get_text().isdigit():
                page_numbers.append(int(a.get_text()))

    total_page = max(page_numbers) if page_numbers else 1
    return threads, current_page, total_page


def parse_original_post_html(html_content: str, board_id: str, thread_id: str,
                        post_id: str | None) -> domain.Post:
    """
    解析討論串 OP 貼文 HTML
    :param html_content: HTML 內容
    :param board_id: 看板 ID
    :param thread_id: 討論串 ID
    :param post_id: 貼文 ID
    :return: 貼文物件
    """
    soup = to_soup(html_content)

    if is_zero(post_id) or post_id == thread_id:
        thread = _parse_thread(soup)
        thread.board_id = board_id
        thread.thread_id = thread_id
        prefix = domain.board_id_to_url_prefix(board_id)
        thread.url = f"{prefix}/pixmicat.php?res={thread_id}"
        return thread
    else:
        all_posts = parse_replies_html(html_content, board_id, thread_id, None)
        return next(iter([x for x in all_posts if x.id == post_id]), None)


def parse_replies_html(html_content: str, board_id: str, thread_id: str,
                        reply_to_id: str | None) -> list[domain.Post]:
    """
    解析相關回覆貼文 HTML
    :param html_content: HTML 內容
    :param board_id: 看板 ID
    :param thread_id: 討論串 ID
    :param reply_to_id: 回覆目標 ID
    :return: 回覆貼文表
    """
    soup = to_soup(html_content)

    # 計算回覆數
    replies_count_map: dict[str, int] = {}
    latest_reply_created_at_map: dict[str, int] = {}

    for post_div in soup.find_all('div', class_='post reply'):
        post = _parse_post(post_div, lambda x: "")
        for c in post.contents:
            if c.type == pb2.PARAGRAPH_TYPE_REPLY_TO:
                no = c.reply_to.id
                replies_count_map[no] = replies_count_map.get(no, 0) + 1
                latest_reply_created_at_map[no] = max(latest_reply_created_at_map.get(no, 0),
                                                               post.created_at)

    # 解析所有回覆
    replies = []

    def get_preview(no: str):
        contents: list[pb2.Paragraph] = next(iter([x.contents for x in replies if x.id == no]), None)
        if is_zero(contents):
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

    for post_div in soup.find_all('div', class_='post reply'):
        post = _parse_post(post_div, get_preview)
        post.thread_id = thread_id
        post.board_id = board_id
        post.url = None
        post.replies_count = replies_count_map.get(post.id, 0)
        post.latest_reply_created_at = latest_reply_created_at_map.get(post.id, 0)
        replies.append(post)

    # 根據 reply to post id 篩選回覆
    if not is_zero(reply_to_id) and reply_to_id != thread_id:
        filtered_posts = []
        for post in replies:
            for c in post.contents:
                if c.type == pb2.PARAGRAPH_TYPE_REPLY_TO and c.reply_to.id == reply_to_id:
                    filtered_posts.append(post)
        return filtered_posts

    return replies


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


def _parse_post(post_div: Tag, get_preview: Callable[[str], str]) -> domain.Post:
    """
    使用 BeautifulSoup 解析貼文
    :param post_div: 貼文 div
    :param get_preview: 獲取預覽函數
    :return: 貼文物件
    """
    post_id = post_div.get("data-no")

    # 解析發文時間
    datetime_element = post_div.select_one('span.now')
    datetime_str = datetime_element.get_text() if datetime_element else ""
    datetime_arr = datetime_str.split(' ')
    created_at = _parse_datetime(datetime_arr[0], datetime_arr[1]) if len(datetime_arr) >= 2 else 0

    # 解析作者名稱
    author_id = datetime_arr[2] if len(datetime_arr) >= 3 else ""
    author_name = post_id

    # 解析內容
    contents = _parse_post_content(post_div, get_preview)

    # 解析第一張圖片
    first_image = next((content.image for content in contents if content.type == pb2.ParagraphType.PARAGRAPH_TYPE_IMAGE), None)
    if not first_image:
        if youtube_video_link := next((content.video for content in contents if content.type == pb2.ParagraphType.PARAGRAPH_TYPE_VIDEO and is_youtube(content.video.url)), None):
            clip = youtube_video_link.url.split('?v=')[-1]
            link = f"https://img.youtube.com/vi/{clip}/0.jpg"
            first_image = image(s=link, thumb=link).image

    return domain.Post(
        id=post_id,
        thread_id=None,
        board_id=None,
        author_id=author_id,
        author_name=author_name,
        created_at=created_at,
        title="無題",
        liked=0,
        disliked=0,
        comments=0,
        image=first_image,
        contents=contents,
        tags=[],
        latest_reply_created_at=0,
        replies_count=0,
        url=None,
    )


def _parse_thread(container) -> domain.Post:
    """
    使用 BeautifulSoup 解析討論串
    :param container: 容器（可以是 BeautifulSoup 物件或討論串 div）
    :return: 討論串貼文物件
    """
    threadpost_div = container.select_one('div.post.threadpost')
    if not threadpost_div:
        # 如果 container 已經是討論串 div
        if container.name == 'div' and 'thread' in container.get('class', []):
            threadpost_div = container.select_one('div.post.threadpost')

    if not threadpost_div:
        raise ValueError("找不到討論串貼文 div")

    thread_id = threadpost_div.get("data-no")

    post = _parse_post(threadpost_div, lambda x: "")

    # 解析標題
    title_span = threadpost_div.select_one('span.title')
    title = title_span.get_text() if title_span else "無題"
    post.title = title

    # 解析貼文
    replies = []
    for post_div in container.select('div.post.reply'):
        replies.append(_parse_post(post_div, lambda x: ""))

    # 獲取回覆數
    post.replies_count = len(replies)

    # 獲取最新回覆時間
    post.latest_reply_created_at = max((p.created_at for p in replies), default=0)

    return post


def _parse_post_content(post_div: Tag, get_preview: Callable[[str], str]) -> list[pb2.Paragraph]:
    """
    使用 BeautifulSoup 解析貼文內容
    :param post_div: 貼文 div
    :param get_preview: 獲取預覽函數
    :return: 段落列表
    """
    contents = []

    # 提取引用內容
    quote_div = post_div.select_one('div.quote')
    if quote_div:
        # 逐元素解析
        for child in quote_div.children:
            # 處理字串
            if isinstance(child, str) and child.strip():
                contents.append(paragraph.text(child.strip()))
            # 處理標籤
            elif isinstance(child, Tag):
                # 處理換行
                if child.name == 'br':
                    contents.append(paragraph.new_line())
                # 處理引用回覆
                elif child.name == 'span' and child.get('class') and 'resquote' in child.get('class'):
                    qlink_a = child.select_one('a.qlink')
                    if qlink_a and qlink_a.get('href'):
                        no = qlink_a.get('href')[2:]  # 去掉 '>>''
                        contents.append(paragraph.reply_to(id=no, preview=get_preview(no)))
                # 處理連結
                elif child.name == 'a':
                    link_url = child.get('href')
                    if is_youtube(link_url):
                        contents.append(paragraph.youtube_video(link_url))
                    else:
                        contents.append(paragraph.link(link_url))
                    # 處理後續文本
                    if child.next_sibling and isinstance(child.next_sibling, str) and child.next_sibling.strip():
                        contents.append(paragraph.text(child.next_sibling.strip()))
    else:
        # 無 quote_div 情況
        contents.append(paragraph.text("None"))

    # 提取圖片資訊
    file_thumb = post_div.select_one('a.file-thumb')
    if file_thumb:
        href = file_thumb.get('href')
        if is_image(href):
            image_link = href
            image_thumb = None
            thumb_element = file_thumb.select_one('img')
            if thumb_element:
                image_thumb = thumb_element.get('src')
            if image_link and image_thumb:
                if image_link.startswith('//'):
                    image_link = "https:" + image_link
                if image_thumb.startswith('//'):
                    image_thumb = "https:" + image_thumb
                contents.insert(0, paragraph.image(s=image_link, thumb=image_thumb))
        if is_video(href):
            video_link = href
            if video_link:
                if video_link.startswith('//'):
                    video_link = "https:" + video_link
                contents.insert(0, paragraph.video(video_link))
    return contents
