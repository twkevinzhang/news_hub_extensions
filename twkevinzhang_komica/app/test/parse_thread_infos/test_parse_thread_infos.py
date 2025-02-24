import json
import os
from unittest import TestCase

from google.protobuf.json_format import MessageToDict

from src.parse_thread_infos import parse_thread_infos_html


class TestParseThreadInfos(TestCase):
    def test_parse_thread_infos_html(self):
        with open(get_html_filename("thread_infos.fragment.html"), "r") as f:
            html = f.read()
            threads = parse_thread_infos_html(html)
            self.assertEqual(len(threads), 30)


def get_html_filename(filename: str):
    return os.path.join(os.path.dirname(__file__), filename)

def print_json(pb2_obj):
    d = MessageToDict(pb2_obj)
    print(json.dumps(d, indent=2, ensure_ascii=False))
