# 🚀 FINAL DEPLOYMENT GUIDE - Climate Cardinals Newsletter

## Complete Step-by-Step Instructions (Updated for Real-Time Web Search API)

### 📋 What You'll Need (5 items total)

- [ ] GitHub account (free)
- [ ] Gmail account (for sending emails)
- [ ] RapidAPI account (free)
- [ ] Client's recipient email addresses
- [ ] 15-20 minutes of time

---

## 🔑 STEP 1: Get RapidAPI Key (5 minutes)

### 1.1 Create RapidAPI Account

1. Go to **https://rapidapi.com/**
2. Click **"Sign Up"**
3. Choose sign-up method:
   - Email + Password, OR
   - Google account, OR
   - GitHub account
4. Verify your email

### 1.2 Subscribe to Real-Time Web Search API

1. Go to this link: **https://rapidapi.com/letscrape-6bRBa3QguO5/api/real-time-web-search**
2. Click **"Subscribe to Test"** button (top right)
3. Choose a plan:
   - Look for **"Basic"** or **"Free"** tier
   - Some plans may require credit card but won't charge if you stay in free limits
4. Click **"Subscribe"**

### 1.3 Get Your API Key

1. After subscribing, you'll see the API dashboard
2. Look at the example code on the right side
3. Find this line:
   ```
   'x-rapidapi-key': 'abc123def456...'
   ```
4. **Copy your API key** (looks like: `00717cd319msh0075d3242ebebe5p10bff8jsnf7837adb6887`)
5. **SAVE THIS KEY** - you'll need it in Step 4

**✅ You should now have your RapidAPI key!**

---

## 📧 STEP 2: Setup Gmail for Sending (5 minutes)

### 2.1 Enable 2-Factor Authentication

1. Go to **https://myaccount.google.com/security**
2. Under "Signing in to Google", click **"2-Step Verification"**
3. Follow the setup process
4. Verify your phone number

### 2.2 Generate App Password

1. Go back to **https://myaccount.google.com/security**
2. Under "Signing in to Google", click **"2-Step Verification"**
3. Scroll down to **"App passwords"**
4. Click **"App passwords"**
5. You may need to sign in again
6. Select:
   - **App**: Mail
   - **Device**: Other (Custom name)
   - **Name it**: "Climate Cardinals Newsletter"
7. Click **"Generate"**
8. Copy the **16-character password** (example: `abcd efgh ijkl mnop`)
9. **Remove all spaces**: `abcdefghijklmnop`
10. **SAVE THIS PASSWORD** - you'll need it in Step 4

**✅ You should now have your Gmail app password!**

---

## 📁 STEP 3: Setup GitHub Repository (10 minutes)

### 3.1 Download the Project Files

1. **Download** the ZIP file I provided: `climate-cardinals-newsletter-FINAL.zip`
2. **Extract** it to a folder on your computer
3. You should see these files:
   ```
   climate-cardinals-newsletter-free/
   ├── automated_newsletter.py
   ├── email_template.py
   ├── requirements.txt
   ├── .env.example
   ├── .gitignore
   ├── README.md
   ├── DEPLOYMENT_GUIDE.md
   ├── RAPIDAPI_SETUP.md
   ├── test_setup.py
   └── .github/
       └── workflows/
           └── newsletter.yml
   ```

### 3.2 Create GitHub Repository

1. Go to **https://github.com/new**
2. Fill in:
   - **Repository name**: `climate-cardinals-newsletter`
   - **Description**: "Automated weekly climate intelligence newsletter"
   - **Privacy**: Choose **Private** (recommended for client projects)
   - **Initialize**: ❌ Do NOT check "Add README file"
3. Click **"Create repository"**

### 3.3 Upload Files to GitHub

**Option A - Web Upload (Easier):**

1. On your new repository page, click **"uploading an existing file"**
2. **Drag and drop ALL files** from the extracted folder
3. Make sure to include the `.github` folder with the `workflows` subfolder
4. Scroll down and click **"Commit changes"**

**Option B - Command Line (Advanced):**

```bash
cd path/to/climate-cardinals-newsletter-free
git init
git add .
git commit -m "Initial commit - automated newsletter"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/climate-cardinals-newsletter.git
git push -u origin main
```

**✅ Your code should now be on GitHub!**

---

## 🔒 STEP 4: Configure GitHub Secrets (5 minutes)

This is **CRITICAL** - without these secrets, the newsletter won't work!

1. Go to your repository on GitHub
2. Click **"Settings"** tab (top menu)
3. In left sidebar, click **"Secrets and variables"** → **"Actions"**
4. Click **"New repository secret"** button

