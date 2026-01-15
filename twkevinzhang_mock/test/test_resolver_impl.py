import unittest
from twkevinzhang_mock.resolver_impl import ResolverImpl
from twkevinzhang_mock import mock_api_pb2 as pb2
from twkevinzhang_mock import mock_domain_models_pb2 as domain_pb2

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
        self.assertEqual(len(res.threads), 20)
        self.assertIn("thread_", res.threads[0].id)

    def test_search_threads(self):
        # Test keyword search
        req = pb2.GetThreadsReq(pkg_name="twkevinzhang_mock", keywords="Gemini")
        res = self.resolver.GetThreads(req, None)
        self.assertGreater(len(res.threads), 0)
        self.assertIn("[Gemini]", res.threads[0].single_image_post.title)

    def test_search_empty_result(self):
        # Test "empty" keyword returns no result
        req = pb2.GetThreadsReq(pkg_name="twkevinzhang_mock", keywords="empty")
        res = self.resolver.GetThreads(req, None)
        self.assertEqual(len(res.threads), 0)
        self.assertEqual(res.page.total_page, 0)

    def test_sorting_hot(self):
        # Test "hot" sorting (based on likes)
        req = pb2.GetThreadsReq(pkg_name="twkevinzhang_mock", sort="hot")
        res = self.resolver.GetThreads(req, None)
        # Check if they are descending
        for i in range(len(res.threads) - 1):
            val_curr = res.threads[i].single_image_post.liked
            val_next = res.threads[i+1].single_image_post.liked
            self.assertGreaterEqual(val_curr, val_next)

    def test_pagination(self):
        # Test second page
        req = pb2.GetThreadsReq(
            pkg_name="twkevinzhang_mock", 
            page=domain_pb2.PaginationReq(page=2, page_size=10)
        )
        res = self.resolver.GetThreads(req, None)
        self.assertEqual(len(res.threads), 10)
        self.assertEqual(res.page.current_page, 2)
        self.assertEqual(res.page.total_page, 10)

if __name__ == '__main__':
    unittest.main()
