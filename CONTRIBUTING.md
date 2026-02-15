# Contributing to AGIE

Thank you for your interest in contributing to AGIE! 🎉

This document provides guidelines for contributing to the project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

**Be respectful.** We're all learning and building together.

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

---

## How Can I Contribute?

### 🐛 Report Bugs

Found a bug? Help us fix it!

**Before submitting:**
1. Check [existing issues](https://github.com/VinceBiggz/agie/issues)
2. Verify it's not already fixed in latest version
3. Gather error messages and logs

**Submit a bug report:**
- Use descriptive title
- Describe exact steps to reproduce
- Include error messages/logs
- Specify your environment (OS, Python version)
- Include sample data if relevant (anonymized!)

**Template:**
```markdown
**Bug Description:**
Brief summary

**Steps to Reproduce:**
1. Run command `agie analyse...`
2. See error...

**Expected Behavior:**
What should have happened

**Actual Behavior:**
What actually happened

**Environment:**
- OS: macOS 14
- Python: 3.13
- AGIE: v0.1.0

**Error Output:**
```
Paste error message here
```
```

### 💡 Suggest Features

Have an idea? We'd love to hear it!

**Good feature requests include:**
- Clear problem statement
- Proposed solution
- Alternative solutions considered
- Why this benefits users

**Example:**
"Add PDF export because executives prefer PDF reports for board meetings. Could use reportlab or weasyprint. Alternative: HTML export that prints to PDF."

### 📖 Improve Documentation

Documentation is crucial! Help us make it better:
- Fix typos or unclear wording
- Add examples or tutorials
- Translate to other languages
- Create video walkthroughs
- Write blog posts

### 🔧 Submit Code

Ready to code? Awesome!

**Good first issues:**
- Add unit tests
- Improve error messages
- Add ISO domain explanations
- Create example use cases
- Enhance CLI output

---

## Development Setup

### 1. Fork & Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/agie.git
cd agie
```

### 2. Create Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
```

### 3. Configure

```bash
cp .env.example .env
# Add your GOOGLE_API_KEY
```

### 4. Create Branch

```bash
git checkout -b feature/your-feature-name
```

**Branch naming:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code improvements
- `test/` - Test additions

---

## Code Standards

### File Structure

```python
"""
Module description.

Detailed explanation of what this module does.

@author: Your Name
@date: 2025-02-15
@version: 0.1.0
@license: MIT
"""

import sys
from pathlib import Path
from typing import Optional

from src.logger import logger
```

### Docstrings (PEP 257)

```python
def analyse_risk(risk_data: Dict, context: Optional[Dict] = None) -> Assessment:
    """
    Analyse risk data against governance framework.
    
    Args:
        risk_data: Dictionary with risk information
        context: Optional additional context
        
    Returns:
        Assessment object with findings
        
    Raises:
        ValidationError: If risk_data is invalid
        
    Example:
        >>> assessment = analyse_risk({'risk_id': 'R-001'})
    """
```

### Type Hints

Always use type hints:
```python
# Good
def process_csv(filepath: Path) -> pd.DataFrame:

# Bad
def process_csv(filepath):
```

### Logging

Use appropriate log levels:
```python
logger.debug("Detailed flow information")
logger.info("Important milestone")
logger.warning("Potential issue")
logger.error("Operation failed")
logger.critical("System-breaking problem")
```

### Error Handling

Handle errors at logical boundaries:
```python
# Good - handle at entry point
def analyse(filepath: Path) -> Report:
    try:
        data = parse_csv(filepath)
        return generate_report(data)
    except CSVParserError as e:
        logger.error(f"CSV parsing failed: {e}")
        raise

# Bad - unnecessary try/catch
def add_numbers(a: int, b: int) -> int:
    try:
        return a + b  # This won't fail!
    except Exception:
        pass
```

### British English

We use British spellings:
- `analyser` not `analyzer`
- `colour` not `color`
- `organisation` not `organization`

---

## Commit Guidelines

### Conventional Commits

Format: `<type>(<scope>): <subject>`

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting (no code change)
- `refactor` - Code restructuring
- `test` - Tests
- `chore` - Maintenance

**Examples:**
```bash
feat(cli): add verbose mode flag
fix(parser): handle missing CSV columns
docs(readme): update installation instructions
refactor(analyser): extract ISO mapping logic
test(parser): add edge case tests
chore: bump anthropic to 0.40.0
```

**Commit message body:**
```
feat(cli): add verbose mode flag

- Add -v/--verbose option to analyse command
- Show detailed API responses when enabled
- Update help text and examples

Resolves #42
```

---

## Pull Request Process

### 1. Update Your Branch

```bash
git fetch upstream
git rebase upstream/main
```

### 2. Test Your Changes

```bash
# Run your code
agie analyse -r data/sample_risk_register.csv -u "Test"

# Check it works
```

### 3. Commit & Push

```bash
git add .
git commit -m "feat: add amazing feature"
git push origin feature/amazing-feature
```

### 4. Create Pull Request

**Title:** Same as commit message
```
feat(cli): add verbose mode
```

**Description:**
```markdown
## What

Add verbose mode to CLI for debugging

## Why

Users requested more visibility into API calls

## How

- Added -v flag to analyse command
- Logs full API responses when enabled
- Added tests

## Testing

- ✅ Tested with sample data
- ✅ Verified help text updates
- ✅ Checked error scenarios

## Screenshots

[If UI change, add screenshot]

Closes #42
```

### 5. Code Review

- Respond to feedback promptly
- Make requested changes
- Push updates to same branch
- Don't force push after review starts

---

## Testing Guidelines

### Manual Testing

Before submitting:
```bash
# Test basic flow
agie validate data/sample_risk_register.csv
agie analyse -r data/sample_risk_register.csv -u "Test case"

# Test edge cases
agie analyse -r nonexistent.csv -u "Test"  # Should error gracefully
agie analyse -r data/sample_risk_register.csv -u ""  # Should validate input
```

### Unit Tests (Future)

We'll add pytest soon. When adding features, include tests:
```python
def test_csv_parser_validates_columns():
    parser = CSVParser()
    with pytest.raises(CSVParserError):
        parser.parse("invalid.csv")
```

---

## Documentation

When adding features, update docs:

**Must update:**
- README.md (if user-facing feature)
- Docstrings in code
- CHANGELOG.md (coming soon)

**Should update:**
- QUICKSTART.md (if affects getting started)
- Examples (if new capability)

---

## Questions?

**Stuck?** Ask for help!

- Comment on the issue
- Open a discussion
- Reach out on [LinkedIn](https://www.linkedin.com/in/vincentwachira)

**Remember:** No question is too small. We're all learning!

---

## Recognition

Contributors will be:
- Listed in README contributors section
- Thanked in release notes
- Forever appreciated! 🙏

---

**Thank you for contributing to AGIE!**

*Together, we're making AI governance accessible.*