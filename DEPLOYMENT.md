# Deployment Guide for Sentiment Analysis API

This guide covers deploying the FastAPI backend separately from your React portfolio.

## Prerequisites

- Python 3.10 (matches Dockerfile)
- Docker (optional, for containerized deployment)
- Git repository with your code

## Environment Variables

Set these in your hosting platform:

- `FRONTEND_URL`: Your React portfolio URL (e.g., `https://your-portfolio.vercel.app`)
- `PORT`: Usually set automatically by the platform

## Deployment Options

### Option 1: Railway (Recommended - Easiest)

1. **Sign up** at [railway.app](https://railway.app)
2. **Create New Project** → "Deploy from GitHub repo"
3. **Select your repository**
4. Railway will automatically detect the Dockerfile
5. **Add Environment Variable**:
   - Key: `FRONTEND_URL`
   - Value: `https://your-portfolio.vercel.app`
6. **Deploy** - Railway will build and deploy automatically
7. **Get your API URL** from the Railway dashboard (e.g., `https://your-api.up.railway.app`)

**Pros**: 
- Automatic deployments from GitHub
- Free tier available
- Easy to use

### Option 2: Render

1. **Sign up** at [render.com](https://render.com)
2. **New** → **Web Service**
3. **Connect your GitHub repository**
4. **Configure**:
   - **Name**: `sentiment-analysis-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. **Add Environment Variable**:
   - `FRONTEND_URL`: `https://your-portfolio.vercel.app`
6. **Deploy**

**Pros**: 
- Free tier available
- Simple configuration

### Option 3: Fly.io

1. **Install Fly CLI**: `curl -L https://fly.io/install.sh | sh`
2. **Login**: `fly auth login`
3. **Launch**: `fly launch` (follow prompts)
4. **Set environment variable**: 
   ```bash
   fly secrets set FRONTEND_URL=https://your-portfolio.vercel.app
   ```
5. **Deploy**: `fly deploy`

**Pros**: 
- Global edge deployment
- Good performance

### Option 4: DigitalOcean App Platform

1. **Sign up** at [digitalocean.com](https://digitalocean.com)
2. **Create** → **App** → **GitHub**
3. **Select repository**
4. **Configure**:
   - **Type**: Web Service
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. **Add Environment Variable**: `FRONTEND_URL`
6. **Deploy**

## Testing Your Deployment

Once deployed, test your API:

```bash
# Test health endpoint
curl https://your-api-url.com/

# Test prediction endpoint
curl -X POST https://your-api-url.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

Expected response:
```json
{
  "text": "I love this product!",
  "sentiment": "Positive",
  "model_version": "v1.0"
}
```

## Connecting to Your React Portfolio

In your React app, create an API utility:

```javascript
// utils/sentimentAPI.js
const API_URL = process.env.REACT_APP_API_URL || 'https://your-api-url.com';

export const analyzeSentiment = async (text) => {
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error analyzing sentiment:', error);
    throw error;
  }
};
```

Add to your `.env` file in React project:
```
REACT_APP_API_URL=https://your-api-url.com
```

## Troubleshooting

### CORS Issues
- Make sure `FRONTEND_URL` environment variable is set correctly
- Check that your React app URL matches the allowed origins in `api.py`

### Model File Not Found
- Ensure `sentiment_model.pkl` is committed to your Git repository
- Verify it's in the root directory (same level as `api.py`)

### Port Issues
- Most platforms set `PORT` automatically
- If using Dockerfile, ensure it exposes port 8000
- Update start command to use `$PORT` environment variable

### Version Mismatches
- Python 3.10 is required (matches Dockerfile)
- scikit-learn==1.7.1 (matches Dockerfile)
- Check `requirements.txt` for exact versions