### Add These 4 Secrets (one at a time):

#### Secret 1: RAPIDAPI_KEY
- **Name**: `RAPIDAPI_KEY`
- **Value**: Your API key from Step 1.3
  - Example: `00717cd319msh0075d3242ebebe5p10bff8jsnf7837adb6887`
- Click **"Add secret"**

#### Secret 2: SENDER_EMAIL
- **Name**: `SENDER_EMAIL`
- **Value**: Your Gmail address
  - Example: `yourname@gmail.com`
- Click **"Add secret"**

#### Secret 3: SENDER_PASSWORD
- **Name**: `SENDER_PASSWORD`
- **Value**: Your 16-character Gmail App Password from Step 2.2 (NO SPACES)
  - Example: `abcdefghijklmnop`
- Click **"Add secret"**

#### Secret 4: RECIPIENT_EMAILS
- **Name**: `RECIPIENT_EMAILS`
- **Value**: Client email addresses separated by commas (NO SPACES between emails)
  - Example: `client@company.com,manager@company.com,team@company.com`
- Click **"Add secret"**

### ✅ Verify All 4 Secrets Are Added

You should see 4 secrets listed:
- ✅ RAPIDAPI_KEY
- ✅ SENDER_EMAIL
- ✅ SENDER_PASSWORD
- ✅ RECIPIENT_EMAILS

---

## ✅ STEP 5: Enable GitHub Actions (2 minutes)

1. Go to **"Actions"** tab in your repository
2. If you see "Workflows aren't being run on this repository":
   - Click **"I understand my workflows, go ahead and enable them"**
3. You should see **"Climate Cardinals Weekly Newsletter"** workflow
4. If it says "This workflow has a workflow_dispatch event trigger":
   - Click **"Enable workflow"**

**✅ GitHub Actions is now enabled!**

---

## 🧪 STEP 6: Test the System (3 minutes)

### 6.1 Run Manual Test

1. Stay on the **"Actions"** tab
2. Click **"Climate Cardinals Weekly Newsletter"** (on the left)
3. Click **"Run workflow"** button (right side)
4. Select **"Branch: main"**
5. Click the green **"Run workflow"** button
6. Wait 10-20 seconds, then refresh the page
7. You should see a workflow run appear (yellow/orange circle = running)

### 6.2 Check the Results

1. Click on the running workflow
2. Click **"collect-and-send"**
3. Click **"Run newsletter script"**
4. You should see output like:
   ```
   🌍 CLIMATE CARDINALS - FREE AUTOMATED NEWSLETTER
   📅 Date: Saturday, February 07, 2026
   📥 Collecting data for the week (Day 6/7)
   💰 Collecting Grants...
     ✓ RapidAPI: 8 results
   ```

### 6.3 What to Expect

**If it's NOT Monday:**
- ✅ Script collects data
- ✅ Saves to CSV files
- ✅ No email sent (waits for Monday)

**If it IS Monday:**
- ✅ Script loads all weekly data
- ✅ Generates beautiful HTML email
- ✅ Sends to all recipient emails
- ✅ Clears data for fresh week

**✅ If you see green checkmarks, it's working!**

---

## 🗓️ STEP 7: Understand the Weekly Cycle

### How the Automation Works:

```
TUESDAY - SUNDAY (Days 2-7)
├─ 9:00 AM UTC - Script runs automatically
├─ Collects ~15-20 searches per category
├─ Appends to weekly CSV files
├─ Removes duplicates
└─ Waits for Monday

MONDAY (Day 1)
├─ 9:00 AM UTC - Script runs automatically
├─ Detects it's Monday
├─ Loads ALL accumulated data from the week
├─ Generates premium HTML email
├─ Sends to all recipients
├─ CLEARS all CSV files
└─ Ready to start fresh week
```

### Daily Schedule:
- **Runs at**: 9:00 AM UTC every day
- **UTC to your timezone**:
  - 9 AM UTC = 4 AM EST (New York)
  - 9 AM UTC = 1 AM PST (Los Angeles)
  - 9 AM UTC = 2:30 PM IST (India)

### To Change the Schedule:

1. Edit `.github/workflows/newsletter.yml`
2. Change the cron line:
   ```yaml
   - cron: '0 14 * * *'  # 2 PM UTC = 9 AM EST
   ```
3. Cron format: `minute hour day month dayofweek`
   - `0 9 * * *` = 9 AM UTC every day
   - `0 14 * * 1` = 2 PM UTC every Monday only

---

## 📊 STEP 8: Monitor & Verify

### Check First Email (Monday)

**After first Monday at 9 AM UTC:**

