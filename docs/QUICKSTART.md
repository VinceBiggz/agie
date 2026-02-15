# AGIE Quickstart Guide

**Get running in 5 minutes**

---

## Prerequisites

- Python 3.8+ installed
- Terminal/command line access
- 5 minutes of your time

---

## Step 1: Get the Code (1 min)

```bash
git clone https://github.com/VinceBiggz/agie.git
cd agie
```

---

## Step 2: Setup Environment (2 min)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install AGIE
pip install -e .
```

---

## Step 3: Get API Key (1 min)

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API key"
3. Copy the key (starts with `AIza...`)

---

## Step 4: Configure (30 sec)

```bash
# Copy template
cp .env.example .env

# Edit .env and add your key
# GOOGLE_API_KEY=AIza...your-key-here
```

**macOS/Linux:**
```bash
echo "GOOGLE_API_KEY=your-key-here" > .env
```

**Windows:**
```powershell
echo GOOGLE_API_KEY=your-key-here > .env
```

---

## Step 5: Run Your First Analysis (30 sec)

```bash
agie analyse \
  -r data/sample_risk_register.csv \
  -u "Deploy AI chatbot for customer support"
```

**You'll see:**
- ✓ Analyser initialised
- ✓ Analysis complete (15 sec)
- ✓ Report saved: `agie_report.md`

---

## What Just Happened?

AGIE:
1. ✅ Parsed your CSV risk register (10 risks)
2. ✅ Analysed your AI use case against ISO 27001
3. ✅ Identified 7 AI-specific risks
4. ✅ Mapped to 13 ISO control domains
5. ✅ Found 9 governance gaps
6. ✅ Generated executive report

**All in ~15 seconds, completely free!**

---

## View Your Report

```bash
# macOS
open agie_report.md

# Linux
xdg-open agie_report.md

# Windows
start agie_report.md

# Or any text editor
code agie_report.md
nano agie_report.md
```

---

## Next Steps

### Try Different Use Cases

```bash
# Financial services
agie analyse -r data/sample_risk_register.csv \
  -u "AI for loan approval decisions" \
  -c "industry: financial services, data: PII"

# HR/Recruitment
agie analyse -r data/sample_risk_register.csv \
  -u "Resume screening AI" \
  -c "industry: HR, data: candidate information"

# Healthcare
agie analyse -r data/sample_risk_register.csv \
  -u "Medical diagnosis assistance AI" \
  -c "industry: healthcare, data: patient records"
```

### Use Your Own Data

Create a CSV with these columns:
- `risk_id` - Unique identifier
- `risk_description` - What could go wrong
- `likelihood` - 1-5 (how likely)
- `impact` - 1-5 (how bad)
- `category` - Optional (Security, Operations, etc.)
- `owner` - Optional
- `mitigation` - Optional
- `status` - Optional

**Example:**
```csv
risk_id,risk_description,likelihood,impact
RISK-001,Data breach from weak passwords,4,5
RISK-002,Model bias in AI decisions,3,4
```

Then:
```bash
agie analyse -r your_risks.csv -u "Your AI use case"
```

### Explore Commands

```bash
# See all commands
agie --help

# View usage examples
agie examples

# Validate your CSV
agie validate your_risks.csv

# Check version
agie version
```

---

## Troubleshooting

### "GOOGLE_API_KEY not found"

**Fix:** Make sure `.env` file exists with your key:
```bash
cat .env  # Should show GOOGLE_API_KEY=...
```

### "Model not found"

**Fix:** AGIE has auto-fallback. If you see this, check internet connection:
```bash
ping google.com
```

### "Rate limit exceeded"

**Fix:** Free tier = 15 requests/min. Wait 60 seconds and try again.

AGIE has built-in rate limiting, so this is rare.

### "Import Error"

**Fix:** Reinstall:
```bash
pip uninstall agie
pip install -e .
```

---

## Learn More

- **Full docs:** See [README.md](../README.md)
- **Project structure:** See [HANDOVER.md](HANDOVER.md)
- **Code examples:** Browse `src/` directory
- **Issues:** [GitHub Issues](https://github.com/VinceBiggz/agie/issues)

---

## Get Help

**Stuck?**
- Check [GitHub Issues](https://github.com/VinceBiggz/agie/issues)
- Open a new issue with your error message
- Reach out on [LinkedIn](https://www.linkedin.com/in/vincentwachira)

---

**That's it! You're ready to assess AI governance risks.** 🎉

**Next:** Try analysing your own AI use cases and risk registers!