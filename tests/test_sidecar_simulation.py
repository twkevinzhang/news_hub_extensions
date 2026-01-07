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
        Simulate the exact steps Sidecar uses to load an extension:
        1. Import isolation
        2. Interface compatibility via Adapter Pattern (serialization)
        """
        pkg_name = "twkevinzhang_komica"
        
        # --- Step 1: Loading (Standard Import Strategy) ---
        logger.info(f"Simulating loading of {pkg_name}...")
        
        ext_path_str = str(self.komica_path)
        if ext_path_str not in sys.path:
            sys.path.insert(0, ext_path_str)
            
        target_module_name = f"{pkg_name}.resolver_impl"
        
        try:
            # We want to ensure that importing the extension DOES NOT conflict with any sidecar protos
            # even if the extension uses 'package pb'.
            module = importlib.import_module(target_module_name)
            logger.info(f"Successfully imported {target_module_name}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.fail(f"Failed to import module: {e}")

        # --- Step 2: Instantiation ---
        logger.info("Instantiating ResolverImpl...")
        ResolverImpl = getattr(module, "ResolverImpl")
        resolver = ResolverImpl()
        self.assertIsNotNone(resolver)
        
        # --- Step 3: Simulation of Sidecar Adapter Pattern ---
        logger.info("Testing Adapter Pattern compatibility...")
        
        # Access the extension's protobuf classes
        ext_pb2 = module.pb2
        
        # Create a dummy request using EXTENSION'S protobuf
        req = ext_pb2.Empty()
        context = MagicMock()
        
        # Call GetSite
        try:
            ext_res = resolver.GetSite(req, context)
            logger.info(f"Extension returned: {ext_res.site.name} ({ext_res.__class__})")
            
            # SIMULATION: Sidecar's conversion logic
            # This is how Sidecar 'translates' the extension's output to its own Domain
            # We simulate this by checking if it can be serialized and would fit a schema.
            serialized = ext_res.SerializeToString()
            self.assertTrue(len(serialized) > 0, "Response should be serializable")
            
            # Verify basic domain requirements
            self.assertEqual(ext_res.site.name, "komica1.org")
            
        except Exception as e:
            self.fail(f"GetSite call failed: {e}")

        # --- Step 4: Verification of Field IDs (Binary Compatibility) ---
        logger.info("Verifying Binary Compatibility...")
        req_boards = ext_pb2.GetBoardsReq(site_id="komica")
        try:
            res_boards = resolver.GetBoards(req_boards, context)
            self.assertTrue(len(res_boards.boards) > 0)
            
            # Check if critical fields exist (adapter-safe)
            first_board = res_boards.boards[0]
            self.assertTrue(hasattr(first_board, 'pkg_name'), "Board must have pkg_name field")
            self.assertEqual(first_board.pkg_name, "twkevinzhang_komica")
            
            logger.info("Binary Compatibility check passed.")
            
        except Exception as e:
             self.fail(f"Binary compatibility check failed: {e}")

if __name__ == "__main__":
    unittest.main()
