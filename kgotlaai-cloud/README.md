# Kgotla AI - Cloud Agents

**Your agents running in the cloud - accessible from any device.**

---

## 🎯 What This Is

This repository runs your 5 AI agents automatically every day in the cloud:
- **Lead Hunter** - Finds 50+ prospects daily
- **Content Machine** - Creates 3 LinkedIn posts
- **Funding Scout** - Tracks ED/SD opportunities
- **Team Tracker** - Monitors IBM progress
- **Website Repair** - Audits and fixes

**You can access results from any browser** - library computer, phone, tablet.

---

## 🚀 Setup Instructions (One-Time)

### Step 1: Create GitHub Account (FREE)
1. Go to https://github.com/signup
2. Sign up with your email
3. Verify your email address

### Step 2: Create Repository
1. Go to https://github.com/new
2. Repository name: `kgotlaai-agents`
3. Make it **Public** (free)
4. Click "Create repository"

### Step 3: Upload Files
1. Download this folder as ZIP
2. Extract the ZIP
3. Go to your GitHub repository
4. Click "Add file" → "Upload files"
5. Drag and drop all files from the extracted folder
6. Click "Commit changes"

### Step 4: Run Agents
1. In your GitHub repo, click "Actions" tab
2. Click "Kgotla AI Daily Agents"
3. Click "Run workflow" button
4. Wait 2-3 minutes

### Step 5: View Results
1. Go to "outputs/" folder in your repo
2. Click on any file to view it
3. Download files as needed

---

## 📅 Automatic Schedule

Your agents run **automatically every day at 6:00 AM UTC**.

To change the time, edit `.github/workflows/daily-agents.yml`:
```yaml
- cron: '0 6 * * *'  # 6 AM UTC
```

Time converter: https://www.worldtimebuddy.com/

---

## 📁 Your Output Files

After each run, you'll find:

| Folder | Contains |
|--------|----------|
| `outputs/leads/` | CSV with 138+ prospects and draft emails |
| `outputs/content/` | LinkedIn posts ready to copy-paste |
| `outputs/funding/` | Application packages for sefa, NEF, etc. |
| `outputs/team/` | Progress reports for your team |
| `outputs/website/` | SSL fix guides and audit reports |
| `DAILY_REPORT.md` | Summary of today's results |

---

## 📱 Access From Anywhere

### Library Computer:
1. Go to https://github.com/YOUR_USERNAME/kgotlaai-agents
2. Click "outputs/" folder
3. Download files you need

### Phone:
1. Open GitHub app or browser
2. Go to your repository
3. View files directly

### Email (Optional):
Add email notifications to get results delivered.

---

## 🔄 Manual Run

Need results NOW?

1. Go to https://github.com/YOUR_USERNAME/kgotlaai-agents/actions
2. Click "Kgotla AI Daily Agents"
3. Click "Run workflow" → "Run workflow"
4. Wait 2-3 minutes
5. Refresh to see results

---

## 🛠️ Customization

### Change Your Info
Edit `agents/config.py`:
```python
COMPANY_CONFIG = {
    'company_name': 'Kgotla AI',
    'founder_name': 'Mahlo Kgotleng',
    'email': 'mahlo@kgotlaai.co.za',
    ...
}
```

### Change Target Industries
Edit individual agent files in `agents/` folder.

### Change Schedule
Edit `.github/workflows/daily-agents.yml`:
```yaml
schedule:
  - cron: '0 6 * * *'  # Change this
```

---

## 💰 Costs

**FREE** - GitHub Actions is free for public repositories.

Limits:
- 2,000 minutes/month (more than enough)
- Runs reset monthly

---

## 🆘 Troubleshooting

### Agents not running?
- Check "Actions" tab for errors
- Make sure repository is Public
- Check that all files were uploaded

### Can't find outputs?
- Go to repository main page
- Look for "outputs/" folder
- Check "DAILY_REPORT.md"

### Need to update agents?
- Edit files directly on GitHub
- Or re-upload modified files

---

## 📞 Support

This system was built for Kgotla AI.

If something breaks:
1. Check the Actions tab for error messages
2. Re-run the workflow
3. Re-upload files if needed

---

## ✅ Quick Checklist

- [ ] GitHub account created
- [ ] Repository created (public)
- [ ] All files uploaded
- [ ] First workflow run complete
- [ ] Outputs visible in repository
- [ ] Daily schedule confirmed

---

**Once set up, this runs automatically every day.**

**You just check your GitHub repo for fresh leads, content, and reports.**

🚀 **Let's get you set up now.**
