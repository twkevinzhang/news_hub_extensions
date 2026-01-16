# News Hub Extension Development Guide

This guide outlines the standards and procedures for developing extensions for News Hub. Unlike traditional standalone gRPC servers, News Hub extensions are **Python packages** dynamically loaded by the main application's sidecar at runtime.

## 1. Architecture Overview

- **Host Environment**: Your extension runs within the generic Python Sidecar process of the News Hub app.
- **Runtime Loading**: The sidecar downloads your extension (source code) to the device's storage and uses Python's `importlib` to load it.
- **No Pip Install**: The end-user's device cannot run `pip install`. You cannot rely on downloading dependencies at runtime.

Each extension must follow a strictly isolating directory structure and use BOTH unique Protobuf package names AND unique Proto filenames to prevent namespace/symbol collisions in the global descriptor pool.

### Namespace Convention

- **Directory**: `your_extension_name/` (should match your author and name)
- **Protobuf Package**: `news_hub.extension.{author}.{name}`
- **Protobuf Filename**: `{author}_{name}_api.proto` (e.g., `komica_api.proto`)

```
your_extension_name/
├── src/
│   ├── resolver_impl.py      # ENTRY POINT: Must implement ResolverImpl
│   ├── domain.py
│   ├── ...
│   └── __init__.py           # Required for package recognition
├── requirements.txt          # For local development/testing only
├── ...
```

### Essential Rules for `src/`

1. **Relative Imports ONLY**: You CANNOT use absolute imports for your own modules.

   - ❌ `import domain` (Will conflict if another extension has `domain.py`)
   - ✅ `from . import domain`
   - ✅ `from .utilities import helper`

2. **Entry Point**: You must have a `resolver_impl.py` containing a class named `ResolverImpl`.

## 3. Dependency Management

Since valid `pip install` is impossible on mobile devices at runtime, we use a **"Batteries-Included"** strategy.

### A. Host-Provided Libraries

The following libraries are built into the News Hub Sidecar. You can import them directly without bundling them.

- `aiohttp` (Async HTTP client)
- `beautifulsoup4` (HTML parsing)
- `lxml` (Fast XML/HTML processing)
- `grpcio` & `protobuf` (Communication)
- `asyncio` & Standard Python 3.8+ Library

**Do NOT** include these in your final distribution bundle. You should list them in your development `requirements.txt` for local testing (IntelliSense/PyTest).

**Platform Contract**: The News Hub Runtime **guarantees** these libraries are available globally. You can rely on them being present in the environment just like the Python standard library.

### B. Pure Python Dependencies

If you need a library NOT in the list above (e.g., `faker`, `python-dateutil`):

1. It must be **Pure Python** (no C extensions, no compilation required).
2. You must **Vendor (Bundle)** the source code of that library directly inside your `src/` folder.
   - Example: `src/my_extension/utils/dateutil/...`

## 4. Implementation Details (`resolver_impl.py`)

News Hub uses a **Shared Domain** architecture with an **Adapter Pattern**. This allows extensions to bundle their own generated Protobuf code while remaining isolated from other extensions.

### Workflow:

1.  **Define Unique Namespaces AND Filenames**:
    Every extension **MUST** use a unique, hierarchical package name AND a unique file name for its `.proto` files. Protobuf does not allow loading two files with the same name (e.g., `sidecar_api.proto`) into the same process, even if they have different packages.

    - Package Format: `news_hub.extension.{author}.{name}`
    - Filename Format: `{author}_{name}_api.proto`

2.  **Import & Rename Shared Domain Models**:
    Download `domain_models.proto` from the [Main Repository](https://github.com/twkevinzhang/news_hub/tree/master/news_hub_protos) and **rename it** to include your extension's name (e.g., `komica_domain_models.proto`) before importing it.

    ```protobuf
    syntax = "proto3";
    // Unique namespace AND unique filename (komica_api.proto)
    package news_hub.extension.komica;

    // Use a unique filename for the imported domain models
    import "komica_domain_models.proto";

    // Define your service using Shared Domain types
    service KomicaResolver {
      rpc GetBoards (GetBoardsReq) returns (GetBoardsRes);
    }
    // ... define messages compatible with Sidecar API ...
    ```

3.  **Generate Python Code**:
    Generate your `_pb2.py` files. Note that you don't necessarily need `_pb2_grpc.py` for the extension's internal implementation since the Sidecar uses a dynamic adapter to call your methods.

4.  **Implement `ResolverImpl`**:
    Your implementation must return your own namespaced Protobuf messages. You do NOT need to inherit from any generated gRPC class.

    ```python
    # src/resolver_impl.py
    from . import komica_api_pb2 as pb2
    from . import komica_domain_models_pb2 as domain_pb2
    from . import salt

    class ResolverImpl:
        def __init__(self):
            self.pkg_name = "twkevinzhang_komica"

        def GetBoards(self, req: pb2.GetBoardsReq, context) -> pb2.GetBoardsRes:
            # Note: req and returned messages are from your OWN namespace.
            # Sidecar handles the conversion automatically.
            return pb2.GetBoardsRes(
                boards=[
                    domain_pb2.Board(
                        id=salt.encode("board_1"),
                        name="General",
                        pkg_name=self.pkg_name
                    )
                ]
            )
    ```

### Why this works:

Despite different Python class types (e.g., `news_hub.extension.komica.GetSiteRes` vs `news_hub.sidecar.GetSiteRes`), the **binary representation** of identical schemas is the same. The Sidecar serializes your response to bytes and parses it using its own internal Protobuf classes, ensuring type isolation without losing data.

## 5. Testing & Verification

Since your code runs in a potentially crowded namespace (Sidecar has many loaded modules), your tests must ensure isolation.

1. **Local Dev**: Use a virtual environment.
2. **Import Verification**: Verify that your code never calls `import my_module` without the relative dot.

### Verification Script Example

Create a test script that simulates loading your package as a module:

```python
import sys
from pathlib import Path

# Simulate sidecar adding your repo to path
sys.path.append("/path/to/your/repo")

# Try importing
from your_extension_name.src import resolver_impl
```

## 6. Migration Checklist (for existing extensions)

- [ ] Add `__init__.py` to `src/`.
- [ ] Convert ALL internal imports to relative imports (e.g., `from domain` -> `from . import domain`).
- [ ] Ensure no binary dependencies are required beyond the Host-Provided list.
- [ ] Rename/Move helper files if they use generic names that might confuse yourself (though relative imports protect the runtime).
