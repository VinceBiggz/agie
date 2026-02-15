# AGIE - AI Governance Intelligence Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Built with Gemini](https://img.shields.io/badge/Built%20with-Gemini%202.5%20Flash-blue)](https://ai.google.dev/)

> Professional AI governance risk assessment tool for IT leaders, CISOs, and compliance officers.

## 🎉 Status: V0.1 Complete! (Feb 15, 2025)

**Built in public over one weekend.** 

**Author:** [Vincent Wachira](https://www.linkedin.com/in/vincentwachira) | [@VinceBiggz](https://github.com/VinceBiggz)

### Weekend Build Achievements:
- ✅ End-to-end risk analysis workflow (CSV → AI → Report)
- ✅ Google Gemini 2.5 Flash integration (FREE - 1,500 requests/day)
- ✅ Professional CLI with beautiful terminal output
- ✅ Markdown report generation (executive-ready)
- ✅ ISO 27001 control domain mapping
- ✅ Production-grade rate limiting & error handling
- ✅ Auto-fallback for API changes
- ✅ Mock mode for offline development
- ✅ 2,000+ lines of tested code
- ✅ Analysis time: ~15 seconds

---

## What is AGIE?

AGIE analyses organisational risk registers and AI use cases against ISO 27001:2022 standards, identifying:
- **AI-specific risks** (bias, explainability, model drift, hallucination)
- **ISO 27001 control domains** (A.5 through A.18)
- **Governance gaps** (missing policies, oversight, monitoring)
- **Regulatory concerns** (GDPR, AI Act, data protection)

**Output:** Executive-ready reports with prioritised recommendations.

**This is NOT a chatbot.** It's an intelligence engine that produces structured, decision-grade insights.

---

## ✨ Features

### Core Functionality
- **CSV Risk Register Parser** - Validates and processes organisational risks
- **AI-Powered Analysis** - Google Gemini 2.5 Flash (free tier) or Claude Sonnet 4 (premium)
- **ISO 27001 Mapping** - Automatic control domain identification
- **Governance Assessment** - Identifies specific policy and process gaps
- **Risk Scoring** - Likelihood × Impact methodology
- **Report Generation** - Professional markdown reports for board presentations
- **CLI Interface** - Beautiful terminal output with progress indicators

### Technical Features
- **Rate Limiting** - Token bucket algorithm (15 RPM) prevents quota exhaustion
- **Auto-Fallback** - Model discovery system handles API changes gracefully
- **Mock Mode** - Develop and test without API calls
- **Cross-Platform** - Works on macOS, Linux, Windows
- **Type-Safe** - Comprehensive type hints and docstrings
- **Production-Grade** - Extensive logging, error handling, validation

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (3.13+ recommended)
- Google AI Studio API key (free tier: 1,500 requests/day)

### Installation

```bash
# Clone repository
git clone https://github.com/VinceBiggz/agie.git
cd agie

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install (this registers 'agie' command)
pip install -e .

# Configure API key
cp .env.example .env
# Edit .env: GOOGLE_API_KEY=your-key-here
```

**Get free Gemini API key:** [Google AI Studio](https://aistudio.google.com/app/apikey)

### Usage

```bash
# Show help
agie --help

# See examples
agie examples

# Validate CSV format
agie validate data/sample_risk_register.csv

# Run analysis
agie analyse \
  -r data/sample_risk_register.csv \
  -u "Deploy AI chatbot for customer support"

# With context
agie analyse \
  -r data/sample_risk_register.csv \
  -u "AI for loan approvals" \
  -c "industry: financial services, data: PII" \
  -o financial_report.md
```

### Expected Output

```
╭────────────────────────────────────────────╮
│ AGIE - AI Governance Intelligence Engine   │
│ Analysing AI risks against ISO 27001...    │
╰────────────────────────────────────────────╯

✓ Analyser ready
✓ Analysis complete

        Analysis Summary         
┌─────────────────────┬─────────┐
│ Overall Risk Score  │ 3.4/10  │
│ Organisational Risks│ 10      │
│ AI-Specific Risks   │ 7       │
│ Governance Gaps     │ 9       │
│ ISO 27001 Domains   │ 13      │
│ High-Priority Items │ 10      │
└─────────────────────┴─────────┘

✓ Report saved: agie_report.md
```

---

## 📊 Sample Analysis Results

**Input:** Financial services chatbot use case + 10 organisational risks

**Output:**
- **7 AI Risks:** Bias, explainability gaps, privacy violations, model drift, hallucination, data poisoning, third-party risk
- **13 ISO Domains:** A.5 (Policies), A.8 (Assets), A.9 (Access), A.12 (Operations), A.14 (Development), A.15 (Suppliers), A.18 (Compliance), and more
- **9 Governance Gaps:** Missing AI framework, weak data governance, insufficient monitoring, unclear accountability
- **95% Confidence:** High-quality AI analysis

**Report includes:**
- Executive summary with risk scoring
- Organisational risk breakdown
- AI-specific risk analysis
- ISO 27001 domain mapping with explanations
- Governance gap assessment
- Prioritised recommendations
- High-priority action items

---

## 🏗️ Architecture

```
┌─────────────────┐
│   User Input    │
│  - CSV Risks    │
│  - Use Case     │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  CSV Parser     │ ← Validates, calculates scores
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Risk Analyser   │ ← Orchestrates workflow
└────┬───────┬────┘
     │       │
     v       v
┌────────┐ ┌────────┐
│ Gemini │ │ Claude │ ← AI analysis
│ (FREE) │ │(Premium)│
└────┬───┘ └────┬───┘
     │          │
     └────┬─────┘
          v
   ┌─────────────┐
   │   Report    │ ← Markdown output
   │  Generator  │
   └─────────────┘
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.13
- **AI Engines:** Google Gemini 2.5 Flash (free) + Anthropic Claude Sonnet 4 (premium)
- **Data:** pandas + pyarrow
- **CLI:** click + rich (beautiful terminal output)
- **Config:** python-dotenv

**Why This Stack:**
- Gemini free tier = unlimited development
- Claude ready for premium analysis when needed
- pandas = industry standard for data processing
- rich = professional terminal UX
- All cross-platform compatible

---

## 📝 Project Structure

```
agie/
├── src/
│   ├── agie.py              # CLI entry point
│   ├── logger.py            # Centralized logging
│   ├── analyser/
│   │   ├── gemini_client.py    # Gemini integration
│   │   ├── claude_client.py    # Claude integration
│   │   ├── mock_claude_client.py  # Offline mode
│   │   └── risk_analyser.py    # Main orchestrator
│   ├── parsers/
│   │   └── csv_parser.py       # CSV validation
│   ├── outputs/
│   │   └── markdown_report.py  # Report generator
│   └── utils/
│       └── model_discovery.py  # Auto-fallback system
├── data/
│   └── sample_risk_register.csv  # Test data
├── docs/
│   ├── HANDOVER.md          # Project documentation
│   └── WEEKEND_PLAN.md      # Build timeline
├── setup.py                 # Pip installation
└── requirements.txt         # Dependencies
```

---

## 🗺️ Roadmap

### V0.1 (Complete - Weekend Build)
- [x] Core analysis engine
- [x] Gemini API integration
- [x] Report generation
- [x] Professional CLI
- [x] Documentation

### V0.2 (Next Week)
- [ ] Claude API testing & comparison
- [ ] PDF export option
- [ ] Multiple use case comparison
- [ ] Enhanced ISO mapping
- [ ] CONTRIBUTING.md guide

### V0.3 (Week 3)
- [ ] Web interface prototype
- [ ] Database persistence
- [ ] Historical tracking
- [ ] Custom taxonomies
- [ ] Batch processing

### V1.0 (Future)
- [ ] API endpoint
- [ ] Multi-language support
- [ ] Plugin system
- [ ] Enterprise features

---

## 🤝 Contributing

This is an open-source learning project. Contributions welcome!

**How to contribute:**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

**Code standards:**
- Follow PEP 257 docstrings
- Use type hints
- Add comprehensive logging
- Test your changes
- Use conventional commits (`feat:`, `fix:`, `docs:`)

**Good first issues:**
- Add more ISO domain explanations
- Improve error messages
- Add unit tests
- Create tutorials
- Translate documentation

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

Free to use, modify, and distribute. Attribution appreciated.

---

## 👨‍💻 Author

**Vincent Wachira Kung'u**
- LinkedIn: [vincentwachira](https://www.linkedin.com/in/vincentwachira)
- GitHub: [@VinceBiggz](https://github.com/VinceBiggz)
- Email: wachirakungu@gmail.com

**Certifications:**
- ISO 27001 Internal Auditor
- ISO 9001:2015 QMS Lead Auditor
- Google Certified Professional Cloud Architect
- Oracle OCI Gen AI Professional
- ITIL v4 Foundations

---

## 🙏 Acknowledgments

- **Google Gemini** - Free tier AI analysis
- **Anthropic Claude** - Premium AI option
- **ISO/IEC 27001:2022** - Security framework
- **#BuildInPublic** community - Inspiration and support

---

## 📞 Support

**Issues?** Open a [GitHub issue](https://github.com/VinceBiggz/agie/issues)

**Questions?** Reach out on [LinkedIn](https://www.linkedin.com/in/vincentwachira)

**Want to contribute?** PRs welcome!

---

## ⭐ Star This Project

If AGIE helps you assess AI governance risks, please star the repository!

---

**Built with ❤️ for IT leaders, CISOs, and compliance officers**

*Making AI governance accessible, one risk assessment at a time.*