# GEMINI.md

本文件為 Gemini 在本 repository 中工作時的指導文件。

## 專案概覽

本倉庫是 **News Hub AI 的擴充市場** (主專案位於 `../news_hub_ai`)。包含多個基於 Python 的 gRPC 擴充功能，提供從各種來源（論壇、新聞網站等）聚合內容的能力。

### 與主專案的關係

- **主專案**: `../news_hub_ai` - Flutter 應用程式搭配 Python sidecar 服務
- **本倉庫**: 擴充市場，包含可安裝的內容提供者
- **整合方式**: Sidecar 服務 (`news_hub_ai/sidecar/src/application/services/extension_loader.py`) 動態載入本倉庫的擴充
- **載入機制**: 擴充通過匯入其 `resolver_impl.py` 載入，該文件必須包含 `ResolverImpl` 類
- **技術架構**: 使用 [flet-dev/serious-python](https://github.com/flet-dev/serious-python) 將 Python 代碼打包進 Flutter app

每個擴充都是一個獨立的套件，實作由 Protocol Buffers 定義的 `ExtensionApiServicer` 介面。

## Extension Architecture

### Core Concepts

- **Extension Package**: Self-contained directory (e.g., `twkevinzhang_komica/`) implementing the gRPC API
- **Repository Metadata**: Root-level JSON files configure extension discovery and distribution
  - `extensions.json`: Lists available extensions with metadata (display_name, version, python_version, etc.)
  - `repo.json`: Repository-level configuration (icon, base_url, signing_key)

### Extension Structure

Each extension follows this pattern:

```
extension_name/
├── src/
│   ├── resolver_impl.py      # gRPC service implementation (ExtensionApiServicer)
│   ├── domain.py              # Core domain models (Post, board_id_to_url_prefix)
│   ├── parse_*.py             # HTML parsers for different content types
│   ├── requester.py           # Async HTTP client with aiohttp
│   ├── salt.py                # ID encoding/decoding
│   ├── extension_api_pb2.py   # Generated protobuf code
│   └── extension_api_pb2_grpc.py
├── test/                      # Unit tests
├── test_resolver_impl.py      # Integration test / dev server
├── requirements.txt           # Pinned dependencies
├── makefile                   # Build commands
└── build/                     # Cross-platform builds (arm64-v8a, armeabi-v7a, x86, x86_64)
```

### gRPC Service Interface

Extensions implement these key RPC methods in `resolver_impl.py`:

- `GetBoards()`: Returns list of boards/sections
- `GetThreads()`: Fetches thread listings with pagination
- `GetOriginalPost()`: Retrieves full thread content
- `GetReplies()`: Gets related/reply posts
- `GetComments()`: Comment handling (may be unimplemented)

### Data Flow

1. **Encoding**: All IDs (board_id, thread_id, post_id) are encoded using `salt.encode()` before returning to gRPC
2. **Decoding**: Request IDs are decoded using `salt.decode()` at the start of each RPC method
3. **HTML Parsing**: BeautifulSoup (lxml) extracts structured data from fetched HTML
4. **Async Requests**: `Requester` class handles concurrent HTTP fetches with aiohttp
5. **Pagination**: Custom `pagination()` helper manages page_size/page logic

### Domain Models

The `Post` class is the central domain model with two presentation modes:

- `article_post`: Full article with all paragraphs (for detail view)
- `single_image_post`: Compact layout emphasizing featured image (for list view)

Posts contain `Paragraph` objects representing different content types (text, images, videos, reply-to references).

## Common Development Commands

### twkevinzhang_komica Extension

```bash
cd twkevinzhang_komica

# Install dependencies
make install

# Run tests
make test

# Run development server (port 55001)
make run
# or
python test_resolver_impl.py

# Clean environment
make clean
```

### Development Environment

- Python 3.12.7 (per README)
- Use virtual environment: `venv/` directory
- Dependencies are pinned in `requirements.txt`

### Protocol Buffers

- Proto definitions generate `extension_api_pb2.py` and `extension_api_pb2_grpc.py`
- Regenerate with: `pip install grpcio-tools===1.67.1` then use grpc_tools
- Generated files are committed to source control

### Building for Distribution

The `build/site-packages/` directory contains cross-compiled Python packages for multiple Android architectures (arm64-v8a, armeabi-v7a, x86, x86_64).

## Key Implementation Patterns

### Error Handling

- `OverPageError`: Raised when pagination exceeds available pages
- Request failures are caught and logged; parser errors are re-raised
- Logging configured in `test_resolver_impl.py` (both file and console handlers)

### Board ID Format

Board IDs follow pattern: `{subdomain}/{board_code}` (e.g., `gita/00b`)

- Convert to URL: `board_id_to_url_prefix()` → `https://{subdomain}.komica1.org/{board_code}`

### Pagination Quirks

- Page numbers start at 1 (user-facing)
- URL pagination differs by page range:
  - Pages 1-10: `/[page+1].htm`
  - Pages 11+: `/pixmicat.php?page_num=[page+1]`
- Some endpoints ignore page_size (determined by upstream HTML structure)

### Content Parsing

Parsers are split by content type:

- `parse_boards.py`: Static board listings (hardcoded Top 50 boards)
- `parse_threads.py`: Thread listings, individual threads, related posts
- HTML content → BeautifulSoup → domain models → protobuf messages

## Repository Structure Notes

- Root directory contains multiple extension packages
- `twkevinzhang_komica`: Production extension for Komica forum
- `twkevinzhang_mock`: Mock/test extension (minimal implementation)
- Extensions are independently versioned via `extensions.json`

## Development Standards

### Version Control

**功能開發任務：**

- 每完成一個獨立功能或重大修改後，必須執行 git commit
- Commit 時使用指定作者：
  - 如果指定 twkevinzhang, 則使用 `git commit --author="twkevinzhang <twkevinzhang@gmail.com>" -m "commit message"`
  - 如果指定 Gemini 3 Flash, 則使用 `git commit --author="Gemini 3 Flash <google-bot@users.noreply.github.com>" -m "commit message"`
  - 如果指定 Sonnet 4.5, 則使用 `git commit --author="Sonnet 4.5 <noreply@anthropic.com>" -m "commit message"`
- Commit message 應使用英文清楚描述變更內容，**必須包含標題與詳細的內文說明**（標題與內文間需有空行分隔）
- Commit message 格式遵循 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/)，且內容需詳細列出具體改動點

