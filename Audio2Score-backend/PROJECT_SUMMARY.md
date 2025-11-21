# 🎵 Audio2Score Backend - 專案總結

## ✅ 完成項目

我已經為你建立了一個完整的 **Python FastAPI Backend**，包含以下功能：

### 🔐 認證系統
- ✅ 用戶註冊 (username, email, password)
- ✅ 用戶登入 (JWT token)
- ✅ 密碼加密 (bcrypt)
- ✅ Token 驗證中間件
- ✅ 獲取當前用戶資訊

### 🎵 音訊轉 MIDI
- ✅ 上傳音檔 (MP3, WAV)
- ✅ 使用 Basic Pitch 轉換為 MIDI
- ✅ 分析 MIDI (音符數量)
- ✅ 儲存到 PostgreSQL (BYTEA 格式)

### 📚 MIDI 管理
- ✅ 獲取用戶的 MIDI 列表
- ✅ 獲取單個 MIDI 檔案 (Base64 編碼)
- ✅ 下載 MIDI 檔案
- ✅ 刪除 MIDI 檔案

### 💾 資料庫
- ✅ PostgreSQL 整合
- ✅ SQLAlchemy ORM
- ✅ 自動建表
- ✅ 關聯式資料 (User ↔ MidiFiles)

### 🚀 部署就緒
- ✅ Render 部署配置
- ✅ 環境變數管理
- ✅ CORS 設定
- ✅ 生產環境優化

---

## 📁 檔案結構

```
Audio2Score-backend/
├── 📄 main.py                      # FastAPI 應用主程式
├── 📄 requirements.txt             # Python 依賴套件
├── 📄 .env                         # 環境變數 (本地)
├── 📄 .env.example                 # 環境變數範本
├── 📄 .gitignore                   # Git 忽略檔案
├── 📄 Procfile                     # Render 啟動命令
├── 📄 runtime.txt                  # Python 版本
├── 📄 README.md                    # 完整文檔
├── 📄 DEPLOYMENT_GUIDE.md          # 詳細部署指南
├── 📄 QUICKSTART.md                # 快速開始
├── 📄 start.bat                    # Windows 啟動腳本
├── 📄 test_api.py                  # API 測試腳本
│
├── 📂 app/                         # 應用程式套件
│   ├── __init__.py
│   ├── config.py                   # 設定檔
│   ├── database.py                 # 資料庫連接
│   ├── models.py                   # 資料庫模型
│   ├── schemas.py                  # Pydantic schemas
│   ├── auth.py                     # 認證邏輯
│   │
│   ├── 📂 routes/                  # API 路由
│   │   ├── __init__.py
│   │   ├── auth.py                 # 認證 API
│   │   └── midi.py                 # MIDI API
│   │
│   └── 📂 services/                # 業務邏輯
│       ├── __init__.py
│       └── audio_converter.py      # 音訊轉換服務
│
└── 📂 uploads/                     # 暫存檔案目錄
```

---

## 🎯 API 端點

### 認證 (Authentication)

| 方法 | 端點 | 說明 | 認證 |
|------|------|------|------|
| POST | `/api/auth/register` | 註冊新用戶 | ❌ |
| POST | `/api/auth/login` | 用戶登入 | ❌ |
| GET | `/api/auth/me` | 取得當前用戶 | ✅ |

### MIDI 操作

| 方法 | 端點 | 說明 | 認證 |
|------|------|------|------|
| POST | `/api/midi/upload` | 上傳音檔轉 MIDI | ✅ |
| GET | `/api/midi/library` | 取得 MIDI 列表 | ✅ |
| GET | `/api/midi/{id}` | 取得 MIDI 詳情 | ✅ |
| GET | `/api/midi/{id}/download` | 下載 MIDI | ✅ |
| DELETE | `/api/midi/{id}` | 刪除 MIDI | ✅ |

---

## 🗄️ 資料庫架構

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

### MIDI Files Table
```sql
CREATE TABLE midi_files (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR NOT NULL,
    original_filename VARCHAR NOT NULL,
    midi_data BYTEA NOT NULL,           -- MIDI 二進位資料
    duration FLOAT,                      -- 時長（秒）
    note_count INTEGER,                  -- 音符數量
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

---

## 🚀 快速開始

### 本地開發

1. **安裝依賴**:
```powershell
pip install -r requirements.txt
```

2. **設定環境變數** (編輯 `.env`):
```env
DATABASE_URL=postgresql://user:pass@localhost/audio2score
SECRET_KEY=your_random_secret_key
```

3. **啟動服務器**:
```powershell
# 方法 1: 使用啟動腳本
.\start.bat

# 方法 2: 手動啟動
uvicorn main:app --reload --port 8000

# 方法 3: 使用 Python
python main.py
```

4. **訪問 API**:
- 主頁: http://localhost:8000
- API 文檔: http://localhost:8000/docs
- 測試: `python test_api.py`

### Render 部署

詳細步驟請參考 `DEPLOYMENT_GUIDE.md`

**簡要步驟**:
1. 創建 PostgreSQL 資料庫
2. 創建 Web Service
3. 設定環境變數
4. 部署
5. 測試 API

---

## 🔧 技術棧

| 類別 | 技術 | 版本 |
|------|------|------|
| **框架** | FastAPI | 0.104.1 |
| **語言** | Python | 3.10+ |
| **Web 服務器** | Uvicorn | 0.24.0 |
| **資料庫** | PostgreSQL | 15 |
| **ORM** | SQLAlchemy | 2.0.23 |
| **認證** | JWT + Passlib | - |
| **音訊處理** | Basic Pitch | 0.2.5 |
| **ML 框架** | TensorFlow | 2.13.0 |
| **音訊分析** | Librosa | 0.10.1 |

---

## 📖 文檔導覽

1. **README.md** - 完整專案文檔
   - 功能介紹
   - API 說明
   - 本地開發設定
   - 測試方法

2. **DEPLOYMENT_GUIDE.md** - 詳細部署指南
   - 逐步部署說明
   - 環境變數配置
   - 故障排除
   - 成本分析

3. **QUICKSTART.md** - 快速開始
   - 5 分鐘快速啟動
   - 常用命令
   - 開發工具推薦

---

## 🧪 測試

### 自動化測試
```powershell
# 測試本地 API
python test_api.py http://localhost:8000

