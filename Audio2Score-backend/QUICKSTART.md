# 快速開始指南 - Audio2Score Backend

## 🚀 本地開發快速啟動

### 1. 安裝 Python 依賴

```powershell
# 創建虛擬環境 (可選但推薦)
python -m venv venv

# 啟動虛擬環境
.\venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt
```

### 2. 設定環境變數

編輯 `.env` 檔案，至少更改以下項目：

```env
# 如果有 PostgreSQL 資料庫，更新這個
DATABASE_URL=postgresql://user:password@localhost:5432/audio2score

# 生成一個隨機密鑰
SECRET_KEY=your_random_secret_key_here
```

**生成密鑰**:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. 啟動服務器

```powershell
# 開發模式 (自動重載)
uvicorn main:app --reload --port 8000

# 或使用 Python 直接運行
python main.py
```

### 4. 測試 API

打開瀏覽器訪問:
- **主頁**: http://localhost:8000/
- **API 文檔**: http://localhost:8000/docs
- **備用文檔**: http://localhost:8000/redoc

### 5. 執行測試

```powershell
# 測試本地 API
python test_api.py http://localhost:8000

# 測試部署的 API
python test_api.py https://your-app.onrender.com
```

---

## 📝 快速測試 API

### 註冊用戶
```powershell
curl -X POST http://localhost:8000/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"test\",\"email\":\"test@test.com\",\"password\":\"test123\"}'
```

### 登入
```powershell
curl -X POST http://localhost:8000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{\"username\":\"test\",\"password\":\"test123\"}'
```

---

## 🐳 使用 Docker (可選)

創建 `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

運行:
```powershell
docker build -t audio2score-backend .
docker run -p 8000:8000 audio2score-backend
```

---

## 📚 API 端點速查

| 方法 | 端點 | 說明 | 需要認證 |
|------|------|------|----------|
| GET | `/` | 健康檢查 | ❌ |
| POST | `/api/auth/register` | 註冊 | ❌ |
| POST | `/api/auth/login` | 登入 | ❌ |
| GET | `/api/auth/me` | 取得用戶資訊 | ✅ |
| POST | `/api/midi/upload` | 上傳音檔轉 MIDI | ✅ |
| GET | `/api/midi/library` | 取得 MIDI 列表 | ✅ |
| GET | `/api/midi/{id}` | 取得 MIDI 詳情 | ✅ |
| GET | `/api/midi/{id}/download` | 下載 MIDI | ✅ |
| DELETE | `/api/midi/{id}` | 刪除 MIDI | ✅ |

---

## 🛠️ 開發工具

### VSCode 擴充套件推薦
- Python (Microsoft)
- Pylance
- Python Debugger
- REST Client

### 使用 REST Client 測試

創建 `test.http`:
```http
### Health Check
GET http://localhost:8000/

### Register
POST http://localhost:8000/api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}

### Login
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

---

## 🔧 故障排除

### 問題: ModuleNotFoundError

**解決**:
```powershell
pip install -r requirements.txt
```

### 問題: 資料庫連接失敗

**解決**:
1. 確保 PostgreSQL 正在運行
2. 檢查 `.env` 中的 `DATABASE_URL`
3. 或使用 SQLite (開發環境):
   ```python
   # 在 app/config.py 中
   database_url: str = "sqlite:///./audio2score.db"
   ```

### 問題: TensorFlow 安裝慢

**解決**: 使用 CPU 版本
```powershell
pip uninstall tensorflow
pip install tensorflow-cpu
```

---

## 📦 專案結構

```
Audio2Score-backend/
├── main.py                    # FastAPI 應用入口
├── requirements.txt           # Python 依賴
├── .env                       # 環境變數
├── Procfile                   # Render 部署
├── runtime.txt               # Python 版本
├── test_api.py               # API 測試腳本
├── app/
│   ├── __init__.py
│   ├── config.py             # 設定
│   ├── database.py           # 資料庫連接
│   ├── models.py             # SQLAlchemy 模型
│   ├── schemas.py            # Pydantic schemas
│   ├── auth.py               # 認證邏輯
│   ├── routes/
│   │   ├── auth.py           # 認證 API
│   │   └── midi.py           # MIDI API
│   └── services/
│       └── audio_converter.py # 音訊轉換
└── uploads/                  # 暫存檔案
```

---

## 🎯 下一步

1. ✅ 完成本地測試
2. 📤 推送到 GitHub
3. 🚀 部署到 Render（參考 DEPLOYMENT_GUIDE.md）
4. 📱 整合前端應用
5. 🎉 開始使用！

---

有任何問題？查看:
- `README.md` - 完整文檔
- `DEPLOYMENT_GUIDE.md` - 詳細部署指南
- `/docs` - API 互動式文檔
