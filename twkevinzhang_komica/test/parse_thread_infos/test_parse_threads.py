import json
import os
from unittest import TestCase

from google.protobuf.json_format import MessageToDict

from twkevinzhang_komica import paragraph
from twkevinzhang_komica.parse_threads import parse_threads_html, parse_replies_html, parse_original_post_html
import twkevinzhang_komica.domain as domain


class TestParseThreadInfos(TestCase):
    def test_parse_thread_infos_html(self):
        with open(get_html_filename("thread_infos.fragment.html"), "r") as f:
            html = f.read()
            thread_infos, current_page, total_page = parse_threads_html(html, 'gaia/1')
            thread_info1 = domain.Post(
                id="26765435",
                thread_id="26765435",
                board_id="gaia/1",
                title="無題",
                author_id="ID:Ho37W5Jk(1/4)",
                author_name="26765435",
                created_at=1740432284,  # 2025/02/25(二) 05:24:44.001 GMT+8
                liked=0,
                disliked=0,
                comments=0,
                image=paragraph.image(
                        s="https://gita.komica1.org/00b/src/1740432283914.jpg",
                        thumb="https://gita.komica1.org/00b/thumb/1740432283914s.jpg",
                    ).image,
                contents=[
                    paragraph.image(
                        s="https://gita.komica1.org/00b/src/1740432283914.jpg",
                        thumb="https://gita.komica1.org/00b/thumb/1740432283914s.jpg",
                    ),
                    paragraph.text("美國正式加入中俄勢力"),
                    paragraph.new_line(),
                    paragraph.text("島民現在在想什麼?"),
                ],
                latest_reply_created_at=1740432471,
                replies_count=1,
                tags=[],
                url='https://gaia.komica1.org/1/pixmicat.php?res=26765435',
            )
            thread_info2 = domain.Post(
                id="26765468",
                thread_id="26765468",
                board_id="gaia/1",
                title="無題",
                author_id="ID:tMp8iWdc",
                author_name="26765468",
                created_at=1740434415,  # 2025/02/25(二) 06:00:15.732 GMT+8
                liked=0,
                disliked=0,
                comments=0,
                image=paragraph.image(
                        s="https://gita.komica1.org/00b/src/1740434415657.jpg",
                        thumb="https://gita.komica1.org/00b/thumb/1740434415657s.jpg",
                    ).image,
                contents=[
                    paragraph.image(
                        s="https://gita.komica1.org/00b/src/1740434415657.jpg",
                        thumb="https://gita.komica1.org/00b/thumb/1740434415657s.jpg",
                    ),
                    paragraph.text("清晨清姬清雞雞"),
                ],
                latest_reply_created_at=0,
                replies_count=0,
                tags=[],
                url='https://gaia.komica1.org/1/pixmicat.php?res=26765468',
            )
            thread_info3 = domain.Post(
                id="26765356",
                thread_id="26765356",
                board_id="gaia/1",
                title="無題",
                author_id="ID:lkoVmHUo",
                author_name="26765356",
                created_at=1740426590,  # 2025/02/25(二) 03:49:50.664 GMT+8
                liked=0,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    paragraph.video(
                        s="https://gita.komica1.org/00b/src/1740426590497.webm",
                    ),
                    paragraph.text("有洗貓的影片嗎"),
                ],
                latest_reply_created_at=1740434260,  # 2025/02/25(二) 03:49:50.664 GMT+8
                replies_count=3,
                tags=[],
                url='https://gaia.komica1.org/1/pixmicat.php?res=26765356',
            )
            self.assertEqual(thread_infos[0], thread_info1)
            self.assertEqual(thread_infos[1], thread_info2)
            self.assertEqual(thread_infos[2], thread_info3)
            self.assertEqual(current_page, 1)
            self.assertEqual(total_page, 820)
            self.assertEqual(len(thread_infos), 3)

    def test_parse_thread_post_html(self):
        with open(get_html_filename("thread_detail.fragment.html"), "r") as f:
            html = f.read()
            post = parse_original_post_html(html, 'gaia/1', '26812758', None)
            post1 = domain.Post(
                id="26812758",
                thread_id="26812758",
                board_id="gaia/1",
                author_id="ID:r76NdmK.(1/4)",
                author_name="26812758",
                created_at=1740886170,  # 2025/03/02(日) 11:29:30.725 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
                image=paragraph.image(
                        s="https://img.youtube.com/vi/AP0N4-4JLdA/0.jpg",
                        thumb="https://img.youtube.com/vi/AP0N4-4JLdA/0.jpg",
                    ).image,
                contents=[
                    paragraph.video(
                        s="https://gita.komica1.org/00b/src/1741657478203.webm",
                    ),
                    paragraph.youtube_video(s="https://www.youtube.com/watch?v=AP0N4-4JLdA"),
                ],
                tags=[],
                latest_reply_created_at=1740886961,  # 2025/03/02(日) 11:42:41.772 GMT+8
                replies_count=6,
                url='https://gaia.komica1.org/1/pixmicat.php?res=26812758',
            )
            self.assertEqual(post, post1)

    def test_parse_regarding_posts_html(self):
        with open(get_html_filename("thread_detail.fragment.html"), "r") as f:
            html = f.read()
            posts = parse_replies_html(html, 'gaia/1', 'mock', None)
            post1 = domain.Post(
                id="26812766",
                thread_id="mock",
                board_id="gaia/1",
                author_id="ID:r76NdmK.(2/4)",
                author_name="26812766",
                created_at=1740886260,  # 2025/03/02(日) 11:31:00.943 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
                image=paragraph.image(s="https://gita.komica1.org/00b/src/1740886260520.jpg", thumb="https://gita.komica1.org/00b/thumb/1740886260520s.jpg").image,
                contents=[
                    paragraph.image(s="https://gita.komica1.org/00b/src/1740886260520.jpg", thumb="https://gita.komica1.org/00b/thumb/1740886260520s.jpg"),
                    paragraph.text("無本文"),
                ],
                tags=[],
                latest_reply_created_at=0,
                replies_count=0,
                url=None,
            )
            post2 = domain.Post(
                id="26812792",
                thread_id="mock",
                board_id="gaia/1",
                author_id="ID:Vzxlijiw",
                author_name="26812792",
                created_at=1740886457,  # 2025/03/02(日) 11:34:17.391 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    paragraph.reply_to(id="26812758", preview=''),
                    paragraph.new_line(),
                    paragraph.text("法蘭可愛"),
                ],
                tags=[],
                latest_reply_created_at=0,
                replies_count=0,
                url=None,
            )
            post3 = domain.Post(
                id="26812814",
                thread_id="mock",
                board_id="gaia/1",
                author_id="ID:r76NdmK.(3/4)",
                author_name="26812814",
                created_at=1740886613,  # 2025/03/02(日) 11:36:53.647 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
                image=paragraph.image(s="https://gita.komica1.org/00b/src/1740886613383.jpg", thumb="https://gita.komica1.org/00b/thumb/1740886613383s.jpg").image,
                contents=[
                    paragraph.image(s="https://gita.komica1.org/00b/src/1740886613383.jpg", thumb="https://gita.komica1.org/00b/thumb/1740886613383s.jpg"),
                    paragraph.link("https://x.com/priconne_redive/status/1896033263946444971/photo/1"),
                ],
                tags=[],
                latest_reply_created_at=0,
                replies_count=0,
                url=None,
            )
            post4 = domain.Post(
                id="26812830",
                thread_id="mock",
                board_id="gaia/1",
                author_id="ID:r76NdmK.(4/4)",
                author_name="26812830",
                created_at=1740886843,  # 2025/03/02(日) 11:40:43.161 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
                image=paragraph.image(s="https://gita.komica1.org/00b/src/1740886843049.jpg", thumb="https://gita.komica1.org/00b/thumb/1740886843049s.jpg").image,
                contents=[
                    paragraph.image(s="https://gita.komica1.org/00b/src/1740886843049.jpg", thumb="https://gita.komica1.org/00b/thumb/1740886843049s.jpg"),
                    paragraph.text("無本文"),
                ],
                tags=[],
                latest_reply_created_at=1740886961,  # 2025/03/02(日) 11:42:41.772 GMT+8
                replies_count=1,
                url=None,
            )
            post5 = domain.Post(
                id="26812836",
                thread_id="mock",
                board_id="gaia/1",
                author_id="ID:Tx/LDMKs",
                author_name="26812836",
                created_at=1740886939,  # 2025/03/02(日) 11:42:19.134 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    paragraph.reply_to(id="26812758", preview=''),
                    paragraph.new_line(),
                    paragraph.text("感覺女角越穿越少..?"),
                ],
                tags=[],
                latest_reply_created_at=0,
                replies_count=0,
                url=None,
            )
            post6 = domain.Post(
                id="26812841",
                thread_id="mock",
                board_id="gaia/1",
                author_id="ID:dvKAH0Qw",
                author_name="26812841",
                created_at=1740886961,  # 2025/03/02(日) 11:42:41.772 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    paragraph.reply_to(id="26812830", preview='[圖片]無本文'),
                    paragraph.new_line(),
                    paragraph.text("誰"),
                ],
                tags=[],
                latest_reply_created_at=0,
                replies_count=0,
                url=None,
            )
            self.assertEqual(posts[0], post1)
            self.assertEqual(posts[1], post2)
            self.assertEqual(posts[2], post3)
            self.assertEqual(posts[3], post4)
            self.assertEqual(posts[4], post5)
            self.assertEqual(posts[5], post6)
            self.assertEqual(len(posts), 6)

    def test_parse_regarding_posts_html_with_post_id(self):
        with open(get_html_filename("thread_detail.fragment.html"), "r") as f:
            html = f.read()
            posts = parse_replies_html(html, 'gaia/1', 'mock', "26812830")
            post6 = domain.Post(
                id="26812841",
                thread_id="mock",
                board_id="gaia/1",
                author_id="ID:dvKAH0Qw",
                author_name="26812841",
                created_at=1740886961,  # 2025/03/02(日) 11:42:41.772 GMT+8
                title="無題",
                liked=0,
                disliked=0,
                comments=0,
                image=None,
                contents=[
                    paragraph.reply_to(id="26812830", preview='[圖片]無本文'),
                    paragraph.new_line(),
                    paragraph.text("誰"),
                ],
                tags=[],
                latest_reply_created_at=0,
                replies_count=0,
                url=None,
            )
            self.assertEqual(posts[0], post6)
            self.assertEqual(len(posts), 1)


def get_html_filename(filename: str):
    return os.path.join(os.path.dirname(__file__), filename)

def print_json(pb2_obj):
    d = MessageToDict(pb2_obj)
    print(json.dumps(d, indent=2, ensure_ascii=False))