**Bug 修復任務 (豁免條款)：**

- **嚴禁執行 git commit**
- AI 於修復完成並通過自動化測試後，應列出修復的邏輯點並**直接宣告任務結束**

### 需求確認機制

**強制中斷與回報 (Mandatory Interruption):**

- 遇到以下情況 **必須立即停止動作**，並列出方案供使用者選擇：
  1. **架構決策分岐**: 技術實現有多種路徑，且涉及目錄結構變更、資料庫 Schema 修改或基礎設施變動。
  2. **潛在風險**: 發現原有架構有重大缺陷，修復它需要大規模重構 (如: 移動大量檔案、重命名核心模組)。
  3. **需求模糊**: 需求描述不完整、有歧義或業務邏輯不明確。

**決策簡報格式:**

- 在詢問時，應使用以下格式簡報：
  - **現狀分析**: 目前架構的限制或問題。
  - **方案 A (保守/繞道)**: 最小改動，可能的副作用。
  - **方案 B (標準/重構)**: 最佳實踐，但成本較高 (如移動檔案)。
  - **推薦建議**: 你的專業建議與理由。

**實作前確認：**

- 當功能需求中使用的技術方案可能不是最佳選擇時，先列出：
  - 需求中提到的方案
  - 建議的替代方案
  - 各方案的優缺點對比
  - 等待確認後再開始實作

### Clean Code Practices

**命名規範：**

- 類別名使用名詞或名詞片語 (如 `PostParser`, `HttpRequester`)
- 方法名使用動詞或動詞片語 (如 `fetch_threads`, `parse_html`)
- 布林變數使用 `is_`, `has_`, `can_` 等前綴 (如 `is_failed`, `has_error`)
- 遵循 PEP 8: 使用 snake_case 命名變數和方法，PascalCase 命名類別
- 避免使用縮寫，除非是業界通用術語 (如 `id`, `url`, `http`)