1. **Check recipient inboxes** for the email
2. **Check spam folder** if not in inbox
3. **Verify email looks correct** (premium design)

### View Collection Progress (Any Day)

1. Go to **"Actions"** tab
2. Click on latest workflow run
3. Click **"Run newsletter script"**
4. See what data was collected

### Check for Errors

If something fails:
1. Go to **"Actions"** tab
2. Look for **red X** next to workflow run
3. Click on it to see error messages
4. Common fixes:
   - Re-check all 4 secrets are correct
   - Verify Gmail app password (no spaces)
   - Check recipient emails format (no spaces after commas)

---

## 🎯 VERIFICATION CHECKLIST

Before considering deployment complete:

- [ ] RapidAPI key obtained and tested
- [ ] Gmail app password generated
- [ ] GitHub repository created
- [ ] All project files uploaded
- [ ] 4 GitHub secrets configured correctly
- [ ] GitHub Actions enabled
- [ ] Test workflow run completed successfully
- [ ] Understand Monday = email day
- [ ] Client email addresses added
- [ ] Spam folder checked (first email)

---

## 🛠️ TROUBLESHOOTING

### Email Not Sending

**Symptoms**: It's Monday but no email received

**Solutions**:
1. Check Gmail hasn't blocked automated sending:
   - Go to Gmail → Check for security alerts
   - Verify "Less secure app access" or "App passwords" is working
2. Verify SENDER_PASSWORD has no spaces
3. Check RECIPIENT_EMAILS format: `email1@domain.com,email2@domain.com`
4. Look at workflow logs for error messages

### API Quota Exceeded

**Symptoms**: "429 Too Many Requests" or "Quota exceeded"

**Solutions**:
- System automatically falls back to DuckDuckGo (free, unlimited)
- No action needed
- Data will still be collected

### No Data Collected

**Symptoms**: CSV files are empty or email has no items

**Solutions**:
1. Check RapidAPI key is valid
2. Verify you're subscribed to Real-Time Web Search API
3. Check workflow logs for API errors
4. System will use DuckDuckGo fallback automatically

### Workflow Not Running

**Symptoms**: No automatic runs appearing

**Solutions**:
1. Check Actions tab is enabled
2. Verify `.github/workflows/newsletter.yml` exists
3. GitHub Actions can have 5-15 minute delays
4. Check repository isn't disabled

---

## 💰 COST BREAKDOWN

### Current Setup (100% FREE)

| Service | Cost | Usage |
|---------|------|-------|
| GitHub Actions | $0 | 2-3 min/day = ~70 min/month (free tier: 2,000 min) |
| RapidAPI | $0 | Free tier (check your plan limits) |
| DuckDuckGo Backup | $0 | Unlimited, free |
| Gmail | $0 | Free sending |
| **TOTAL** | **$0/month** | ✅ |

### If You Need to Scale

- **GitHub Actions overage**: $0.008/minute
- **RapidAPI paid tiers**: Check pricing page
- **Still very affordable** (<$5/month even with 10x usage)

---

## 📝 FINAL CHECKLIST

- [ ] Downloaded ZIP and extracted files
- [ ] Created GitHub repository
- [ ] Uploaded all files to GitHub
- [ ] Added 4 secrets to GitHub
- [ ] Enabled GitHub Actions
- [ ] Ran test workflow successfully
- [ ] Understand weekly cycle (Monday = email)
- [ ] Client emails configured
- [ ] First Monday verified

---

## 🎉 YOU'RE DONE!

The system is now **fully automated**:

✅ **Runs automatically** every day at 9 AM UTC
✅ **Collects data** Tuesday-Sunday
✅ **Sends email** every Monday
✅ **Clears data** after sending
✅ **Costs $0** to run
✅ **No manual work** required ever

### To Disable Later:
1. Actions tab → Climate Cardinals Weekly Newsletter
2. Click "..." menu → Disable workflow

### To Re-enable:
1. Same steps → Enable workflow

---

## 📞 SUPPORT

If something goes wrong:

1. **Check workflow logs** in Actions tab
2. **Review troubleshooting** section above
3. **Verify all 4 secrets** are correct
4. **Check spam folder** for emails
5. **Contact technical support** if needed

---

## 🚀 NEXT STEPS

After deployment:
1. **Monitor first week** of data collection
2. **Verify first Monday email** arrives
3. **Check spam folders** initially
4. **Confirm with client** email looks good
5. **Set it and forget it!**

---

**Made with 🌍 for Climate Cardinals**

*Last Updated: February 2026*


### 1.1 Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name: "Climate Cardinals Newsletter"
4. Click "Create"

