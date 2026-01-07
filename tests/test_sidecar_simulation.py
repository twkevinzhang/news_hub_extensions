import importlib.util
import sys
import logging
from pathlib import Path
import os
import unittest
from unittest.mock import MagicMock
import asyncio

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("test_sidecar_loader")

class TestSidecarExtensionLoader(unittest.TestCase):
    def setUp(self):
        # 1. Simulate Sidecar Environment Paths
        # The test is running from news_hub_extensions root
        self.extensions_root = Path(os.getcwd())
        self.komica_path = self.extensions_root / "twkevinzhang_komica"
        
        if not self.komica_path.exists():
            self.fail(f"Extension path not found: {self.komica_path}")

    def test_dynamic_loading_and_execution(self):
        """
        Simulate the exact steps Sidecar uses to load an extension
        and verify we can call its methods via the gRPC servicer interface.
        """
        pkg_name = "twkevinzhang_komica"
        
        # --- Step 1: Loading (Standard Import Strategy) ---
        logger.info(f"Simulating loading of {pkg_name} using Standard Import Standard...")
        
        # With the new structure:
        # /path/to/extensions/twkevinzhang_komica/  <-- Add this to sys.path
        #     twkevinzhang_komica/                  <-- Package folder
        #         __init__.py
        #         resolver_impl.py
        
        ext_path_str = str(self.komica_path)
        if ext_path_str not in sys.path:
            logger.info(f"Adding {ext_path_str} to sys.path")
            sys.path.insert(0, ext_path_str)
            
        # Now we can simply import the package by name!
        # This is the standard, pythonic way.
        target_module_name = f"{pkg_name}.resolver_impl"
        
        try:
            # Sidecar can still use spec_from_file_location if it wants specific file control,
            # OR just use import_module since path is set.
            # Using import_module simulates "import twkevinzhang_komica.resolver_impl"
            module = importlib.import_module(target_module_name)
            logger.info(f"Successfully imported {target_module_name}")
            
        except ImportError as e:
            import traceback
            traceback.print_exc()
            self.fail(f"Failed to import module: {e}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.fail(f"Failed to import module (Unexpected): {e}")

        # --- Step 2: Instantiation ---
        logger.info("Instantiating ResolverImpl...")
        
        if not hasattr(module, "ResolverImpl"):
            self.fail("Module does not have ResolverImpl class")
            
        ResolverImpl = getattr(module, "ResolverImpl")
        resolver = ResolverImpl()
        
        self.assertIsNotNone(resolver, "Resolver instance should not be None")
        
        # --- Step 3: Execution (Simulate gRPC calls) ---
        logger.info("Testing GetSite method...")
        
        # We need to mock the request object and context since we don't have the full protobuf stack here easily accessible
        # OR we can assume the module loaded its own protobufs successfully (which passed the import test).
        # To call the method normally, we need proper protobuf objects.
        # Since 'module' has loaded the extension's protobufs via relative import, we can access them through the module!
        
        # Access the protobuf classes from the loaded module's imports
        # resolver_impl imports 'extension_api_pb2' as 'pb2'
        pb2 = module.pb2
        
        # Create a dummy request
        req = pb2.Empty()
        context = MagicMock()
        
        # Call GetSite
        try:
            res = resolver.GetSite(req, context)
            logger.info(f"GetSite result: {res}")
            
            self.assertEqual(res.site.name, "komica1.org")
            self.assertEqual(res.site.url, "https://komica1.org")
            
        except Exception as e:
            self.fail(f"GetSite call failed: {e}")

        # --- Step 4: Test Async Method (GetBoards) ---
        # GetBoards is regular method in this implementation, not async def, but it might call async parsers?
        # Looking at code: GetBoards calls parse_boards.list(), which is sync.
        logger.info("Testing GetBoards method...")
        
        req_boards = pb2.GetBoardsReq(site_id="1") # Using specific ID might be needed
        try:
            res_boards = resolver.GetBoards(req_boards, context)
            self.assertTrue(len(res_boards.boards) > 0, "Should return at least one board")
            first_board = res_boards.boards[0]
            logger.info(f"First board: {first_board.name}")
            self.assertEqual(first_board.pkg_name, "twkevinzhang_komica")
            
        except Exception as e:
             self.fail(f"GetBoards call failed: {e}")

if __name__ == "__main__":
    unittest.main()