**方法設計：**

- 單一方法長度不超過 20 行 (不含空行和註解)
- 一個方法只做一件事，符合單一職責原則
- 參數數量不超過 3 個，超過則使用數據類或字典封裝
- 避免使用輸出參數，使用返回值或 tuple

**可讀性優先：**

- 代碼邏輯應該自解釋，通過良好的命名和結構展現意圖
- 盡可能不要寫「做了什麼」的註解，用 Clean Code 的方法，用函數呼叫邏輯以及命名來表達邏輯
- 只在「為什麼這樣做」而非「做了什麼」時才寫註解
- 使用 Guard Clause (提前返回) 減少嵌套層級
- 提取複雜條件判斷為命名清晰的方法

**錯誤處理：**

- 自定義異常類來處理特定錯誤情況 (如 `OverPageError`)
- 使用 logging 模組記錄錯誤和調試信息
- 錯誤信息應該有意義，能指導問題解決
- 適當使用 try-except，但不要過度捕獲異常
- 異常只用於真正的異常情況，可預期的錯誤應使用返回值處理

### Testing Requirements

**測試覆蓋率要求：**

- Unit tests 覆蓋率 > 80%，特別是核心解析邏輯和業務邏輯
- 執行 `python -m pytest --cov=src --cov-report=html tests/` 生成覆蓋率報告
- 關鍵業務邏輯（parser、domain models、gRPC service）必須有完整的測試覆蓋

**測試實踐：**

- 使用 `pytest` 進行測試
- 測試文件放置在 `test/` 目錄
- Mock 外部依賴 (HTTP 請求、文件 I/O) 使用 `pytest-mock` 或 `unittest.mock`
- 測試命名清楚描述測試場景: `test_parse_thread_infos_with_valid_html`
- 測試應覆蓋各種邊界情況和錯誤情況
- 運行測試: `make test` 或 `python -m pytest tests/`

**可測試性設計：**

- 所有組件設計為可測試，使用依賴注入
- Parser 邏輯與 HTTP 請求分離，便於 Mock
- 複雜的業務邏輯提取為獨立函數，便於單元測試

### Code Quality Checks

執行以下檢查確保代碼品質：

```bash
# 語法檢查
python3 -m flake8 src --select=E9,F63,F7,F82 --count

# 運行測試
make test

# 測試覆蓋率
python -m pytest --cov=src --cov-report=html tests/
```

### AI Diagnostic Protocol (Metacognitive Monitoring)

為了防止 AI 陷入無效的邏輯死循環並優化 Token 消耗，AI 在執行任務時必須遵循以下協議：

**防止邏輯死循環 (Loop Detection)：**

- 在提出建議前，檢查該建議是否與前兩次嘗試高度相似
- 若在沒有獲得新日誌或錯誤訊息的情況下，重複要求修改同一段代碼，必須立即停止並承認陷入盲點
- 避免在無新資訊的情況下重複相同的修改嘗試

**層級切換診斷 (Architectural Skepticism)：**

- 若代碼邏輯（語法、if/else）看起來正確但執行失敗（如：客戶端 Loading 超時），必須從代碼層面轉向架構層面檢查
- 檢查 gRPC 連接、端口衝突、網路配置等環境因素
- 檢查 Python 異步事件迴圈和執行緒池配置

**執行緒與併發警示：**

- Extensions 使用 `grpc.aio` 非同步伺服器
- 大部分 Streaming 請求運行在非同步事件迴圈中
- 對於同步的擴展開發或 IO 操作，應使用 `run_in_executor` 委託給執行緒池
- 超時定義：本專案 gRPC 請求的超時判定基準為 `10 秒`
- 若超過此閾值，AI 必須停止重試並轉向架構層面檢查

**中斷與人工干預 (Interruption Protocol)：**

- 若連續 2 次嘗試失敗，AI 應停止自動嘗試
- 動作：列出已排除的可能性，請求使用者提供更高層級的診斷（如：netstat 狀態、執行緒堆疊、環境變數）
- 例外：除非使用者標註 [我在睡覺/請勿打擾]，否則禁止在無把握時盲目消耗 Token

