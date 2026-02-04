#!/usr/bin/env python3
"""
Quick Start Script for IPO Intelligence Platform
Run this to test the system with sample data
"""

import sys
import subprocess
from pathlib import Path
import time

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════╗
║          IPO INTELLIGENCE PLATFORM - QUICK START          ║
║                                                           ║
║     Domain-Specific RAG System for IPO Analysis          ║
╚═══════════════════════════════════════════════════════════╝
    """)

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required = [
        'streamlit',
        'pdfplumber',
        'sentence_transformers',
        'faiss',
        'pandas',
        'requests',
        'beautifulsoup4',
        'plotly'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("\n✓ All dependencies installed")
    return True

def check_ollama():
    """Check if Ollama is running"""
    print("\n🤖 Checking Ollama...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"  ✓ Ollama is running")
            
            # Check for mistral or llama
            model_names = [m['name'] for m in models]
            if any('mistral' in name for name in model_names):
                print("  ✓ Mistral model found")
                return True
            elif any('llama' in name for name in model_names):
                print("  ✓ LLaMA model found")
                return True
            else:
                print("  ⚠️  No supported model found")
                print("  Run: ollama pull mistral")
                return False
    except:
        print("  ✗ Ollama not running")
        print("\n  To start Ollama:")
        print("    1. Install from: https://ollama.ai")
        print("    2. Run: ollama serve")
        print("    3. Pull model: ollama pull mistral")
        return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    print("\n📁 Setting up directories...")
    
    dirs = [
        'data/raw',
        'data/processed',
        'data/embeddings',
        'data/external',
        'models/embeddings'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {dir_path}")
    
    print("\n✓ Directories created")

def create_sample_data():
    """Create sample data for testing"""
    print("\n📄 Creating sample data...")
    
    sample_text = """
SAMPLE IPO PROSPECTUS - DEMO COMPANY LIMITED

BUSINESS OVERVIEW
Demo Company Limited is engaged in the manufacturing and distribution of technology products.
We operate three manufacturing facilities with a combined capacity of 100,000 units per year.
Current capacity utilization stands at 75%.

Our business model focuses on B2B sales to enterprise customers. Top 5 customers account for
45% of revenue, creating concentration risk.

FINANCIAL HIGHLIGHTS
                        FY 2021    FY 2022    FY 2023
Revenue (Rs. Cr)          800        900       1000
EBITDA (Rs. Cr)           150        180        200
PAT (Rs. Cr)               80        100        120
Total Assets              1000       1100      1200
Equity                     400        480        580

RISK FACTORS
1. Customer Concentration: Heavy dependence on top customers
2. Regulatory Risk: Subject to government regulations
3. Competition: Increasing competition in the sector
4. Supply Chain: Dependent on imported components

IPO DETAILS
Total Issue Size: Rs. 800 Crore
- Fresh Issue: Rs. 500 Crore
- Offer for Sale: Rs. 300 Crore

Use of Proceeds:
- Capacity Expansion: 40%
- Debt Repayment: 30%
- Working Capital: 20%
- General Corporate: 10%
"""
    
    sample_file = Path('data/raw/sample_ipo_data.txt')
    with open(sample_file, 'w') as f:
        f.write(sample_text)
    
    print(f"  ✓ Sample data created: {sample_file}")

def run_tests():
    """Run basic tests"""
    print("\n🧪 Running basic tests...")
    
    # Test embedder
    try:
        from src.embeddings.embedder import Embedder
        embedder = Embedder()
        test_emb = embedder.embed_single("test text")
        print(f"  ✓ Embedder working (dim={len(test_emb)})")
    except Exception as e:
        print(f"  ✗ Embedder failed: {e}")
        return False
    
    # Test vector store
    try:
        from src.embeddings.vector_store import VectorStore
        vs = VectorStore()
        print("  ✓ Vector store initialized")
    except Exception as e:
        print(f"  ✗ Vector store failed: {e}")
        return False
    
    # Test financial calculator
    try:
        from src.analysis.financial_calculator import FinancialCalculator
        calc = FinancialCalculator()
        print("  ✓ Financial calculator ready")
    except Exception as e:
        print(f"  ✗ Financial calculator failed: {e}")
        return False
    
    print("\n✓ All tests passed")
    return True

def start_streamlit():
    """Start Streamlit app"""
    print("\n🚀 Starting Streamlit app...")
    print("\n" + "="*60)
    print("The application will open in your browser shortly.")
    print("If it doesn't, navigate to: http://localhost:8501")
    print("="*60 + "\n")
    
    try:
        subprocess.run(['streamlit', 'run', 'main.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
    except Exception as e:
        print(f"\n✗ Error starting Streamlit: {e}")
        print("\nYou can start manually with: streamlit run main.py")

def main():
    print_banner()
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("⚠️  Python 3.9+ required")
        sys.exit(1)
    
    # Run checks
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        sys.exit(1)
    
    ollama_ok = check_ollama()
    if not ollama_ok:
        print("\n⚠️  Ollama not ready. Some features will be limited.")
        print("Continue anyway? (y/n): ", end='')
        if input().lower() != 'y':
            sys.exit(1)
    
    setup_directories()
    create_sample_data()
    
    if not run_tests():
        print("\n❌ Tests failed. Please check your installation.")
        sys.exit(1)
    
    print("\n✅ System ready!")
    print("\nWhat would you like to do?")
    print("  1. Start Streamlit app (recommended)")
    print("  2. Run CLI demo")
    print("  3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        start_streamlit()
    elif choice == '2':
        print("\nCLI demo coming soon. Use Streamlit app for now.")
    else:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
