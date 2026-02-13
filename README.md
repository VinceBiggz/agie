# AGIE - AI Governance Intelligence Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Built with Gemini](https://img.shields.io/badge/Built%20with-Gemini%202.5%20Flash-blue)](https://ai.google.dev/)

> Lightweight AI-powered governance analysis engine for risk assessment and ISO 27001 compliance mapping.

## 🚧 Status: Active Development (V0.1) - Day 1 Complete!

**Built in public over one weekend.** Follow the journey:
- LinkedIn: [Vincent Wachira](https://www.linkedin.com/in/vincentwachira)
- GitHub: [@VinceBiggz](https://github.com/VinceBiggz)

### 🎉 Day 1 Achievements (Feb 14, 2025):
- ✅ Professional project structure with centralized logging
- ✅ CSV risk register parser with validation
- ✅ Gemini 2.5 Flash integration (FREE tier!)
- ✅ Production-grade rate limiting (15 RPM)
- ✅ Mock client for development
- ✅ Real AI governance analysis working

**Coming Tomorrow:** Full end-to-end workflow, report generation, CLI interface

---

## What is AGIE?

AGIE analyzes organizational risk registers and AI use cases against:
- **ISO 27001 control domains** (A.5 through A.18)
- **AI-specific governance principles** (bias, explainability, model drift, third-party risk)
- **Regulatory frameworks** (GDPR, financial regulations, data protection)

**Output:** Executive-ready risk reports with actionable recommendations.

**This is NOT a chatbot.** It's an intelligence layer that produces structured, decision-grade insights for CISOs, compliance officers, and IT leaders.

---

## ✨ Features

### Implemented ✅
- **CSV Risk Register Parsing** - Validates and processes organizational risk data
- **AI-Powered Analysis** - Google Gemini 2.5 Flash for governance assessment
- **ISO 27001 Mapping** - Automatic control domain identification
- **AI Risk Detection** - Identifies bias, explainability, drift, and third-party risks
- **Rate Limiting** - Token bucket algorithm (15 requests/min)
- **Comprehensive Logging** - Production-grade observability
- **Mock Mode** - Develop without API calls

### In Progress 🚧
- Risk scoring engine (likelihood × impact)
- Markdown report generation
- CLI interface (`agie analyze ...`)
- Multiple use case comparison

### Planned 📋
- PDF report export
- Web interface
- Custom taxonomy support
- Historical tracking

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
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Get Your Free Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create API key
3. Add to `.env` file

### Test the Components

```bash
# Test CSV parser
python src/parsers/csv_parser.py

# Test Gemini AI analysis (REAL API call)
python src/analyzer/gemini_client.py

# Coming tomorrow: Full workflow
python src/analyzer/risk_analyzer.py
```

---

## 📊 Example Output

```
AI Risks Identified (7):
  1. Bias and Discrimination in product recommendations
  2. Explainability and Transparency gaps
  3. Privacy Violations and Data Leakage risks
  4. Model Drift and performance decay
  5. Hallucination in financial advice
  6. Data Poisoning/Integrity Attacks
  7. Third-Party AI Risk from cloud services

ISO 27001 Domains Affected (11):
  - A.5 Information Security Policies
  - A.8 Asset Management
  - A.9 Access Control
  - A.12 Operations Security
  - A.15 Supplier Relationships
  - A.18 Compliance
  ... and 5 more

Confidence Score: 0.95
```

---

## 🏗️ Architecture

```
Input Layer
  ├── CSV Risk Register Parser
  └── Use Case Description

Intelligence Layer
  ├── Gemini 2.5 Flash API
  ├── Rate Limiter (15 RPM)
  └── Structured Prompt Engine

Analysis Layer
  ├── ISO 27001 Domain Mapper
  ├── AI Risk Identifier
  └── Governance Gap Analyzer

Output Layer
  ├── Risk Scoring Engine (coming)
  └── Report Generator (coming)
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.13
- **AI Engine:** Google Gemini 2.5 Flash (free tier)
- **Data Processing:** pandas
- **CLI Framework:** click + rich
- **Logging:** Python logging module
- **Environment:** python-dotenv

---

## 📝 Development Philosophy

- **Build in Public:** Transparent progress, real-time updates
- **Production-Grade:** Comprehensive logging, error handling, rate limiting
- **Test-Driven:** Every component tested before integration
- **Documented:** Clear docstrings, type hints, comments
- **Modular:** Single-responsibility modules, easy to extend

---

## 🗺️ Roadmap

### V0.1 (This Weekend - Feb 14-16)
- [x] Project structure
- [x] CSV parser
- [x] Gemini API integration
- [x] Mock client
- [ ] Risk analyzer integration
- [ ] Report generator
- [ ] CLI interface

### V0.2 (Week 2)
- [ ] Enhanced ISO mapping
- [ ] Multiple use case comparison
- [ ] PDF report output
- [ ] Performance optimizations

### V1.0 (Week 3+)
- [ ] Web interface
- [ ] Database persistence
- [ ] Custom taxonomy support
- [ ] Historical tracking
- [ ] API endpoint

---

## 🤝 Contributing

This is a learning project built in public. Contributions welcome!

**How to contribute:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Code Standards:**
- Follow PEP 257 docstring conventions
- Use type hints
- Add comprehensive logging
- Test your changes
- Use conventional commits

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

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

- Built with [Google Gemini](https://ai.google.dev/) 2.5 Flash (free tier)
- Inspired by the need for practical AI governance tools in Africa
- Part of the #BuildInPublic movement

---

## 📞 Support

Having issues? Found a bug?
- Open an issue on [GitHub](https://github.com/VinceBiggz/agie/issues)
- Reach out on [LinkedIn](https://www.linkedin.com/in/vincentwachira)

---

**⭐ Star this repo if you find it useful!**

*Built with ❤️ for IT leaders, CISOs, and compliance officers*