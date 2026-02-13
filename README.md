# AGIE - AI Governance Intelligence Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> Lightweight AI-powered governance analysis engine for risk assessment and ISO 27001 compliance mapping.

## 🚧 Status: Active Development (V0.1)

This is a weekend project built in public. Follow the journey:
- [LinkedIn Updates](#) (add your link later)
- [Dev.to Blog](#) (optional)

## What is AGIE?

AGIE analyzes organizational risk registers and AI use cases against:
- ISO 27001 control domains
- AI-specific governance principles (bias, explainability, third-party risk)
- Produces executive-ready risk reports

**This is NOT a chatbot.** It's an intelligence layer that produces structured, decision-grade insights.

## Features (V0.1)

- ✅ CSV risk register ingestion
- ✅ AI use case analysis via Claude API
- ✅ ISO 27001 domain mapping
- ✅ AI governance gap identification
- ✅ Risk scoring (likelihood × impact)
- ✅ Markdown report generation

## Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/agie.git
cd agie

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run analysis
python src/agie.py analyze --risk-register data/sample_risk_register.csv --use-case "We're deploying a chatbot for customer support"
```

## Architecture