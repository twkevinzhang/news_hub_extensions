# News Hub Extension Development Guide

This guide outlines the standards and procedures for developing extensions for News Hub. Unlike traditional standalone gRPC servers, News Hub extensions are **Python packages** dynamically loaded by the main application's sidecar at runtime.

## 1. Architecture Overview

- **Host Environment**: Your extension runs within the generic Python Sidecar process of the News Hub app.
- **Runtime Loading**: The sidecar downloads your extension (source code) to the device's storage and uses Python's `importlib` to load it.
- **No Pip Install**: The end-user's device cannot run `pip install`. You cannot rely on downloading dependencies at runtime.

## 2. Project Structure

Each extension must follow a strictly isolating directory structure to prevent namespace collisions with other extensions.

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

Your extension must implement the gRPC servicer interface defined in `extension_api.proto`.

```python
# src/resolver_impl.py
import extension_api_pb2_grpc as pb2_grpc
from . import domain  # Note the relative import!

class ResolverImpl(pb2_grpc.ExtensionApiServicer):
    def __init__(self):
        pass

    # Implement methods: GetSite, GetBoards, GetThreadInfos, etc.
```

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