### 1.2 Enable Custom Search API

1. In Google Cloud Console, click "☰" menu
2. Go to "APIs & Services" → "Library"
3. Search for "Custom Search API"
4. Click "Custom Search API"
5. Click "Enable"

### 1.3 Create API Key

1. Go to "APIs & Services" → "Credentials"
2. Click "+ CREATE CREDENTIALS" → "API key"
3. Copy the API key (starts with AIza...)
4. Click "Restrict Key" (optional but recommended)
   - Under "API restrictions" → "Restrict key"
   - Select "Custom Search API"
   - Click "Save"
5. **SAVE THIS API KEY** - you'll need it later

### 1.4 Create Custom Search Engine

1. Go to https://programmablesearchengine.google.com/
2. Click "Add" or "Get Started"
3. Configuration:
   - **Name**: Climate Cardinals Search
   - **What to search**: Search the entire web
   - Turn ON "Search the entire web"
4. Click "Create"
5. Click "Customize" → "Setup"
6. Copy the "Search engine ID" (looks like: abc123def456...)
7. **SAVE THIS ID** - you'll need it later

---

## 📧 STEP 2: Setup Gmail for Sending (5 minutes)

### 2.1 Enable 2-Factor Authentication

1. Go to https://myaccount.google.com/security
2. Under "Signing in to Google", click "2-Step Verification"
3. Follow the setup process
4. Verify your phone number

### 2.2 Generate App Password

1. Go back to https://myaccount.google.com/security
2. Under "Signing in to Google", click "2-Step Verification"
3. Scroll down to "App passwords"
4. Click "App passwords"
5. Select:
   - **Select app**: Mail
   - **Select device**: Other (Custom name)
   - **Name**: Climate Cardinals Newsletter
6. Click "Generate"
7. Copy the 16-character password (like: abcd efgh ijkl mnop)
8. **SAVE THIS PASSWORD** - you'll need it later
9. Remove spaces: abcdefghijklmnop

---

## 📁 STEP 3: Setup GitHub Repository (5 minutes)

### 3.1 Create Repository

1. Go to https://github.com/new
2. Repository name: `climate-cardinals-newsletter`
3. Description: "Automated weekly climate intelligence newsletter"
4. Make it **Private** (recommended)
5. ✓ Add README file
6. Click "Create repository"

### 3.2 Upload Files

Option A - Web Upload:
1. Click "Add file" → "Upload files"
2. Drag and drop all files:
   - automated_newsletter.py
   - email_template.py
   - requirements.txt
   - .env.example
   - .gitignore
   - README.md
   - test_setup.py
3. Create folder `.github/workflows/`
4. Upload newsletter.yml to that folder
5. Click "Commit changes"

Option B - Git Command Line:
```bash
git clone https://github.com/YOUR_USERNAME/climate-cardinals-newsletter.git
cd climate-cardinals-newsletter

# Copy all project files to this directory
# Then:
git add .
git commit -m "Initial commit - automated newsletter system"
git push origin main
```

---

## 🔒 STEP 4: Configure GitHub Secrets (5 minutes)

1. Go to your repository on GitHub
2. Click "Settings" tab
3. In left sidebar, click "Secrets and variables" → "Actions"
4. Click "New repository secret" button

Add each of these secrets (5 total):

### Secret 1: GOOGLE_API_KEY
- Name: `GOOGLE_API_KEY`
- Value: Your API key from Step 1.3 (starts with AIza...)
- Click "Add secret"

### Secret 2: GOOGLE_CX_ID
- Name: `GOOGLE_CX_ID`
- Value: Your Search Engine ID from Step 1.4
- Click "Add secret"

### Secret 3: SENDER_EMAIL
- Name: `SENDER_EMAIL`
- Value: Your Gmail address (e.g., yourname@gmail.com)
- Click "Add secret"

### Secret 4: SENDER_PASSWORD
- Name: `SENDER_PASSWORD`
- Value: Your 16-character App Password from Step 2.2 (no spaces)
- Click "Add secret"

### Secret 5: RECIPIENT_EMAILS
- Name: `RECIPIENT_EMAILS`
- Value: Client's email addresses separated by commas
- Example: `client@example.com,manager@example.com,team@example.com`
- **NO SPACES** between emails
- Click "Add secret"

---

## ✅ STEP 5: Enable GitHub Actions (2 minutes)

1. Go to "Actions" tab in your repository
2. If prompted "Enable Actions", click the button
3. You should see "Climate Cardinals Weekly Newsletter" workflow
4. Click on it
5. Click "Enable workflow" if needed

---

## 🧪 STEP 6: Test the System (5 minutes)

