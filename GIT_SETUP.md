# 🚀 Git Setup & Deployment Guide

Complete guide to publishing your IPO Intelligence Platform to GitHub.

---

## 📋 Prerequisites

- Git installed on your system
- GitHub account created
- Project folder ready

---

## 🎯 Step-by-Step Git Setup

### Step 1: Initialize Git Repository

```bash
# Navigate to project directory
cd ipo_analyzer

# Initialize git
git init

# Check status
git status
```

### Step 2: Configure Git (First Time Only)

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

### Step 3: Create .gitignore

Already created! The `.gitignore` file excludes:
- Virtual environments (`venv/`)
- Python cache files (`__pycache__/`)
- Large data files (PDFs, models)
- IDE files (`.vscode/`, `.idea/`)
- Environment variables (`.env`)

### Step 4: Add Files to Git

```bash
# Add all files
git add .

# Check what will be committed
git status

# You should see files in green (staged for commit)
```

### Step 5: Create Initial Commit

```bash
# Create first commit
git commit -m "Initial commit: IPO Intelligence Platform - Complete RAG System"

# Verify commit
git log --oneline
```

---

## 🌐 Create GitHub Repository

### Option A: GitHub Web Interface

1. **Go to GitHub**
   - Visit https://github.com
   - Click "+" icon → "New repository"

2. **Repository Settings**
   - **Name**: `ipo-intelligence-platform`
   - **Description**: `Production-grade RAG system for IPO prospectus analysis with hybrid AI approach`
   - **Visibility**: Public (or Private)
   - **DO NOT** initialize with README (we already have one)
   - Click "Create repository"

3. **Copy Repository URL**
   - Copy the HTTPS or SSH URL shown

### Option B: GitHub CLI

```bash
# Install GitHub CLI (if not installed)
# macOS: brew install gh
# Windows: winget install GitHub.cli

# Login to GitHub
gh auth login

# Create repository
gh repo create ipo-intelligence-platform --public --description "Production-grade RAG system for IPO analysis"

# Repository will be created and remote will be added automatically
```

---

## 🔗 Connect Local Repository to GitHub

### If you created repo via web interface:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/ipo-intelligence-platform.git

# Verify remote
git remote -v

# Should show:
# origin  https://github.com/YOUR_USERNAME/ipo-intelligence-platform.git (fetch)
# origin  https://github.com/YOUR_USERNAME/ipo-intelligence-platform.git (push)
```

### If you used GitHub CLI:

Remote is already configured! Skip to next step.

---

## 📤 Push Code to GitHub

### First Push

```bash
# Push to GitHub
git push -u origin main

# If you get an error about 'master' vs 'main':
git branch -M main
git push -u origin main
```

### Verify Upload

1. Go to your GitHub repository page
2. Refresh the page
3. You should see all your files!

---

## 🎨 Customize Your Repository

### Add Topics (Tags)

On GitHub repository page:
1. Click "⚙️ Settings" (or the gear icon next to About)
2. Add topics:
   - `rag`
   - `llm`
   - `artificial-intelligence`
   - `financial-analysis`
   - `ipo-analysis`
   - `vector-database`
   - `faiss`
   - `ollama`
   - `streamlit`
   - `python`
   - `machine-learning`
   - `nlp`

### Update Repository Description

Click "⚙️" next to About and add:
- **Description**: `Production-grade RAG system for IPO prospectus analysis with hybrid AI (LLM + deterministic calculations). Features: FAISS vector search, local Ollama LLM, Streamlit dashboard, zero hallucination on financials.`
- **Website**: Add your demo URL if you have one
- **Topics**: As listed above

### Add Repository Social Preview

1. Go to Settings → General
2. Scroll to "Social preview"
3. Upload a screenshot of your Streamlit dashboard (optional)

---

## 📊 Enable GitHub Features

### Enable Issues

1. Go to Settings → Features
2. Check "Issues"
3. Create issue templates (optional)

### Enable Discussions

1. Go to Settings → Features
2. Check "Discussions"
3. Great for Q&A and community

### Enable GitHub Pages (for documentation)

1. Go to Settings → Pages
2. Source: Deploy from branch
3. Branch: main → /docs or /root
4. This will host your `index.html` at:
   `https://YOUR_USERNAME.github.io/ipo-intelligence-platform/`

---

## 🏷️ Create Release

### Tag Your First Version

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Initial release: Complete IPO Intelligence Platform"
git push origin v1.0.0
```

### Create GitHub Release

1. Go to Releases → "Draft a new release"
2. **Tag**: v1.0.0
3. **Title**: `v1.0.0 - Initial Release`
4. **Description**:

```markdown
# 🚀 IPO Intelligence Platform v1.0.0

Production-grade RAG system for IPO prospectus analysis.

## ✨ Features

- ✅ Complete RAG pipeline (SEBI → PDF → Analysis → Chatbot)
- ✅ 5,934 lines of production code
- ✅ Hybrid AI approach (LLM + deterministic calculations)
- ✅ Zero hallucination on financial metrics
- ✅ Beautiful Streamlit dashboard
- ✅ Comprehensive documentation

## 📦 What's Included

- Full source code
- Test suite
- Documentation (5 guides)
- Quick start script
- Example configurations

## 🚀 Quick Start

```bash
pip install -r requirements.txt
ollama pull mistral && ollama serve
python quickstart.py
```

## 📚 Documentation

- [Quick Start](README_QUICKSTART.md)
- [Setup Guide](SETUP_GUIDE.md)
- [Architecture](ARCHITECTURE.md)
- [Web Docs](index.html)

