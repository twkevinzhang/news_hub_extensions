import unittest
from twkevinzhang_mock.resolver_impl import ResolverImpl
from twkevinzhang_mock import extension_api_pb2 as pb2

class TestResolverImpl(unittest.TestCase):
    def setUp(self):
        self.resolver = ResolverImpl()

    def test_get_site(self):
        res = self.resolver.GetSite(pb2.Empty(), None)
        self.assertEqual(res.site.name, "Mock Site")
        self.assertTrue(res.site.id.startswith("mock_"))

    def test_get_boards(self):
        req = pb2.GetBoardsReq()
        res = self.resolver.GetBoards(req, None)
        self.assertGreater(len(res.boards), 0)
        self.assertEqual(res.boards[0].name, "General Discussion")

    def test_get_thread_infos(self):
        req = pb2.GetThreadInfosReq(site_id="mock_site")
        res = self.resolver.GetThreadInfos(req, None)
        self.assertGreater(len(res.thread_infos), 0)
        self.assertIn("mock_", res.thread_infos[0].id)

if __name__ == '__main__':
    unittest.main()