### 6.1 Manual Test Run

1. Go to "Actions" tab
2. Click "Climate Cardinals Weekly Newsletter"
3. Click "Run workflow" button (right side)
4. Click green "Run workflow" button
5. Wait 2-3 minutes
6. Click on the running workflow to see logs
7. Verify it completes successfully ✓

### 6.2 What to Check

✓ "Checkout repository" - should pass  
✓ "Install dependencies" - should pass  
✓ "Run newsletter script" - should show data collection  
✓ No error messages  

If it's not Monday, you'll see:
```
📥 Collecting data for the week (Day X/7)
```

If it IS Monday, you'll see:
```
📧 It's Monday! Sending weekly newsletter...
✅ Email sent successfully
```

---

## 🗓️ STEP 7: Verify Schedule (1 minute)

The workflow is set to run:
- **Every day at 9:00 AM UTC**
- UTC time = 4:00 AM EST / 1:00 AM PST

To change the schedule:
1. Edit `.github/workflows/newsletter.yml`
2. Change the cron line:
```yaml
- cron: '0 14 * * *'  # 2 PM UTC = 9 AM EST
```

Cron format: `minute hour day month dayofweek`
- `0 9 * * *` = 9 AM UTC every day
- `0 14 * * 1` = 2 PM UTC every Monday only

---

## 📊 STEP 8: Understand the Weekly Cycle

### Tuesday - Sunday (Data Collection Days)
- Script runs at 9 AM UTC
- Collects ~20-25 queries per category
- Stays under 100 queries/day limit
- Appends to weekly_data/ CSV files
- Removes duplicates automatically

### Monday (Email Day)
- Script runs at 9 AM UTC
- Detects it's Monday
- Generates HTML email from all accumulated data
- Sends to RECIPIENT_EMAILS
- **Clears all CSV files** for fresh week
- Ready to start collecting for next week

---

## 🔍 STEP 9: Monitoring & Maintenance

### Check if Emails are Sending

**Every Monday after 9 AM UTC:**
1. Check recipient inbox
2. Check spam folder
3. Verify email looks correct

### View Collection Progress

1. Go to "Actions" tab
2. Click on latest workflow run
3. Click "Run newsletter script"
4. See what data was collected

### Check Weekly Data

Data accumulates in `weekly_data/` folder:
- `grants.csv` - Grant opportunities
- `events.csv` - Climate events
- `experts.csv` - LinkedIn experts
- `csr_reports.csv` - ESG reports
- `state.json` - Tracks queries and state

---

## 🛠️ Troubleshooting

### "Workflow not running"
- Check Actions tab → Enable workflows
- Verify cron schedule is correct
- GitHub Actions may have 5-15 minute delay

### "Email not received"
- Check spam folder
- Verify SENDER_EMAIL has sending quota
- Check Gmail hasn't blocked automated sending
- Review workflow logs for errors

### "API quota exceeded"
- Script auto-limits to 90 queries/day
- Check if state.json is saving properly
- May need to reduce DAILY_QUERY_LIMIT

### "No data collected"
- Google may have blocked too many requests
- Try different search keywords
- Check API key is valid
- Verify Custom Search Engine is working

---

## 💰 Cost Analysis

### Current Setup (FREE)
- GitHub Actions: 2,000 minutes/month FREE
- Daily runs: ~2-3 minutes each
- Monthly usage: ~70 minutes
- **Cost: $0/month** ✓

### If You Need More
- GitHub Actions overage: $0.008/minute
- Still very cheap (~$0.56/month if you 10x the usage)

---

## 📝 Final Checklist

- [ ] Google API credentials obtained
- [ ] Gmail app password generated
- [ ] GitHub repository created
- [ ] All files uploaded
- [ ] 5 GitHub secrets configured
- [ ] Workflow enabled
- [ ] Test run completed successfully
- [ ] Schedule verified (9 AM UTC daily)
- [ ] Client email addresses added
- [ ] First Monday email confirmed

---

## 🎉 You're Done!

The system is now fully automated:
- **No manual work required**
- Data collects automatically Tuesday-Sunday
- Email sends automatically every Monday
- CSVs clear automatically after sending
- Runs forever (until you disable it)

### To Disable Later
1. Go to Actions tab
2. Click workflow name
3. Click "•••" menu
4. Select "Disable workflow"

### To Re-enable
1. Same steps
2. Select "Enable workflow"

---

## 📞 Support

If something goes wrong:
1. Check workflow logs in Actions tab
2. Review troubleshooting section above
3. Check GitHub Issues for similar problems
4. Contact technical support

**Made with 🌍 for Climate Cardinals**
