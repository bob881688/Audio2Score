# 📚 文件導覽

這個目錄包含了 Audio2Score Backend 的所有文件。以下是快速導覽：

## 🎯 快速開始

### 新手？從這裡開始！
1. **PROJECT_SUMMARY.md** - 📖 專案總覽（必讀！）
2. **QUICKSTART.md** - 🚀 5 分鐘快速啟動
3. **README.md** - 📚 完整技術文檔

### 要部署？看這裡！
4. **DEPLOYMENT_GUIDE.md** - 🌐 詳細部署指南

## 📁 核心檔案

### 應用程式
- **main.py** - FastAPI 主程式
- **requirements.txt** - Python 依賴套件
- **.env** - 環境變數 (本地開發)
- **.env.example** - 環境變數範本

### 部署配置
- **Procfile** - Render 啟動命令
- **runtime.txt** - Python 版本指定
- **.gitignore** - Git 忽略檔案

### 工具腳本
- **start.bat** - Windows 快速啟動
- **test_api.py** - 完整 API 測試
- **check.py** - 健康檢查

## 📂 目錄結構

### app/ - 應用程式套件
```
app/
├── config.py          # 設定管理
├── database.py        # 資料庫連接
├── models.py          # 資料模型
├── schemas.py         # API schemas
├── auth.py            # 認證邏輯
├── routes/            # API 路由
│   ├── auth.py        # 認證端點
│   └── midi.py        # MIDI 端點
└── services/          # 業務邏輯
    └── audio_converter.py  # 音訊轉換
```

### uploads/ - 暫存檔案
- 上傳的音訊檔案
- 轉換的 MIDI 檔案
- (自動清理)

## 📖 文檔說明

### 1. PROJECT_SUMMARY.md
**最重要的文件！** 包含：
- ✅ 完成功能列表
- 📁 完整專案結構
- 🎯 API 端點速查
- 🗄️ 資料庫架構
- 💡 開發提示

**何時閱讀**: 第一次了解專案

### 2. QUICKSTART.md
**快速上手指南**，包含：
- 🚀 本地開發步驟
- 📝 快速測試命令
- 🛠️ 開發工具推薦
- 🔧 常見問題解決

**何時閱讀**: 準備開始開發

### 3. README.md
**完整技術文檔**，包含：
- 📖 功能介紹
- 🏗️ 技術架構
- 📚 API 詳細說明
- 🧪 測試方法
- 🔒 安全建議

**何時閱讀**: 需要深入了解

### 4. DEPLOYMENT_GUIDE.md
**部署完整指南**，包含：
- 📋 逐步部署說明（附截圖說明）
- ⚙️ 環境變數配置
- 🐛 故障排除方案
- 💰 成本分析
- 📊 監控建議

**何時閱讀**: 準備部署到 Render

## 🎓 學習路徑

### 第一天：了解專案
1. 閱讀 `PROJECT_SUMMARY.md`
2. 查看專案結構
3. 理解 API 端點

### 第二天：本地開發
1. 閱讀 `QUICKSTART.md`
2. 安裝依賴
3. 啟動服務器
4. 測試 API

### 第三天：深入學習
1. 閱讀 `README.md`
2. 了解認證流程
3. 理解音訊轉換
4. 測試所有功能

### 第四天：部署上線
1. 閱讀 `DEPLOYMENT_GUIDE.md`
2. 創建 Render 帳號
3. 設定資料庫
4. 部署 Web Service
5. 測試線上 API

## 🔍 快速查詢

### 我想...

#### 快速啟動本地服務器
```powershell
# 方法 1
.\start.bat

# 方法 2
uvicorn main:app --reload
```

#### 測試 API
```powershell
python test_api.py http://localhost:8000
```

#### 檢查服務是否運行
```powershell
python check.py http://localhost:8000
```

#### 查看 API 文檔
打開瀏覽器: http://localhost:8000/docs

#### 部署到 Render
查看 `DEPLOYMENT_GUIDE.md`

#### 了解某個功能
查看 `README.md` 的相關章節

## 📞 需要幫助？

### 問題排查順序
1. **檢查錯誤訊息** - 終端或 Render Logs
2. **查看 QUICKSTART.md** - 故障排除章節
3. **查看 DEPLOYMENT_GUIDE.md** - 常見問題章節
4. **查看 README.md** - 故障排除章節

### 常見問題文檔位置

| 問題 | 查看文檔 | 章節 |
|------|----------|------|
| 如何安裝？ | QUICKSTART.md | 安裝章節 |
| 如何啟動？ | QUICKSTART.md | 快速啟動 |
| API 怎麼用？ | README.md | API 端點 |
| 如何部署？ | DEPLOYMENT_GUIDE.md | 完整指南 |
| 部署失敗？ | DEPLOYMENT_GUIDE.md | 故障排除 |
| 資料庫錯誤？ | DEPLOYMENT_GUIDE.md | 常見問題 |
| CORS 錯誤？ | README.md | 安全性章節 |

## 🎯 推薦閱讀順序

### 初學者
1. PROJECT_SUMMARY.md （了解專案）
2. QUICKSTART.md （開始開發）
3. 實際操作（測試 API）
4. DEPLOYMENT_GUIDE.md （部署）

### 有經驗者
1. PROJECT_SUMMARY.md （快速概覽）
2. README.md（技術細節）
3. 直接開發
4. DEPLOYMENT_GUIDE.md（需要時）

### 只想部署
1. DEPLOYMENT_GUIDE.md（完整跟隨）
2. 完成！

## 💡 提示

- 📌 所有文檔都包含目錄，可快速跳轉
- 🔍 使用 Ctrl+F 搜尋關鍵字
- 📝 建議先通讀 PROJECT_SUMMARY.md
- 🚀 QUICKSTART.md 可讓你 5 分鐘內啟動
- 📚 遇到問題先查文檔，99% 的問題都有解答

## 🎉 開始吧！

選擇適合你的文檔開始閱讀：

- 🆕 新手？→ `PROJECT_SUMMARY.md`
- 🚀 想快速開始？→ `QUICKSTART.md`
- 📚 想深入了解？→ `README.md`
- 🌐 想部署上線？→ `DEPLOYMENT_GUIDE.md`

**祝你開發順利！** 🎵
