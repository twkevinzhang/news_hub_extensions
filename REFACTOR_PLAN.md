# Modification Plan: Migrating Extensions to Dynamic Libraries

This plan outlines the steps to refactor `twkevinzhang_komica` and `twkevinzhang_mock` to comply with the new `EXTENSION_DEVELOPMENT.md` standards.

## Objectives

1.  **Namespace Safety**: Convert all imports to relative imports to prevent dynamic loading usage conflicts.
2.  **Runtime Compatibility**: Ensure reliance only on Host-Provided libraries.
3.  **Entry Point Standardization**: Verify `ResolverImpl` accessibility.

## Phase 1: `twkevinzhang_komica` Refactor

### 1.1 Source Code Adjustments (`src/`)

- **Add `__init__.py`**: Mark the directory as a package.
- **Refactor Imports**:
  - `resolver_impl.py`:
    - `import parse_boards` -> `from . import parse_boards`
    - `import salt` -> `from . import salt`
    - `from domain import ...` -> `from .domain import ...`
    - `from parse_threads import ...` -> `from .parse_threads import ...`
    - `from requester import ...` -> `from .requester import ...`
    - `from utilities import ...` -> `from .utilities import ...`
  - `parse_threads.py`:
    - `from domain import ...` -> `from .domain import ...`
    - `from utilities import ...` -> `from .utilities import ...`
  - Any other files using internal modules must use `from . import module`.

### 1.2 Verification

- **Requirements Check**: Confirm `requirements.txt` only lists: `protobuf`, `grpcio`, `lxml`, `aiohttp`, `beautifulsoup4`. All of these are provided by the Host Sidecar. No action needed but to verify version compatibility.
- **Test Suite Loop**: Since tests usually run from the root, we need to ensure they can still import the code correctly.
  - Tests might need to do `from src import ...` or `from twkevinzhang_komica.src import ...` depending on how `pytest` is invoked.

## Phase 2: `twkevinzhang_mock` Refactor

### 2.1 Source Code Adjustments

- Similar to Komica, ensure all internal imports are relative.

## Phase 3: Validation

### 3.1 Simulation Script

Create a script `simulate_load.py` in the root of `news_hub_extensions`:

1.  Iterate through directories (`twkevinzhang_komica`, etc.).
2.  Attempt to load `resolver_impl` using `importlib` without adding the _inner_ `src` to `sys.path`, but rather adding the extension root.
    - _Correction_: The sidecar logic usually adds the extension folder (e.g., `/.../twkevinzhang_komica`) to `sys.path`.
    - Then it loads `src.resolver_impl`? Or does it expect `src` to be in path?
    - **Critical Dictionary Check**: The current sidecar implementation (line 29 of `extension_loader.py`) adds `extension_path` (the folder containing `src`) to `sys.path`.
    - It then loads `resolver_impl.py` directly as a file.
    - **Correction for Sidecar**: If the sidecar loads the file directly via `spec_from_file_location`, relative imports might define package scope differently.
    - **Preferred Approach**: To support relative imports properly (`from . import domain`), the loaded file must be considered part of a package.
    - **Action Item**: We likely need to treat `src` as a package.

## Execution Order

1.  Apply changes to `twkevinzhang_komica/src`.
2.  Run existing tests to ensure no regression.
3.  Apply changes to `twkevinzhang_mock/src`.
