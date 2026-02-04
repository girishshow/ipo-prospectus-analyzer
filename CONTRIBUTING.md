# Contributing to IPO Intelligence Platform

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🎯 Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit code fixes
- ✨ Add new features
- 🧪 Add tests

## 🚀 Getting Started

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/ipo-intelligence-platform.git
cd ipo-intelligence-platform
```

### 3. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small

```python
def calculate_metric(data: Dict) -> float:
    """
    Calculate specific metric from financial data.
    
    Args:
        data: Dictionary with financial data
        
    Returns:
        Calculated metric value
    """
    # Implementation
    pass
```

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

```bash
# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=src --cov-report=html
```

### Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update relevant documentation files
- Add examples for new features

## 🔍 Pull Request Process

### 1. Make Your Changes

- Write clean, tested code
- Follow existing code style
- Add/update tests
- Update documentation

### 2. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git commit -m "Add feature: Multi-currency support for financial calculations"
# or
git commit -m "Fix bug: Handle empty PDF pages gracefully"
```

### 3. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 4. Create Pull Request

- Go to the original repository
- Click "New Pull Request"
- Select your fork and branch
- Fill in the PR template

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] All tests pass
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

## 🐛 Reporting Bugs

### Before Submitting

- Check existing issues
- Verify bug with latest version
- Collect relevant information

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., macOS 13]
- Python: [e.g., 3.9]
- Version: [e.g., 1.0.0]

**Additional Context**
Any other relevant information
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Problem Statement**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Mockups, examples, etc.
```

## 🏗️ Project Structure

Understanding the codebase:

```
src/
├── ingestion/      # Data collection
├── processing/     # PDF parsing
├── embeddings/     # RAG components
├── llm/           # LLM integration
├── analysis/      # Analysis modules
└── chatbot/       # Q&A system
```

## 🧪 Testing Guidelines

### Unit Tests

```python
def test_financial_calculator():
    """Test financial metric calculations"""
    calc = FinancialCalculator()
    data = {'revenue': {2023: 1000}}
    
    result = calc.calculate_metrics(data)
    assert result is not None
```

### Integration Tests

```python
def test_end_to_end_analysis():
    """Test complete analysis pipeline"""
    orchestrator = IPOAnalysisOrchestrator("Test", "output/")
    result = orchestrator.run_complete_analysis("test.pdf")
    
    assert 'business' in result
    assert 'financials' in result
```

## 📝 Documentation Standards

### Code Documentation

- Add docstrings to all public functions
- Include type hints
- Explain complex logic with comments

### README Updates

- Keep examples up to date
- Update feature lists
- Maintain installation instructions

## ⚡ Performance Guidelines

- Avoid unnecessary computations
- Use batch processing where possible
- Cache expensive operations
- Profile before optimizing

## 🔒 Security Guidelines

- Never commit API keys or secrets
- Use environment variables
- Validate user inputs
- Follow security best practices

## 📊 Code Review Process

PRs will be reviewed for:

- ✅ Functionality
- ✅ Code quality
- ✅ Test coverage
- ✅ Documentation
- ✅ Performance
- ✅ Security

## 🎓 Learning Resources

- [RAG Architecture](https://docs.anthropic.com)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Streamlit Docs](https://docs.streamlit.io)

## 💬 Communication

- **Issues**: For bugs and features
- **Discussions**: For questions and ideas
- **Pull Requests**: For code contributions

## 📅 Release Process

1. Version bump in `setup.py`
2. Update CHANGELOG.md
3. Create release tag
4. Publish release notes

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## ❓ Questions?

- Check [documentation](docs/)
- Open a discussion
- Ask in pull request

## 📜 Code of Conduct

Be respectful, inclusive, and constructive. We're building together!

---

**Thank you for contributing to IPO Intelligence Platform! 🚀**