## 🎯 Built For

- Technical interviews
- Learning RAG architecture
- Production financial analysis
- AI system design patterns
```

5. Click "Publish release"

---

## 🔄 Daily Git Workflow

### Making Changes

```bash
# 1. Create a new branch for your feature
git checkout -b feature/new-analysis-module

# 2. Make your changes
# ... edit files ...

# 3. Check what changed
git status
git diff

# 4. Stage changes
git add .

# 5. Commit changes
git commit -m "Add: New industry comparison module"

# 6. Push to GitHub
git push origin feature/new-analysis-module

# 7. Create Pull Request on GitHub
# Go to repository → Pull Requests → New PR
```

### Syncing with Remote

```bash
# Get latest changes
git pull origin main

# If you have conflicts, resolve them
# Then commit the merge
git commit -m "Merge remote changes"
```

---

## 🎯 Best Practices

### Commit Messages

Use clear, descriptive messages:

```bash
# Good ✅
git commit -m "Add: Multi-currency support for financial calculations"
git commit -m "Fix: Handle empty PDF pages in parser"
git commit -m "Update: Improve chunking strategy for tables"
git commit -m "Docs: Add deployment guide"

# Bad ❌
git commit -m "updates"
git commit -m "fix bug"
git commit -m "changes"
```

### Commit Message Format

```
Type: Brief description (50 chars max)

Detailed explanation if needed (72 chars per line)

- Bullet points for multiple changes
- Reference issue numbers: Fixes #123
```

**Types**:
- `Add:` - New feature
- `Fix:` - Bug fix
- `Update:` - Improve existing feature
- `Docs:` - Documentation only
- `Test:` - Add/update tests
- `Refactor:` - Code restructuring
- `Style:` - Formatting changes

### Branching Strategy

```bash
# Main branches
main          # Production-ready code
develop       # Integration branch

# Feature branches
feature/name  # New features
bugfix/name   # Bug fixes
hotfix/name   # Urgent fixes
docs/name     # Documentation
```

---

## 🔐 Security Best Practices

### Never Commit

- ❌ API keys
- ❌ Passwords
- ❌ Private keys
- ❌ `.env` files
- ❌ Large data files

### Use Environment Variables

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
```

### Scan for Secrets

```bash
# Install git-secrets
brew install git-secrets  # macOS

# Initialize
git secrets --install
git secrets --register-aws

# Scan commits
git secrets --scan
```

---

## 📊 Advanced Git Commands

### View History

```bash
# Show commit history
git log --oneline --graph --all

# Show changes in last commit
git show

# Show who changed what
git blame filename.py
```

### Undo Changes

```bash
# Discard unstaged changes
git restore filename.py

# Unstage files
git restore --staged filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### Work with Branches

```bash
# List branches
git branch -a

# Delete branch
git branch -d feature/old-feature

# Rename branch
git branch -m old-name new-name
```

---

## 🚀 CI/CD Setup

### GitHub Actions

Already configured in `.github/workflows/ci.yml`!

**What it does**:
- ✅ Runs tests on every push
- ✅ Checks code formatting
- ✅ Runs security scans
- ✅ Tests on Python 3.9, 3.10, 3.11

### View Action Results

1. Go to "Actions" tab on GitHub
2. See test results for each commit
3. Fix any failing tests

---

## 📈 Repository Analytics

### GitHub Insights

Check these regularly:
1. **Traffic** - Views and clones
2. **Community** - Issues, PRs, discussions
3. **Contributors** - Who's contributing
4. **Commits** - Activity over time

### Add Badges to README

Already included in README.md:
- Python version
- License
- Build status
- etc.

---

## 🎓 Learning Resources

### Git Basics
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Interactive Git Tutorial](https://learngitbranching.js.org/)

### GitHub Features
- [GitHub Docs](https://docs.github.com)
- [GitHub Skills](https://skills.github.com)

---

## ❓ Troubleshooting

### Common Issues

**Issue**: "Permission denied (publickey)"
```bash
# Solution: Use HTTPS instead of SSH
git remote set-url origin https://github.com/USERNAME/REPO.git
```

**Issue**: "Updates were rejected"
```bash
# Solution: Pull first, then push
git pull origin main --rebase
git push origin main
```

**Issue**: "Merge conflicts"
```bash
# Solution: Resolve conflicts manually
# 1. Open conflicted files
# 2. Edit to resolve conflicts
# 3. Stage and commit
git add .
git commit -m "Resolve merge conflicts"
```

---

## ✅ Checklist for Publishing

Before making repository public:

- [ ] README.md is complete and professional
- [ ] .gitignore excludes sensitive files
- [ ] No API keys or secrets in code
- [ ] LICENSE file is present
- [ ] CONTRIBUTING.md explains how to contribute
- [ ] Tests are passing
- [ ] Documentation is up to date
- [ ] index.html works properly
- [ ] Example data is included (if applicable)

---

## 🎉 You're Ready!

Your repository is now:
- ✅ Version controlled
- ✅ Backed up on GitHub
- ✅ Shareable with others
- ✅ Portfolio-ready
- ✅ Collaborative

### Share Your Work

```bash
# Your repository URL:
https://github.com/YOUR_USERNAME/ipo-intelligence-platform

# Share on:
- LinkedIn
- Twitter
- Resume
- Portfolio website
```

---

## 📞 Next Steps

1. **Add to resume** - Include GitHub link
2. **Write blog post** - Explain your project
3. **Share on social media** - Get feedback
4. **Keep improving** - Regular updates
5. **Help others** - Answer issues

---

**Happy coding! 🚀**
