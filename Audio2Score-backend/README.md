# Audio2Score Backend

Backend API for the Audio2Score mobile application. Provides user authentication, audio-to-MIDI conversion using Basic Pitch, and MIDI file storage in PostgreSQL.

## Features

- 🔐 User authentication (register/login with JWT)
- 🎵 Audio to MIDI conversion using Spotify's Basic Pitch
- 💾 PostgreSQL database for storing MIDI files
- 📚 User library management
- 🚀 Ready for Render deployment

## Tech Stack

- **Runtime**: Node.js (v18+)
- **Framework**: Express.js
- **Database**: PostgreSQL
- **Authentication**: JWT + bcrypt
- **Audio Processing**: Basic Pitch
- **File Upload**: Multer

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info (protected)

### MIDI Operations
- `POST /api/midi/upload` - Upload audio and convert to MIDI (protected)
- `GET /api/midi/library` - Get user's MIDI library (protected)
- `GET /api/midi/:id` - Get specific MIDI file (protected)
- `GET /api/midi/:id/download` - Download MIDI file (protected)
- `DELETE /api/midi/:id` - Delete MIDI file (protected)

## Setup

### Prerequisites

1. Node.js 18+ and npm
2. PostgreSQL database
3. Python 3.8+ (for Basic Pitch)

### Installation

1. Install Node.js dependencies:
```bash
npm install
```

2. Install Basic Pitch (Python):
```bash
pip install basic-pitch
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Edit `.env` with your configuration:
```env
DATABASE_URL=postgresql://user:password@host:5432/database
JWT_SECRET=your_super_secret_jwt_key
PORT=3000
NODE_ENV=production
ALLOWED_ORIGINS=*
```

5. Run database migration:
```bash
npm run migrate
```

6. Start the server:
```bash
# Development
npm run dev

# Production
npm start
```

## Deployment on Render

### Step 1: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: `audio2score-db`
   - Database: `audio2score`
   - User: (auto-generated)
   - Region: Choose closest to you
   - Plan: Free or paid
4. Click "Create Database"
5. Copy the "Internal Database URL" for later

### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - Name: `audio2score-backend`
   - Environment: `Node`
   - Region: Same as database
   - Branch: `main` or your default branch
   - Build Command: `npm install && pip install basic-pitch`
   - Start Command: `npm start`

### Step 3: Add Environment Variables

In the "Environment" section, add:

```
DATABASE_URL=<your_internal_database_url>
JWT_SECRET=<generate_a_random_secret>
NODE_ENV=production
PORT=10000
ALLOWED_ORIGINS=*
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait for deployment to complete
3. Once deployed, run migration:
   - Go to "Shell" tab
   - Run: `npm run migrate`

### Step 5: Update Frontend

Update your frontend `.env` file with the Render URL:
```
EXPO_PUBLIC_API_URL=https://audio2score-backend.onrender.com/api
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### MIDI Files Table
```sql
CREATE TABLE midi_files (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  filename VARCHAR(255) NOT NULL,
  original_filename VARCHAR(255) NOT NULL,
  midi_data BYTEA NOT NULL,
  duration FLOAT,
  note_count INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Usage Examples

### Register User
```bash
curl -X POST https://your-app.onrender.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Login
```bash
curl -X POST https://your-app.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### Upload Audio
```bash
curl -X POST https://your-app.onrender.com/api/midi/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "audio=@/path/to/audio.mp3"
```

### Get Library
```bash
curl https://your-app.onrender.com/api/midi/library \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Troubleshooting

### Basic Pitch Installation Issues

If you encounter issues with Basic Pitch on Render:

1. Add a `requirements.txt` file:
```
basic-pitch>=0.2.0
tensorflow>=2.9.0
```

2. Update Build Command:
```bash
npm install && pip install -r requirements.txt
```

### Database Connection Issues

- Ensure `DATABASE_URL` uses the Internal Database URL from Render
- Check that SSL is enabled for production

### Memory Issues

- Upgrade to a paid Render plan for more memory
- Consider processing audio files asynchronously with a job queue

## License

MIT