**擴展系統異常處置：**

- 若發生擴展包依賴衝突、`requirements.txt` 安裝失敗或 `serious_python` 運行期環境限制（如 C 擴展不支援），應立即觸發「自我審計協議」
- 停止盲目修改代碼，並向使用者回報可能的環境隔離問題或依賴衝突
- 明確說明診斷假設和已嘗試的方案

**透明度報告：**

- 每次診斷時，應向使用者說明目前的診斷假設
- 清楚列出已排除的可能性和下一步計劃
- 不在不確定的情況下做出承諾

## Adding a New Extension

To add a new extension to the marketplace:

1. **Create extension directory** following the naming pattern: `{author}_{site_name}/`
2. **Implement required structure**:
   - `src/resolver_impl.py` with `ResolverImpl` class implementing `ExtensionApiServicer`
   - `requirements.txt` with pinned dependencies (使用 `===` 固定版本)
   - `makefile` with `install`, `test`, `run` targets
   - `test_resolver_impl.py` for local development/testing
   - `README.md` documenting development environment and setup
3. **Update repository metadata**:
   - Add entry to root `extensions.json` with pkg_name, display_name, version, etc.
   - Ensure `pkg_name` matches directory name
4. **Follow existing patterns**:
   - Use `salt.py` for ID encoding/decoding
   - Implement async HTTP with `requester.py` pattern
   - Parse HTML to domain models, then convert to protobuf
   - Use standard logging configuration
5. **Code quality**:
   - Follow Clean Code practices outlined above
   - Write unit tests with > 80% coverage
   - Pass flake8 checks

## Task Completion Checklist

在宣告任務完成前，必須逐項確認：

### Code Quality

- [ ] 執行 `python3 -m flake8 src --select=E9,F63,F7,F82 --count`，確認 0 error
- [ ] 執行 `make test` 或 `python -m pytest tests/`，確認所有測試通過
- [ ] 測試覆蓋率 > 80% (特別是核心解析和業務邏輯)
- [ ] 代碼符合 Clean Code 原則 (命名、方法長度、職責分離)
- [ ] 遵循 PEP 8 規範

### Extension Architecture

- [ ] `ResolverImpl` 正確實現所有必要的 gRPC 方法
- [ ] ID encoding/decoding 使用 `salt.encode()` 和 `salt.decode()`
- [ ] 所有異步操作正確使用 `asyncio`
- [ ] HTTP 請求通過 `Requester` 類處理
- [ ] 錯誤處理完善，有意義的日誌記錄

### Testing

- [ ] 核心解析邏輯有單元測試
- [ ] Mock 了外部依賴 (HTTP 請求)
- [ ] 測試覆蓋各種邊界情況和錯誤情況
- [ ] 測試命名清晰描述測試場景

### Documentation

- [ ] `README.md` 記錄開發環境要求
- [ ] `requirements.txt` 所有依賴都固定版本 (`===`)
- [ ] 更新 `extensions.json` (如果添加新擴展)
- [ ] 複雜邏輯有適當註解說明「為什麼」

### Version Control (功能開發任務)

- [ ] 已執行 git commit (使用指定 author)
- [ ] Commit message 清楚描述變更內容
- [ ] Commit message 遵循 Conventional Commits 格式
- [ ] Commit message 包含標題與詳細內文說明

### AI Self-Audit (修復任務)

- [ ] **是否避開了 Token 陷阱？** 確認沒有重複建議已嘗試過的方案
- [ ] **環境因素確認？** 若涉及連線或異步問題，是否已確認非執行緒阻塞引起
- [ ] **透明度報告：** 是否已向使用者說明目前的診斷假設

## Important Context

- Extensions run as gRPC servers (default port: 55001 for komica)
- Server configured with single ThreadPoolExecutor worker
- SSL verification disabled in HTTP client (`verify_ssl=False`) for certain target sites
- All timestamps use Unix epoch integers
- Extensions are dynamically loaded by the main app's sidecar service using Python's `importlib`
- The main app is built using [flet-dev/serious-python](https://github.com/flet-dev/serious-python) to package Python code into Flutter app
- Main project repository: `../news_hub_ai`
