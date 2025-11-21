# Render 部署指南

## 步驟 1: 準備 GitHub Repository

1. 確保你的 backend 代碼已經推送到 GitHub
2. 確保包含以下檔案：
   - `package.json`
   - `src/index.js`
   - `requirements.txt` (Python 依賴)
   - `.gitignore`

## 步驟 2: 在 Render 創建 PostgreSQL 資料庫

1. 前往 [Render Dashboard](https://dashboard.render.com/)
2. 點擊 **"New +"** → **"PostgreSQL"**
3. 設定：
   - **Name**: `audio2score-db`
   - **Database**: `audio2score` (可選，會自動生成)
   - **User**: (自動生成)
   - **Region**: 選擇離你最近的區域
   - **PostgreSQL Version**: 15 或最新版本
   - **Plan**: 選擇 **Free** (或付費方案)
4. 點擊 **"Create Database"**
5. 等待資料庫創建完成
6. 複製 **"Internal Database URL"** (格式如: `postgresql://user:pass@host/db`)

## 步驟 3: 創建 Web Service

1. 回到 Dashboard，點擊 **"New +"** → **"Web Service"**
2. 選擇 **"Build and deploy from a Git repository"**
3. 連接你的 GitHub 帳號並選擇你的 repository
4. 設定：

### Basic Settings
- **Name**: `audio2score-backend`
- **Region**: 與資料庫相同的區域
- **Branch**: `main` (或你的預設分支)
- **Root Directory**: 如果 backend 在子目錄，填入路徑（例如：`Audio2Score-backend`）
- **Environment**: `Node`
- **Build Command**: 
  ```bash
  npm install && pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  npm start
  ```

### Advanced Settings
- **Auto-Deploy**: Yes (推薦)

## 步驟 4: 設定環境變數

在 **"Environment"** 區段，添加以下變數：

1. `DATABASE_URL`
   - Value: 貼上你在步驟 2 複製的 Internal Database URL
   
2. `JWT_SECRET`
   - Value: 生成一個隨機字串（例如：使用 [這個工具](https://www.uuidgenerator.net/)）
   - 範例: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6`

3. `NODE_ENV`
   - Value: `production`

4. `PORT`
   - Value: `10000` (Render 預設)

5. `ALLOWED_ORIGINS`
   - Value: `*` (或指定你的前端 URL)

## 步驟 5: 部署

1. 點擊 **"Create Web Service"**
2. 等待部署完成（第一次可能需要 5-10 分鐘）
3. 檢查 **"Logs"** 確認沒有錯誤

## 步驟 6: 執行資料庫 Migration

部署完成後，需要初始化資料庫：

1. 在 Render Dashboard 中，找到你的 `audio2score-backend` service
2. 點擊 **"Shell"** 標籤
3. 執行以下命令：
   ```bash
   npm run migrate
   ```
4. 確認看到成功訊息：
   ```
   ✅ Users table created/verified
   ✅ MIDI files table created/verified
   ✅ Indexes created/verified
   🎉 Migration completed successfully!
   ```

## 步驟 7: 測試 API

找到你的服務 URL（例如：`https://audio2score-backend.onrender.com`）

### 測試根端點
```bash
curl https://audio2score-backend.onrender.com/
```

應該返回：
```json
{
  "message": "Audio2Score Backend API",
  "version": "1.0.0",
  "status": "running"
}
```

### 測試註冊
```bash
curl -X POST https://audio2score-backend.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'
```

### 測試登入
```bash
curl -X POST https://audio2score-backend.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

## 步驟 8: 更新前端設定

在你的前端專案中更新 `.env` 檔案：

```env
EXPO_PUBLIC_API_URL=https://audio2score-backend.onrender.com/api
```

## 常見問題

### 1. Build 失敗：Python 相關錯誤

**問題**: `pip: command not found` 或 Python 套件安裝失敗

**解決方案**: 
- 確保 Build Command 包含 Python 安裝步驟
- 或者修改為：
  ```bash
  npm install && python3 -m pip install -r requirements.txt
  ```

### 2. 資料庫連接失敗

**問題**: `Connection refused` 或 `timeout`

**解決方案**:
- 確認使用 **Internal Database URL**（不是 External）
- 檢查 `DATABASE_URL` 環境變數是否正確設定

### 3. Basic Pitch 轉換失敗

**問題**: Audio 上傳後轉換失敗

**解決方案**:
- 檢查 Logs 查看詳細錯誤
- 確保 `requirements.txt` 中的依賴都已安裝
- 可能需要升級到付費方案以獲得更多記憶體

### 4. 服務休眠（Free Plan）

**問題**: Free plan 的服務在 15 分鐘不活動後會休眠

**解決方案**:
- 升級到付費方案
- 或使用外部服務定期 ping 你的 API

### 5. CORS 錯誤

**問題**: 前端無法訪問 API

**解決方案**:
- 更新 `ALLOWED_ORIGINS` 環境變數
- 包含你的前端 URL 和 Expo 開發伺服器
- 範例: `http://localhost:19006,exp://192.168.1.1:19000,https://your-app.com`

## 監控和維護

### 查看 Logs
- Dashboard → 選擇服務 → "Logs" 標籤

### 檢查效能
- Dashboard → 選擇服務 → "Metrics" 標籤

### 重新部署
- 推送代碼到 GitHub 會自動觸發重新部署
- 或在 Dashboard 手動點擊 "Manual Deploy"

## 升級建議

如果你的應用變大或需要更好的效能：

1. **資料庫**: 升級到 Standard plan ($7/月) 以獲得更好的效能
2. **Web Service**: 升級到 Starter plan ($7/月) 以避免休眠
3. **使用 CDN**: 考慮使用 Cloudflare 加速靜態資源

## 安全建議

1. **定期更新依賴**:
   ```bash
   npm update
   pip install --upgrade -r requirements.txt
   ```

2. **更改 JWT_SECRET**: 定期輪換密鑰

3. **限制 CORS**: 在生產環境不要使用 `*`，指定具體的前端域名

4. **啟用 HTTPS**: Render 自動提供，確保前端也使用 HTTPS

5. **監控**: 定期檢查 Logs 找出異常活動

## 成本估算

### Free Plan
- PostgreSQL: 1GB 儲存，有效期 90 天
- Web Service: 512MB RAM，每月 750 小時
- **總成本**: $0/月
- **限制**: 服務會休眠，資料庫 90 天後刪除

### 建議的付費方案
- PostgreSQL Standard: $7/月
- Web Service Starter: $7/月
- **總成本**: $14/月
- **優勢**: 不休眠，持久化資料庫，更好的效能

## 支援

如果遇到問題：
1. 查看 Render Logs
2. 檢查 [Render 文檔](https://render.com/docs)
3. 查看 [Render Community](https://community.render.com/)
