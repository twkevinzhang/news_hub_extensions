from datetime import datetime

from lxml import html
from lxml.etree import _Element

import extension_api_pb2 as pb2


def parse_thread_infos_html(html_content) -> list[pb2.ThreadInfo]:
    tree = html.fromstring(html_content)
    threads = []

    for thread_div in tree.xpath('//div[@class="thread"]'):
        thread_id = thread_div.get("data-no")
        thread_url = f"pixmicat.php?res={thread_id}"
        title = thread_div.xpath('.//span[@class="title"]/text()')
        title = title[0] if title else "無題"
        author_name = thread_div.xpath('.//span[@class="name"]/text()')
        author_name = author_name[0] if author_name else "無名"

        # 解析發文時間
        date_elements = thread_div.xpath('.//span[@class="now"]/text()')
        time_elements = thread_div.xpath('.//span[@class="qlink"]/following-sibling::span[1]/text()')
        created_at = _parse_datetime(date_elements[0] if date_elements else "2025/02/25(二)",
                                     time_elements[0] if time_elements else "00:00:00.000")

        # 解析 preview_content
        preview_content = thread_div.xpath('.//div[@class="quote"]/text()')
        preview_content = "\n".join(preview_content).strip()

        # 解析帖子
        posts = []
        for post_div in thread_div.xpath('.//div[contains(@class, "post")]'):
            post = _parse_regarding_post_html(thread_id, author_name, post_div)
            posts.append(post)

        # 取得回覆數
        regarding_post_count = len(posts)

        # 取得最新回覆時間
        latest_regarding_post_created_at = max((post.created_at for post in posts), default=created_at)

        thread = pb2.ThreadInfo(
            id=thread_id,
            board_id=None,
            site_id=None,
            url=thread_url,
            title=title,
            author_name=author_name,
            created_at=created_at,
            latest_regarding_post_created_at=latest_regarding_post_created_at,
            regarding_post_count=regarding_post_count,
            preview_content=preview_content,
        )
        threads.append(thread)
    return threads


def _parse_datetime(date_str, time_str):
    """
    解析時間格式，例如 '2025/02/25(二) 05:24:44.001' 轉換為 timestamp
    """
    try:
        dt_str = f"{date_str} {time_str}"
        dt_obj = datetime.strptime(dt_str, "%Y/%m/%d(%a) %H:%M:%S.%f")
        return int(dt_obj.timestamp())
    except Exception as e:
        return 0

def _parse_regarding_post_html(
        thread_id: str,
        author_name: str,
        post_div: _Element,
) -> pb2.Post:
    post_id = post_div.get("data-no")
    author_id = post_div.xpath('.//span[@class="id"]/@data-id')
    author_id = author_id[0] if author_id else ""

    # 解析回覆數
    replies = post_div.xpath('.//div[@class="backquote"]/a/@data-no')
    regarding_post_count = len(replies)

    # 解析內容
    content = post_div.xpath('.//div[@class="quote"]/text()')
    content = "\n".join(content).strip()

    # 解析發文時間
    date_elements = post_div.xpath('.//span[@class="now"]/text()')
    time_elements = post_div.xpath('.//span[@class="qlink"]/following-sibling::span[1]/text()')
    created_at = _parse_datetime(date_elements[0] if date_elements else "2025/02/25(二)",
                                 time_elements[0] if time_elements else "00:00:00.000")

    return pb2.Post(
        id=post_id,
        origin_post_id=None,
        thread_id=thread_id,
        board_id=None,
        site_id=None,
        authorId=author_id,
        author_name=author_name,
        content=content,
        created_at=created_at,
        title=None,
        like=0,
        dislike=0,
        comments=regarding_post_count,
        # contents=content
    )
