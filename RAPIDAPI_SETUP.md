# 🔑 How to Get FREE RapidAPI Key (5 minutes)

## ✅ Why RapidAPI Real-Time Web Search?
- **FREE tier available**
- Google-powered search results
- Returns structured data (title, URL, snippet)
- Easy integration

---

## 📝 Step-by-Step Setup

### Step 1: Create RapidAPI Account (2 min)

1. Go to https://rapidapi.com/
2. Click **"Sign Up"**
3. Sign up with:
   - Email + Password, OR
   - Google account, OR
   - GitHub account
4. Verify your email if needed

### Step 2: Subscribe to Real-Time Web Search API (2 min)

1. Go to https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-web-search
2. Click **"Subscribe to Test"** button
3. Select the **FREE plan** (or Basic plan if it has free tier)
4. Click **"Subscribe"**
   - May ask for credit card for verification
   - **Won't charge** if you stay in free limits

### Step 3: Get Your API Key (1 min)

1. After subscribing, you'll see the API dashboard
2. Look at the example code on the right
3. Find the line: `'x-rapidapi-key': 'YOUR_KEY_HERE'`
4. Copy your key (looks like: `00717cd319msh0075d3242ebebe5p10bff8jsnf7837adb6887`)
5. **Save this key** - you'll need it for deployment

---

## 🎯 Example Request

The API works like this:
```bash
curl --request GET \
  --url 'https://real-time-web-search.p.rapidapi.com/search?q=climate%20grants&num=10' \
  --header 'x-rapidapi-key: YOUR_KEY_HERE' \
  --header 'x-rapidapi-host: real-time-web-search.p.rapidapi.com'
```

---

## 🔐 Where to Add the Key

### For GitHub Actions:
1. Go to your repo → Settings → Secrets → Actions
2. Click "New repository secret"
3. Name: `RAPIDAPI_KEY`
4. Value: Your copied key (example: `00717cd319msh0075d3242ebebe5p10bff8jsnf7837adb6887`)
5. Click "Add secret"

### For Local Testing:
1. Copy `.env.example` to `.env`
2. Edit `.env`:
   ```
   RAPIDAPI_KEY=00717cd319msh0075d3242ebebe5p10bff8jsnf7837adb6887
   ```
3. Save the file

---

## ✅ Verification

Test your key works:

```bash
python test_setup.py
```

You should see:
```
✓ RapidAPI connection successful!
✓ Search working - found X results
```

---

## 🆘 Troubleshooting

### "Invalid API key"
- Make sure you subscribed to the API
- Copy the full key (no spaces)
- Key format: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### "Quota exceeded"
- You've used your monthly free searches
- System automatically falls back to DuckDuckGo
- No action needed - backup is unlimited

### "429 Too Many Requests"
- You're making requests too fast
- Script already has delays built-in
- Wait a few minutes and try again

---

## 💰 Pricing Information

Check your plan limits at:
https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-web-search/pricing

The newsletter is designed to work within free tier limits by:
- Using smart caching (7-day cache)
- Distributing queries across days
- Falling back to DuckDuckGo when needed

---

## 🎉 That's It!

You now have:
- ✅ Free API key
- ✅ Google-powered search results
- ✅ Automatic backup system
- ✅ Ready to deploy

**Next step**: Follow DEPLOYMENT_GUIDE.md to complete setup.

---

**Need help?** Check the troubleshooting section or review the full documentation in README.md
