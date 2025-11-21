# Render 部署指南 (FastAPI + Python)

完整的步驟指南，幫助你將 Audio2Score Backend 部署到 Render。

## 📋 前置要求

- GitHub 帳號
- Render 帳號（免費）
- 專案已推送到 GitHub

## 🚀 部署步驟

### 步驟 1: 準備 GitHub Repository

1. **確保所有檔案都已提交**:
```bash
cd Audio2Score-backend
git add .
git commit -m "Add FastAPI backend"
git push origin main
```

2. **確認以下檔案存在**:
   - ✅ `main.py` - FastAPI 應用程式
   - ✅ `requirements.txt` - Python 依賴
   - ✅ `Procfile` - Render 啟動命令
   - ✅ `runtime.txt` - Python 版本
   - ✅ `.env.example` - 環境變數範本

---

### 步驟 2: 在 Render 創建 PostgreSQL 資料庫

1. 前往 [Render Dashboard](https://dashboard.render.com/)

2. 點擊 **"New +"** → **"PostgreSQL"**

3. **設定資料庫**:
   ```
   Name: audio2score-db
   Database: audio2score
   User: (自動生成)
   Region: Singapore (或離你最近的)
   PostgreSQL Version: 15
   Plan: Free
   ```

4. 點擊 **"Create Database"**

5. **等待資料庫創建完成** (約 1-2 分鐘)

6. **複製連接字串**:
   - 找到 **"Internal Database URL"**
   - 格式類似: `postgresql://user:pass@dpg-xxxxx/audio2score`
   - **重要**: 使用 Internal URL，不是 External

![Database URL](https://i.imgur.com/example.png)

---

### 步驟 3: 創建 Web Service

1. 回到 Dashboard，點擊 **"New +"** → **"Web Service"**

2. **選擇部署方式**:
   - 選擇 **"Build and deploy from a Git repository"**
   - 點擊 **"Next"**

3. **連接 GitHub**:
   - 如果第一次使用，需要授權 Render 訪問 GitHub
   - 選擇你的 repository
   - 如果找不到，點擊 **"Configure account"** 給予權限

4. **基本設定**:
   ```
   Name: audio2score-backend
   Region: Singapore (與資料庫相同)
   Branch: main
   Root Directory: Audio2Score-backend (如果在子目錄)
   ```

5. **環境設定**:
   ```
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

6. **進階設定** (可選):
   ```
   Auto-Deploy: Yes (推薦，代碼更新時自動部署)
   ```

---

### 步驟 4: 設定環境變數 ⚙️

在 **"Environment"** 區段添加以下變數:

#### 必要變數:

1. **DATABASE_URL** 🔗
   - Value: 貼上步驟 2 複製的 Internal Database URL
   - 範例: `postgresql://user:pass@dpg-xxxxx/audio2score`

2. **SECRET_KEY** 🔐
   - 生成方式 (在終端執行):
   ```python
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   - 或使用線上工具: https://www.uuidgenerator.net/
   - Value: 你生成的隨機字串（至少 32 字元）

3. **ALGORITHM** 🔒
   - Value: `HS256`

4. **ACCESS_TOKEN_EXPIRE_MINUTES** ⏱️
   - Value: `10080` (7 天)

5. **NODE_ENV** 🌍
   - Value: `production`

6. **ALLOWED_ORIGINS** 🌐
   - Value: `*` (開發階段)
   - 生產環境應改為具體的 URL

#### 環境變數總覽:
```
DATABASE_URL = postgresql://user:pass@dpg-xxxxx/audio2score
SECRET_KEY = your_generated_random_secret_key_here
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 10080
NODE_ENV = production
ALLOWED_ORIGINS = *
```

---

### 步驟 5: 開始部署 🎉

1. 檢查所有設定
2. 點擊 **"Create Web Service"**
3. Render 開始建置和部署 (第一次約 5-10 分鐘)

#### 部署過程:
```
📦 Cloning repository...
🔧 Installing dependencies...
📚 Installing TensorFlow...
🎵 Installing Basic Pitch...
✅ Build completed
🚀 Starting server...
```

4. **監控 Logs**:
   - 點擊 **"Logs"** 標籤查看即時日誌
   - 確認看到: `🚀 Starting Audio2Score Backend API...`

---

### 步驟 6: 測試部署 🧪

1. **取得服務 URL**:
   - 在 Dashboard 頂部找到你的 URL
   - 格式: `https://audio2score-backend.onrender.com`

2. **測試健康檢查**:
   ```bash
   curl https://audio2score-backend.onrender.com/
   ```
   
   預期回應:
   ```json
   {
     "message": "Audio2Score Backend API",
     "version": "1.0.0",
     "status": "running",
     "framework": "FastAPI"
   }
   ```

3. **查看 API 文檔**:
   - Swagger UI: `https://audio2score-backend.onrender.com/docs`
   - ReDoc: `https://audio2score-backend.onrender.com/redoc`

4. **測試註冊 API**:
   ```bash
   curl -X POST https://audio2score-backend.onrender.com/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "password": "password123"
     }'
   ```

5. **使用測試腳本**:
   ```bash
   python test_api.py https://audio2score-backend.onrender.com
   ```

---

### 步驟 7: 更新前端設定 📱

在你的前端專案 `Audio2Score/.env` 檔案中:

```env
EXPO_PUBLIC_API_URL=https://audio2score-backend.onrender.com/api
```

**重要**: 不要在 URL 最後加 `/`

---

## 🔍 驗證清單

部署完成後，確認以下項目:

- [ ] ✅ 健康檢查端點正常 (`/`)
- [ ] ✅ API 文檔可訪問 (`/docs`)
- [ ] ✅ 可以註冊新用戶
- [ ] ✅ 可以登入
- [ ] ✅ 可以獲取用戶資訊
- [ ] ✅ 資料庫連接正常
- [ ] ✅ 前端可以連接到 API

---

## 🐛 常見問題排解

### 1. Build 失敗 - TensorFlow 安裝錯誤

**錯誤訊息**:
```
ERROR: Could not find a version that satisfies the requirement tensorflow
```

**解決方法**:
```bash
# 在 requirements.txt 中使用較舊版本
tensorflow==2.13.0
```

或使用 CPU 版本:
```bash
tensorflow-cpu==2.13.0
```

---

### 2. 資料庫連接失敗

**錯誤訊息**:
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**檢查項目**:
1. ✅ 使用 **Internal Database URL**，不是 External
2. ✅ DATABASE_URL 格式正確
3. ✅ 資料庫和 Web Service 在同一區域
4. ✅ 資料庫狀態為 "Available"

**正確的 URL 格式**:
```
postgresql://user:password@hostname/database
```

---

### 3. 服務啟動後無回應

**可能原因**:
- Port 設定錯誤
- Start Command 錯誤

**檢查 Logs**:
```bash
# 應該看到
✅ Connected to PostgreSQL database
✅ Database tables created/verified
🚀 Starting Audio2Score Backend API...
```

**確認 Start Command**:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**注意**: 必須使用 `$PORT` 環境變數，Render 會自動設定

---

### 4. CORS 錯誤

**錯誤訊息** (前端):
```
Access to fetch has been blocked by CORS policy
```

**解決方法**:

1. **開發階段**: 使用 `*`
   ```env
   ALLOWED_ORIGINS=*
   ```

2. **生產環境**: 指定具體域名
   ```env
   ALLOWED_ORIGINS=https://your-frontend.com,exp://192.168.1.1:19000
   ```

3. **多個來源**:
   ```env
   ALLOWED_ORIGINS=http://localhost:19006,https://app.com,exp://192.168.1.1:19000
   ```

---

### 5. 音檔轉換失敗

**錯誤訊息**:
```
Failed to convert audio to MIDI
```

**可能原因**:
- Memory 不足 (Free plan 512MB)
- 音檔太大
- Basic Pitch 未正確安裝

**解決方法**:
1. 升級到付費方案 (更多記憶體)
2. 限制上傳檔案大小
3. 檢查 Build Logs 確認 basic-pitch 已安裝

---

### 6. 服務休眠 (Free Plan)

**現象**:
- 15 分鐘不活動後，服務會休眠
- 第一次請求需要 30-60 秒喚醒

**解決方法**:
1. **升級到付費方案** ($7/月)
2. **使用 Cron Job 定期 ping**:
   - 使用 Render Cron Jobs
   - 或使用外部服務 (UptimeRobot, Cron-job.org)
   - 每 10 分鐘 ping 一次: `curl https://your-app.onrender.com/health`

---

## 📊 監控和維護

### 查看日誌
1. Dashboard → 選擇服務 → **"Logs"** 標籤
2. 即時查看請求和錯誤
3. 搜尋特定錯誤訊息

### 查看效能指標
1. Dashboard → 選擇服務 → **"Metrics"** 標籤
2. 查看:
   - CPU 使用率
   - Memory 使用率
   - 請求數量
   - 回應時間

### 手動重新部署
1. Dashboard → 選擇服務
2. 點擊 **"Manual Deploy"** → **"Deploy latest commit"**

---

## 💰 成本分析

### Free Plan (免費方案)
```
PostgreSQL:
  - 1GB 儲存空間
  - 有效期 90 天後刪除
  - 連接數限制

Web Service:
  - 512MB RAM
  - 每月 750 小時
  - 15 分鐘後休眠
  - 共享 CPU

總成本: $0/月
```

### 推薦的付費方案
```
PostgreSQL Standard:
  - 10GB 儲存
  - 持久化資料
  - $7/月

Web Service Starter:
  - 512MB RAM
  - 不休眠
  - $7/月

總成本: $14/月
```

### 升級時機
當你遇到以下情況時考慮升級:
- ⚠️ 服務經常休眠影響用戶體驗
- ⚠️ 記憶體不足導致轉換失敗
- ⚠️ 資料庫 90 天期限即將到期
- ⚠️ 需要更好的效能

---

## 🔒 安全性建議

### 1. 更新 SECRET_KEY
```python
# 生成強密鑰
import secrets
print(secrets.token_urlsafe(32))
```

### 2. 設定 CORS
生產環境不要使用 `*`:
```env
ALLOWED_ORIGINS=https://your-app.com
```

### 3. 限制檔案大小
在 `app/routes/midi.py` 添加:
```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

### 4. Rate Limiting
考慮使用 `slowapi`:
```python
pip install slowapi
```

### 5. 定期更新依賴
```bash
pip list --outdated
pip install --upgrade package_name
```

---

## 📚 其他資源

- [Render 官方文檔](https://render.com/docs)
- [FastAPI 文檔](https://fastapi.tiangolo.com/)
- [Basic Pitch GitHub](https://github.com/spotify/basic-pitch)
- [PostgreSQL 最佳實踐](https://www.postgresql.org/docs/)

---

## ✅ 完成！

你的 Backend 現在已經成功部署到 Render！

**下一步**:
1. 📱 更新前端 `.env` 檔案
2. 🧪 測試所有 API 端點
3. 📊 監控服務狀態
4. 🎉 開始使用 Audio2Score！

如有問題，檢查 Render Logs 或參考上面的故障排除指南。
