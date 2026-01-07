# News Hub Extension Development Guide

This guide outlines the standards and procedures for developing extensions for News Hub. Unlike traditional standalone gRPC servers, News Hub extensions are **Python packages** dynamically loaded by the main application's sidecar at runtime.

## 1. Architecture Overview

- **Host Environment**: Your extension runs within the generic Python Sidecar process of the News Hub app.
- **Runtime Loading**: The sidecar downloads your extension (source code) to the device's storage and uses Python's `importlib` to load it.
- **No Pip Install**: The end-user's device cannot run `pip install`. You cannot rely on downloading dependencies at runtime.

Each extension must follow a strictly isolating directory structure and use a unique Protobuf package name to prevent namespace/symbol collisions.

### Namespace Convention

- **Directory**: `your_extension_name/` (should match your author and name)
- **Protobuf Package**: `news_hub.extension.{author}.{name}`

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

1.  **Define a Unique Namespace**:
    Every extension **MUST** use a unique, hierarchical package name in its `.proto` file to prevent symbol collisions at the Protobuf descriptor level.

    - Format: `news_hub.extension.{author}.{name}`

2.  **Import Shared Domain Models**:
    Download the shared `domain_models.proto` from the [Main Repository](https://github.com/twkevinzhang/news_hub/tree/master/news_hub_protos) and import it into your extension's `.proto`.

    ```protobuf
    syntax = "proto3";
    // Unique namespace prevents collisions with other extensions
    package news_hub.extension.komica;

    // Import the Shared Domain definitions
    import "domain_models.proto";

    // Define your service using Shared Domain types
    service KomicaResolver {
      // You can use types from news_hub.domain directly
      rpc GetSite (news_hub.domain.Empty) returns (GetSiteRes);
    }

    message GetSiteRes {
      news_hub.domain.Site site = 1;
    }
    ```

3.  **Generate Python Code**:
    Generate your `_pb2.py` and `_pb2_grpc.py` files using the `grpc_tools.protoc` compiler. You are encouraged to bundle these generated files within your extension.

4.  **Implement `ResolverImpl`**:
    Your implementation must return your own namespaced Protobuf messages. The Sidecar's adapter layer will automatically handle the conversion to its internal domain models using binary serialization.

    ```python
    # src/resolver_impl.py
    from . import extension_api_pb2 as pb2
    from . import extension_api_pb2_grpc as pb2_grpc
    from . import salt

    class ResolverImpl(pb2_grpc.ExtensionApiServicer):
        def __init__(self):
            self.site_id = "komica"
            self.pkg_name = "twkevinzhang_komica"

        def GetSite(self, req: pb2.GetSiteReq, context) -> pb2.GetSiteRes:
            # Note: We are returning our OWN namespaced GetSiteRes
            return pb2.GetSiteRes(
                site=pb2.Site(
                    id=salt.encode(self.site_id),
                    pkg_name=self.pkg_name,
                    icon="https://komica1.org/favicon.ico",
                    name="Komica",
                    description="A popular imageboard",
                    url="https://komica1.org",
                )
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
