# News Hub Extensions Repository

> 官方擴充功能倉庫 - 為 News Hub 提供多樣化的論壇支援

這是 [News Hub](https://github.com/twkevinzhang/news_hub) 的官方擴充功能倉庫。透過安裝擴充功能,您可以在 News Hub 中瀏覽不同的論壇網站,無需等待 App 更新。

> [!NOTE] > **開發者請注意**: 如果您想要開發自己的擴充功能,請參閱 [Extension Development Guide](./docs/EXTENSION_DEVELOPMENT.md)

---

## 📦 可用擴充功能

| 擴充功能名稱   | 版本 | 語言     | 分級   | 說明                        |
| -------------- | ---- | -------- | ------ | --------------------------- |
| Mock Extension | v1   | 繁體中文 | 全年齡 | 測試用擴充功能,提供模擬資料 |

### Mock Extension

**套件名稱**: `twkevinzhang_mock`

這是一個測試用擴充功能,主要用於:

- 開發階段的功能測試
- UI/UX 原型驗證
- 提供模擬資料以便進行 App 開發

> [!WARNING]
> 此擴充功能僅供開發測試使用,不會連接到真實的論壇網站。

---

## 🚀 如何使用

### 1. 安裝 News Hub App

如果您尚未安裝 News Hub,請前往 [News Hub Releases](https://github.com/twkevinzhang/news_hub/releases) 下載最新版本。

詳細的安裝步驟請參考 [News Hub README - Quick Start](https://github.com/twkevinzhang/news_hub#-quick-start) 段落。

### 2. 新增擴充功能倉庫

1. 開啟 News Hub App
2. 點擊 **設定 → Repo & Extensions**
3. 點擊「新增倉庫」按鈕
4. 輸入倉庫 URL:
   ```
   https://github.com/twkevinzhang/news_hub_extensions
   ```
5. 點擊「確認」

### 3. 安裝擴充功能

1. 在 **Repo & Extensions** 頁面中,找到您想要的擴充功能
2. 點擊「安裝」按鈕
3. 等待下載與安裝完成
4. 安裝完成後,該擴充功能的論壇板塊將可在「建立收藏」中使用

### 4. 建立收藏並開始瀏覽

1. 開啟導航抽屜(側邊選單)
2. 點擊「建立收藏」
3. 從已安裝的擴充功能中選擇您想要的論壇板塊
4. 開始瀏覽!

> [!TIP]
> 您可以在一個收藏中混合不同擴充功能的板塊,打造個人化的閱讀體驗。

---

## ❓ 常見問題 (FAQ)

### Q1: 擴充功能會自動更新嗎?

A: 目前需要手動檢查更新。未來版本將支援自動更新通知。

### Q2: 我可以同時安裝多個倉庫的擴充功能嗎?

A: 可以!您可以新增多個擴充功能倉庫,並從不同來源安裝擴充功能。

### Q3: 擴充功能安全嗎?

A: 官方倉庫中的擴充功能都經過審核。如果您要安裝第三方倉庫的擴充功能,請確認來源可信。

### Q4: 為什麼我安裝的擴充功能無法使用?

A: 請檢查:

- News Hub App 版本是否為最新版本
- Sidecar 服務是否正常運行(可在設定中查看狀態)
- 擴充功能是否與您的 Python 版本相容(需要 Python 3.8+)

### Q5: 如何回報擴充功能的問題?

A: 請在本倉庫的 [Issues](https://github.com/twkevinzhang/news_hub_extensions/issues) 頁面回報,並提供:

- 擴充功能名稱與版本
- News Hub App 版本
- 錯誤訊息或截圖
- 重現步驟

---

## 🧩 開發自己的擴充功能

想要為您喜愛的論壇建立擴充功能嗎?

📖 **[Extension Development Guide](./docs/EXTENSION_DEVELOPMENT.md)** - 完整的開發指南

您將學習到:

- 擴充功能架構與運作原理
- 如何使用 Python 撰寫爬蟲邏輯
- Protobuf 定義與 gRPC 通訊
- 依賴管理與打包規範
- 測試與除錯技巧

---

## 📝 授權條款

MIT License

---

## 🙏 致謝

感謝所有為 News Hub 生態系統貢獻擴充功能的開發者!

**Made with ❤️ by the News Hub community**
