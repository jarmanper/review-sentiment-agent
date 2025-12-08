# React Portfolio Integration Guide

This guide shows how to integrate the Sentiment Analysis API into your React portfolio hosted on Vercel.

## Step 1: Add API Utility Function

Create a file in your React project: `src/utils/sentimentAPI.js` (or `.ts` for TypeScript)

```javascript
// src/utils/sentimentAPI.js

// Replace with your deployed API URL
const API_URL = process.env.REACT_APP_API_URL || 'https://your-api-url.com';

/**
 * Analyzes the sentiment of a given text
 * @param {string} text - The text to analyze
 * @returns {Promise<{text: string, sentiment: string, model_version: string}>}
 */
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
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error analyzing sentiment:', error);
    throw error;
  }
};

/**
 * Checks if the API is available
 * @returns {Promise<boolean>}
 */
export const checkAPIHealth = async () => {
  try {
    const response = await fetch(`${API_URL}/`);
    return response.ok;
  } catch (error) {
    return false;
  }
};
```

## Step 2: Create React Component

Create `src/components/SentimentAnalyzer.jsx`:

```jsx
import { useState } from 'react';
import { analyzeSentiment } from '../utils/sentimentAPI';
import './SentimentAnalyzer.css'; // Optional styling

function SentimentAnalyzer() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeSentiment(text);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze sentiment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setText('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="sentiment-analyzer">
      <h2>Sentiment Analysis</h2>
      <p className="description">
        Enter text below to analyze its sentiment (Positive or Negative)
      </p>

      <div className="input-section">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to analyze..."
          rows={6}
          className="text-input"
          disabled={loading}
        />
        
        <div className="button-group">
          <button 
            onClick={handleAnalyze} 
            disabled={loading || !text.trim()}
            className="analyze-btn"
          >
            {loading ? 'Analyzing...' : 'Analyze Sentiment'}
          </button>
          {(text || result) && (
            <button 
              onClick={handleClear}
              className="clear-btn"
              disabled={loading}
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {result && (
        <div className={`result ${result.sentiment.toLowerCase()}`}>
          <div className="result-header">
            <span className="sentiment-label">{result.sentiment}</span>
            <span className="model-version">v{result.model_version}</span>
          </div>
          <div className="result-text">
            <strong>Analyzed:</strong> "{result.text}"
          </div>
        </div>
      )}
    </div>
  );
}

export default SentimentAnalyzer;
```

## Step 3: Optional Styling

Create `src/components/SentimentAnalyzer.css`:

```css
.sentiment-analyzer {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.sentiment-analyzer h2 {
  margin-top: 0;
  color: #333;
}

.description {
  color: #666;
  margin-bottom: 1.5rem;
}

.input-section {
  margin-bottom: 1.5rem;
}

.text-input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.2s;
}

.text-input:focus {
  outline: none;
  border-color: #4CAF50;
}

.text-input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.analyze-btn,
.clear-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.analyze-btn {
  background-color: #4CAF50;
  color: white;
}

.analyze-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.analyze-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.clear-btn {
  background-color: #f44336;
  color: white;
}

.clear-btn:hover:not(:disabled) {
  background-color: #da190b;
}

.error-message {
  padding: 1rem;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.result {
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.result.positive {
  background-color: #e8f5e9;
  border-left: 4px solid #4CAF50;
}

.result.negative {
  background-color: #ffebee;
  border-left: 4px solid #f44336;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.sentiment-label {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.model-version {
  font-size: 0.875rem;
  color: #666;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.result-text {
  color: #555;
  line-height: 1.6;
}
```

## Step 4: Environment Variables

Create `.env` file in your React project root:

```env
REACT_APP_API_URL=https://your-api-url.com
```

For Vercel, add this in your Vercel project settings:
- Go to Project Settings → Environment Variables
- Add `REACT_APP_API_URL` with your deployed API URL

## Step 5: Use the Component

Import and use in your portfolio:

```jsx
// src/App.jsx or wherever you want to use it
import SentimentAnalyzer from './components/SentimentAnalyzer';

function App() {
  return (
    <div className="App">
      {/* Your other portfolio content */}
      
      <section id="sentiment-analysis">
        <SentimentAnalyzer />
      </section>
      
      {/* More portfolio content */}
    </div>
  );
}
```

## Step 6: TypeScript Support (Optional)

If using TypeScript, create `src/utils/sentimentAPI.ts`:

```typescript
interface SentimentResponse {
  text: string;
  sentiment: 'Positive' | 'Negative';
  model_version: string;
}

const API_URL = process.env.REACT_APP_API_URL || 'https://your-api-url.com';

export const analyzeSentiment = async (text: string): Promise<SentimentResponse> => {
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

  return response.json();
};

export const checkAPIHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_URL}/`);
    return response.ok;
  } catch {
    return false;
  }
};
```

## Troubleshooting

### CORS Errors
- Make sure your API has `FRONTEND_URL` environment variable set to your Vercel URL
- Check browser console for specific CORS error messages
- Verify API is deployed and accessible

### API Not Found
- Verify `REACT_APP_API_URL` is set correctly
- Test API directly with curl or Postman
- Check API deployment logs

### Network Errors
- Ensure API is running and accessible
- Check if API URL is correct (no trailing slash)
- Verify environment variables are set in Vercel