# 測試部署的 API
python test_api.py https://your-app.onrender.com
```

### 手動測試
```powershell
# 健康檢查
curl http://localhost:8000/

# 註冊
curl -X POST http://localhost:8000/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"test\",\"email\":\"test@test.com\",\"password\":\"test123\"}'

# 登入
curl -X POST http://localhost:8000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"test\",\"password\":\"test123\"}'
```

---

## 🌟 主要特色

### 1. 高效能
- ⚡ FastAPI 非同步處理
- 🚀 Uvicorn ASGI 服務器
- 💾 資料庫連接池

### 2. 安全性
- 🔐 JWT Token 認證
- 🔒 Bcrypt 密碼加密
- 🛡️ CORS 保護
- ✅ Pydantic 輸入驗證

### 3. 可擴展性
- 📦 模組化設計
- 🎯 清晰的專案結構
- 📚 完整的文檔
- 🧪 測試腳本

### 4. 開發友好
- 📖 自動生成 API 文檔 (Swagger UI)
- 🔄 熱重載 (開發模式)
- 🐛 詳細的錯誤訊息
- 💡 型別提示

---

## 📝 環境變數說明

| 變數名 | 必要 | 預設值 | 說明 |
|--------|------|--------|------|
| `DATABASE_URL` | ✅ | - | PostgreSQL 連接字串 |
| `SECRET_KEY` | ✅ | - | JWT 密鑰 (32+ 字元) |
| `ALGORITHM` | ❌ | HS256 | JWT 演算法 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | ❌ | 10080 | Token 有效期 (分鐘) |
| `PORT` | ❌ | 8000 | 服務器端口 |
| `NODE_ENV` | ❌ | development | 環境 (development/production) |
| `ALLOWED_ORIGINS` | ❌ | * | CORS 允許的來源 |

---

## 🎓 下一步建議

### 短期 (1-2 週)
- [ ] 完成本地開發測試
- [ ] 部署到 Render
- [ ] 整合前端應用
- [ ] 基本功能測試

### 中期 (1-2 個月)
- [ ] 添加 Rate Limiting
- [ ] 實作檔案大小限制
- [ ] 優化音訊轉換效能
- [ ] 添加更多 MIDI 分析功能

### 長期 (3-6 個月)
- [ ] 添加音訊預覽功能
- [ ] 實作批次處理
- [ ] 添加 WebSocket 支援 (即時進度)
- [ ] 實作快取機制
- [ ] 添加 CDN 支援

---

## 🤝 與前端整合

### 前端設定
在 `Audio2Score/.env`:
```env
EXPO_PUBLIC_API_URL=https://your-backend.onrender.com/api
```

### 前端範例 (React Native / Expo)
```typescript
// authService.ts
const API_URL = process.env.EXPO_PUBLIC_API_URL;

export const register = async (username, email, password) => {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password })
  });
  return response.json();
};

export const login = async (username, password) => {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  return response.json();
};

// midiService.ts
export const uploadAudio = async (audioUri, token) => {
  const formData = new FormData();
  formData.append('audio', {
    uri: audioUri,
    type: 'audio/mpeg',
    name: 'audio.mp3'
  });

  const response = await fetch(`${API_URL}/midi/upload`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  return response.json();
};

export const getLibrary = async (token) => {
  const response = await fetch(`${API_URL}/midi/library`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.json();
};
```

---

## 💡 提示和技巧

### 開發環境
1. **使用虛擬環境**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **查看即時日誌**:
   ```powershell
   uvicorn main:app --reload --log-level debug
   ```

3. **使用 SQLite 測試** (不需要 PostgreSQL):
   ```python
   # .env
   DATABASE_URL=sqlite:///./test.db
   ```

### 生產環境
1. **使用強密鑰**:
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

2. **設定 CORS**:
   ```env
   ALLOWED_ORIGINS=https://your-app.com,https://another-app.com
   ```

3. **監控日誌**:
   - Render Dashboard → Logs
   - 查找錯誤和效能問題

---

## 📞 支援

遇到問題？

1. **查看文檔**:
   - README.md
   - DEPLOYMENT_GUIDE.md
   - QUICKSTART.md

2. **檢查日誌**:
   ```powershell
   # 本地
   查看終端輸出

   # Render
   Dashboard → Logs
   ```

3. **常見問題**:
   - TensorFlow 安裝慢 → 使用 tensorflow-cpu
   - 資料庫連接失敗 → 檢查 DATABASE_URL
   - CORS 錯誤 → 設定 ALLOWED_ORIGINS

---

## ✨ 總結

你現在擁有一個:
- ✅ 功能完整的 FastAPI Backend
- ✅ 用戶認證系統
- ✅ 音訊轉 MIDI 功能
- ✅ PostgreSQL 資料庫整合
- ✅ Render 部署配置
- ✅ 完整的文檔和測試

**準備好部署了嗎？**
👉 查看 `DEPLOYMENT_GUIDE.md` 開始部署！

**需要快速測試？**
👉 執行 `.\start.bat` 或查看 `QUICKSTART.md`！

---

**祝你開發順利！** 🎉
