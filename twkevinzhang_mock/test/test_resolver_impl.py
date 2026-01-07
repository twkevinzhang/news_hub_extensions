import unittest
from twkevinzhang_mock.resolver_impl import ResolverImpl
from twkevinzhang_mock import sidecar_api_pb2 as pb2
from twkevinzhang_mock import domain_models_pb2 as domain_pb2

class TestResolverImpl(unittest.TestCase):
    def setUp(self):
        self.resolver = ResolverImpl()

    def test_get_boards(self):
        req = pb2.GetBoardsReq(pkg_name="twkevinzhang_mock")
        res = self.resolver.GetBoards(req, None)
        self.assertGreater(len(res.boards), 0)
        self.assertEqual(res.boards[0].name, "General Discussion")

    def test_get_threads(self):
        req = pb2.GetThreadsReq(pkg_name="twkevinzhang_mock", board_id="mock/board_1")
        res = self.resolver.GetThreads(req, None)
        self.assertGreater(len(res.threads), 0)
        self.assertIn("thread_", res.threads[0].id)

if __name__ == '__main__':
    unittest.main()
