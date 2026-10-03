# MAi pot Flask API - Quick Start Guide

## 🚀 One-Minute Deployment Checklist

### Before Deploying:
- [ ] OpenAI API key ready (`sk-...`)
- [ ] GitHub repository connected to Render
- [ ] All files in repository:
  - [ ] `app.py`
  - [ ] `requirements.txt`
  - [ ] `Procfile`
  - [ ] `runtime.txt`
  - [ ] `README.md`
  - [ ] `.gitignore`

### On Render Dashboard:
- [ ] Create new Web Service
- [ ] Connect GitHub repo
- [ ] Set Build Command: `pip install -r requirements.txt`
- [ ] Set Start Command: `gunicorn app:app`
- [ ] Add Environment Variables:
  - `OPENAI_API_KEY=sk-your_key`
  - `RENDER_EXTERNAL_URL=https://your-app-name.onrender.com`
- [ ] Click Deploy

### After Deployment:
- [ ] Test home route: `GET https://your-app-name.onrender.com/`
- [ ] Test health: `GET https://your-app-name.onrender.com/health`
- [ ] Test API: `POST https://your-app-name.onrender.com/api/chat`

---

## 📝 Sample API Test

```bash
# Test home route
curl https://your-app-name.onrender.com/

# Test AI chat
curl -X POST https://your-app-name.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Who created you?"}'

# Test with image
curl -X POST https://your-app-name.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Analyze this chart", "image": "https://example.com/chart.png"}'
```

---

## 🆘 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| 502 Bad Gateway | Check OPENAI_API_KEY in Render env vars |
| 404 on /api/chat | Verify Procfile: `web: gunicorn app:app` |
| Keep-alive not working | Set RENDER_EXTERNAL_URL env var |
| Slow responses | GPT-4o calls take 2-10s normally |

---

## 📞 Support
- Render Issues: Check deployment logs in dashboard
- OpenAI Issues: Visit https://platform.openai.com/account/billing
- Code Issues: Review README.md for full documentation

---

**Created by Yahya.Kurdistan** ✨
