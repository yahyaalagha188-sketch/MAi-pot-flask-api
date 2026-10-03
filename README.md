# MAi pot Flask API - Deployment Ready

**Universal AI Assistant for Financial & Crypto Analysis**

**Creator:** Yahya.Kurdistan  
**Powered by:** OpenAI GPT-4o

---

## 🚀 Quick Start (Render Deployment)

### Step 1: Connect GitHub
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Connect your GitHub repo: `MAi-pot-flask-api`
4. Click **Connect**

### Step 2: Configure Web Service
- **Name:** `mai-pot-api`
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Region:** Choose closest to you

### Step 3: Set Environment Variables
Click **Environment** and add:
```
OPENAI_API_KEY=sk-your_actual_key_here
RENDER_EXTERNAL_URL=https://mai-pot-api.onrender.com
```

### Step 4: Deploy
Click **Create Web Service** and wait for green status ✅

---

## ✨ Features

✅ **AI Chat API** - GPT-4o powered responses  
✅ **Multilingual** - Kurdish (Sorani), Arabic, English, 50+ languages  
✅ **Crypto Analysis** - Deep market & technical analysis  
✅ **Image Processing** - Chart & image analysis via GPT-4o vision  
✅ **Identity Handling** - Proudly declares creator (Yahya.Kurdistan)  
✅ **Keep-Alive** - Auto-pings every 5 minutes to prevent sleep  
✅ **Production Ready** - Gunicorn WSGI + dynamic PORT support  

---

## 📡 API Endpoints

### 1. Home Route
```bash
GET https://mai-pot-api.onrender.com/
```
Returns app info and online status

### 2. Health Check
```bash
GET https://mai-pot-api.onrender.com/health
```
Monitoring endpoint

### 3. Chat API (Main)
```bash
POST https://mai-pot-api.onrender.com/api/chat
Content-Type: application/json

{
  "text": "Analyze Bitcoin's market trend",
  "image": "https://example.com/chart.png"  # Optional
}
```

---

## 🔧 Local Testing

### 1. Clone & Setup
```bash
git clone https://github.com/yahyaalagha188-sketch/MAi-pot-flask-api.git
cd MAi-pot-flask-api
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install & Run
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-your_key
python app.py
```
Visit: `http://localhost:5000/`

---

## 📝 Example Requests

### Text Analysis
```bash
curl -X POST https://mai-pot-api.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Who created you?"}'
```

### Chart Analysis
```bash
curl -X POST https://mai-pot-api.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Analyze this chart",
    "image": "https://example.com/chart.png"
  }'
```

### Professional Email
```bash
curl -X POST https://mai-pot-api.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Write a professional email about quarterly results"}'
```

---

## 🛠️ Frontend Integration

### JavaScript/React
```javascript
const response = await fetch('https://mai-pot-api.onrender.com/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: 'Your question here',
    image: 'https://example.com/chart.png' // optional
  })
});
const { reply } = await response.json();
console.log(reply);
```

### Python
```python
import requests
response = requests.post(
  'https://mai-pot-api.onrender.com/api/chat',
  json={'text': 'Your question'}
)
print(response.json()['reply'])
```

---

## 📦 Project Structure

```
MAi-pot-flask-api/
├── app.py              # Main Flask application
├── requirements.txt    # Dependencies
├── Procfile           # Render config
├── runtime.txt        # Python version
├── .gitignore         # Git ignore
└── README.md          # This file
```

---

## ⚙️ Environment Variables

| Variable | Required | Example |
|----------|----------|----------|
| `OPENAI_API_KEY` | ✅ Yes | `sk-...` |
| `RENDER_EXTERNAL_URL` | ⚠️ For keep-alive | `https://mai-pot-api.onrender.com` |
| `PORT` | Auto-assigned | `5000` (Render sets this) |

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| 502 Bad Gateway | Check OPENAI_API_KEY in Render env |
| App goes to sleep | Set RENDER_EXTERNAL_URL env var |
| Image not processing | Ensure image URL is public & valid |
| Slow responses | GPT-4o typically takes 2-10 seconds |

---

## 🎯 Key Features Explained

### Keep-Alive Mechanism
Automatically pings the app every 5 minutes to prevent Render free tier from sleeping. Runs in background thread.

### Identity Handling
When user asks "Who created you?", bot responds:
> "I was created by Yahya.Kurdistan. I am the MAi pot AI assistant..."

### Multilingual Support
Responds in the user's language (Kurdish, Arabic, English, etc.)

### Image Analysis
Accepts chart/image URLs or base64-encoded files via GPT-4o vision API

---

## 💡 Tips for Production

1. **Upgrade Render Plan** - Free tier sleeps; paid plans stay always-on
2. **Monitor API Costs** - Set OpenAI usage limits in dashboard
3. **Add Rate Limiting** - Protect API from abuse
4. **Use CORS Headers** - If calling from browser
5. **Log Requests** - Add logging for debugging

---

## 📞 Support

- **Render Issues:** Check deployment logs in dashboard
- **OpenAI Issues:** Visit https://platform.openai.com/account/billing
- **Code Issues:** Review documentation or open GitHub issue

---

## 📄 License

Created by **Yahya.Kurdistan** ✨

---

**Ready to deploy? Start with Step 1 above!** 🚀
