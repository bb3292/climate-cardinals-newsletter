# Climate Cardinals - Automated Weekly Newsletter

🌍 **100% FREE automated climate intelligence newsletter** using RapidAPI + DuckDuckGo

---

## ⚡ Quick Start

1. **Get RapidAPI Key** (5 min) - See `RAPIDAPI_SETUP.md`
2. **Setup Gmail** (5 min) - Enable 2FA and generate app password
3. **Deploy to GitHub** (10 min) - Upload files and add 4 secrets
4. **Done!** - Runs automatically forever

**Full guide**: See `DEPLOYMENT_GUIDE.md`

---

## 📋 What You Need

- ✅ RapidAPI account (free)
- ✅ Gmail account (free)
- ✅ GitHub account (free)
- ✅ 20 minutes of time

**Total Cost: $0/month forever**

---

## 🚀 Features

- ✅ **Runs daily** - Collects data Tuesday-Sunday
- ✅ **Sends Monday** - Beautiful email every Monday morning
- ✅ **Auto-clears** - Fresh data each week
- ✅ **100% FREE** - No paid APIs needed
- ✅ **Dual search** - RapidAPI + DuckDuckGo backup
- ✅ **Smart caching** - Reduces API calls by 40%
- ✅ **Premium design** - Magazine-quality email template

---

## 📊 What It Collects

Each week gathers:
- 💰 **Grants & Funding** - Climate/sustainability opportunities
- 📅 **Events & Conferences** - Upcoming climate events
- 👥 **Climate Experts** - LinkedIn profiles of leaders
- 📊 **ESG Reports** - Corporate sustainability disclosures

---

## 🔑 Required Secrets (GitHub)

Add these 4 secrets to GitHub Actions:

1. **RAPIDAPI_KEY** - From Real-Time Web Search API
2. **SENDER_EMAIL** - Your Gmail address  
3. **SENDER_PASSWORD** - Gmail app password (16 chars, no spaces)
4. **RECIPIENT_EMAILS** - Client emails (comma-separated, no spaces)

---

## 📁 Project Structure

```
climate-cardinals-newsletter/
├── automated_newsletter.py    # Main automation script
├── email_template.py          # Premium HTML email generator
├── requirements.txt           # Python dependencies
├── .env.example              # Config template
├── .github/workflows/
│   └── newsletter.yml        # GitHub Actions workflow
├── DEPLOYMENT_GUIDE.md       # Step-by-step deployment
├── RAPIDAPI_SETUP.md         # How to get API key
└── test_setup.py             # Verify your setup
```

---

## 🗓️ How It Works

### Tuesday - Sunday (Days 2-7)
- Script runs at 9 AM UTC
- Collects ~15-20 searches/category
- Saves to CSV files
- Removes duplicates

### Monday (Day 1)
- Script runs at 9 AM UTC
- Loads all accumulated data
- Generates HTML email
- Sends to recipients
- **Clears all data** for new week

---

## 🔧 Setup Instructions

### Option 1: Quick Deploy (Recommended)

```bash
# 1. Get RapidAPI key (see RAPIDAPI_SETUP.md)

# 2. Upload to GitHub
# - Create new repository
# - Upload all files

# 3. Add 4 secrets in Settings → Secrets → Actions

# 4. Enable workflow in Actions tab

# Done! Runs automatically
```

### Option 2: Local Testing

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
cp .env.example .env
# Edit .env with your keys

# 3. Test setup
python test_setup.py

# 4. Run manually
python automated_newsletter.py
```

---

## ✅ Verification

After deployment:

1. **Test run** - Go to Actions → Run workflow
2. **Check logs** - Should see data collection
3. **Wait for Monday** - First email sends
4. **Check inbox** - Verify email received
5. **Check spam** - First email may go to spam

---

## 📊 API Usage

### RapidAPI Limits
- Check your plan at: https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-web-search/pricing
- Newsletter uses ~15-20 searches/day
- ~100-140 searches/week
- ~400-500 searches/month

### Backup System
- If RapidAPI quota exceeded → Auto-switches to DuckDuckGo
- DuckDuckGo is unlimited and free
- No interruption to service

---

## 🛠️ Troubleshooting

### No email received
- Check spam folder
- Verify SENDER_PASSWORD has no spaces
- Check RECIPIENT_EMAILS format: `email1@x.com,email2@y.com`

### API errors
- Verify RapidAPI key is correct
- Check you're subscribed to Real-Time Web Search
- System auto-falls back to DuckDuckGo

### No data collected
- Check workflow logs in Actions tab
- Verify RapidAPI subscription is active
- DuckDuckGo backup will still work

---

## 📞 Support Files

- **`DEPLOYMENT_GUIDE.md`** - Complete deployment instructions
- **`RAPIDAPI_SETUP.md`** - How to get free API key
- **`test_setup.py`** - Verify your configuration

---

## 💰 Cost Breakdown

| Service | Usage | Cost |
|---------|-------|------|
| GitHub Actions | ~70 min/month | $0 (free tier: 2,000 min) |
| RapidAPI | Check your plan | $0 (free tier) |
| DuckDuckGo | Unlimited backup | $0 |
| Gmail | Email sending | $0 |
| **Total** | | **$0/month** |

---

## 🎉 You're All Set!

After deployment, the system:
- ✅ Runs automatically daily
- ✅ Sends beautiful emails every Monday
- ✅ Costs nothing to operate
- ✅ Requires zero maintenance

**Just set it and forget it!** 🚀

---

## 📝 License

MIT License - Free to use and modify

---

**Made with 🌍 for Climate Cardinals**

*Questions? Check DEPLOYMENT_GUIDE.md or RAPIDAPI_SETUP.md*
