import json
import os
from unittest import TestCase

from google.protobuf.json_format import MessageToDict

from src import paragraph
from src.parse_threads import parse_thread_infos_html, parse_regarding_posts_html
import src.extension_api_pb2 as pb2


class TestParseThreadInfos(TestCase):
    def test_parse_thread_infos_html(self):
        with open(get_html_filename("thread_infos.fragment.html"), "r") as f:
            html = f.read()
            thread_infos = parse_thread_infos_html(html, 'mock', 'mock')
            thread_info1 = pb2.Post(
                id="26765435",
                thread_id="26765435",
                board_id="mock",
                site_id="mock",
                title="無題",
                author_id="ID:Ho37W5Jk(1/4)",
                author_name="無名",
                created_at=1740432284,  # 2025/02/25(二) 05:24:44.001 GMT+8
                latest_regarding_post_created_at=1740434260,  # 2025/02/25(二) 05:24:44.001 GMT+8
                regarding_posts=4,
                contents=[
                    paragraph.image(
                        s="https://gita.komica1.org/00b/src/1740432283914.jpg",
                        thumb="https://gita.komica1.org/00b/thumb/1740432283914s.jpg",
                    ),
                    paragraph.text("美國正式加入中俄勢力"),
                    paragraph.text("島民現在在想什麼?"),
                ],
            )
            thread_info2 = pb2.Post(
                id="26765468",
                thread_id="26765468",
                board_id="mock",
                site_id="mock",
                title="無題",
                author_id="ID:tMp8iWdc",
                author_name="無名",
                created_at=1740434415,  # 2025/02/25(二) 06:00:15.732 GMT+8
                latest_regarding_post_created_at=1740434260,  # 2025/02/25(二) 06:00:15.732 GMT+8
                regarding_posts=4,
                contents=[
                    paragraph.image(
                        s="https://gita.komica1.org/00b/src/1740434415657.jpg",
                        thumb="https://gita.komica1.org/00b/thumb/1740434415657s.jpg",
                    ),
                    paragraph.text("清晨清姬清雞雞"),
                ],
            )
            thread_info3 = pb2.Post(
                id="26765356",
                thread_id="26765356",
                board_id="mock",
                site_id="mock",
                title="無題",
                author_id="ID:lkoVmHUo",
                author_name="無名",
                created_at=1740426590,  # 2025/02/25(二) 03:49:50.664 GMT+8
                latest_regarding_post_created_at=1740434260,  # 2025/02/25(二) 03:49:50.664 GMT+8
                regarding_posts=4,
                contents=[
                    paragraph.image(
                        s="https://gita.komica1.org/00b/src/1740426590497.webm",
                        thumb="https://gita.komica1.org/00b/thumb/1740426590497s.jpg",
                    ),
                    paragraph.text("有洗貓的影片嗎"),
                ],
            )
            self.assertEqual(thread_infos[0], thread_info1)
            self.assertEqual(thread_infos[1], thread_info2)
            self.assertEqual(thread_infos[2], thread_info3)
            self.assertEqual(len(thread_infos), 3)

    def test_parse_regarding_posts_html(self):
        with open(get_html_filename("thread_detail.fragment.html"), "r") as f:
            html = f.read()
            posts = parse_regarding_posts_html(html, 'mock', 'mock', 'mock')
            post1 = pb2.Post(
                id="26812766",
                origin_post_id="mock",
                thread_id="mock",
                board_id="mock",
                site_id="mock",
                author_id="ID:r76NdmK.(2/4)",
                author_name="無名",
                contents=[
                    paragraph.image(s="https://gita.komica1.org/00b/src/1740886260520.jpg", thumb="https://gita.komica1.org/00b/thumb/1740886260520s.jpg"),
                    paragraph.text("無本文"),
                ],
                created_at=1740886260,  # 2025/03/02(日) 11:31:00.943 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
            )
            post2 = pb2.Post(
                id="26812792",
                origin_post_id="mock",
                thread_id="mock",
                board_id="mock",
                site_id="mock",
                author_id="ID:Vzxlijiw",
                author_name="無名",
                contents=[
                    paragraph.reply_to(s="26812758"),
                    paragraph.text("法蘭可愛"),
                ],
                created_at=1740886457,  # 2025/03/02(日) 11:34:17.391 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
            )
            post3 = pb2.Post(
                id="26812814",
                origin_post_id="mock",
                thread_id="mock",
                board_id="mock",
                site_id="mock",
                author_id="ID:r76NdmK.(3/4)",
                author_name="無名",
                contents=[
                    paragraph.image(s="https://gita.komica1.org/00b/src/1740886613383.jpg", thumb="https://gita.komica1.org/00b/thumb/1740886613383s.jpg"),
                    paragraph.link("https://x.com/priconne_redive/status/1896033263946444971/photo/1"),
                ],
                created_at=1740886613,  # 2025/03/02(日) 11:36:53.647 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
            )
            post4 = pb2.Post(
                id="26812830",
                origin_post_id="mock",
                thread_id="mock",
                board_id="mock",
                site_id="mock",
                author_id="ID:r76NdmK.(4/4)",
                author_name="無名",
                contents=[
                    paragraph.image(s="https://gita.komica1.org/00b/src/1740886843049.jpg", thumb="https://gita.komica1.org/00b/thumb/1740886843049s.jpg"),
                    paragraph.text("無本文"),
                ],
                created_at=1740886843,  # 2025/03/02(日) 11:40:43.161 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
                regarding_posts=1,
            )
            post5 = pb2.Post(
                id="26812836",
                origin_post_id="mock",
                thread_id="mock",
                board_id="mock",
                site_id="mock",
                author_id="ID:Tx/LDMKs",
                author_name="無名",
                contents=[
                    paragraph.reply_to(s="26812758"),
                    paragraph.text("感覺女角越穿越少..?"),
                ],
                created_at=1740886939,  # 2025/03/02(日) 11:42:19.134 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
            )
            post6 = pb2.Post(
                id="26812841",
                origin_post_id="mock",
                thread_id="mock",
                board_id="mock",
                site_id="mock",
                author_id="ID:dvKAH0Qw",
                author_name="無名",
                contents=[
                    paragraph.reply_to(s="26812830"),
                    paragraph.text("誰"),
                ],
                created_at=1740886961,  # 2025/03/02(日) 11:42:41.772 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
            )
            self.assertEqual(posts[0], post1)
            self.assertEqual(posts[1], post2)
            self.assertEqual(posts[2], post3)
            self.assertEqual(posts[3], post4)
            self.assertEqual(posts[4], post5)
            self.assertEqual(posts[5], post6)
            self.assertEqual(len(posts), 6)


def get_html_filename(filename: str):
    return os.path.join(os.path.dirname(__file__), filename)

def print_json(pb2_obj):
    d = MessageToDict(pb2_obj)
    print(json.dumps(d, indent=2, ensure_ascii=False))
