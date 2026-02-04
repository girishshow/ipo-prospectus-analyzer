"""
Comprehensive Test Suite for IPO Intelligence Platform
Tests each module independently and integration
"""

import pytest
import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestEmbeddings:
    """Test embedding functionality"""
    
    def test_embedder_initialization(self):
        """Test embedder can be initialized"""
        from src.embeddings.embedder import Embedder
        
        embedder = Embedder()
        assert embedder is not None
        assert embedder.embedding_dim == 384
    
    def test_single_embedding(self):
        """Test single text embedding"""
        from src.embeddings.embedder import Embedder
        
        embedder = Embedder()
        text = "This is a test sentence"
        embedding = embedder.embed_single(text)
        
        assert embedding.shape == (384,)
        assert isinstance(embedding, np.ndarray)
    
    def test_batch_embedding(self):
        """Test batch embedding"""
        from src.embeddings.embedder import Embedder
        
        embedder = Embedder()
        texts = ["Text one", "Text two", "Text three"]
        embeddings = embedder.embed_texts(texts)
        
        assert embeddings.shape == (3, 384)
    
    def test_similarity_computation(self):
        """Test similarity calculation"""
        from src.embeddings.embedder import Embedder
        
        embedder = Embedder()
        emb1 = embedder.embed_single("The cat sat on the mat")
        emb2 = embedder.embed_single("The cat is sitting on the mat")
        emb3 = embedder.embed_single("The dog ran in the park")
        
        sim_similar = embedder.compute_similarity(emb1, emb2)
        sim_different = embedder.compute_similarity(emb1, emb3)
        
        # Similar sentences should have higher similarity
        assert sim_similar > sim_different


class TestChunking:
    """Test chunking functionality"""
    
    def test_chunker_initialization(self):
        """Test chunker initialization"""
        from src.embeddings.chunker import SemanticChunker
        
        chunker = SemanticChunker(chunk_size=512, overlap_ratio=0.15)
        assert chunker.chunk_size == 512
        assert chunker.overlap_tokens == 76
    
    def test_basic_chunking(self):
        """Test basic text chunking"""
        from src.embeddings.chunker import SemanticChunker
        
        chunker = SemanticChunker(chunk_size=50, overlap_ratio=0.2)
        
        text = " ".join(["word"] * 200)  # 200 words
        chunks = chunker.chunk_text(text)
        
        assert len(chunks) > 0
        assert all('text' in chunk for chunk in chunks)
    
    def test_section_splitting(self):
        """Test section-aware chunking"""
        from src.embeddings.chunker import SemanticChunker
        
        chunker = SemanticChunker()
        
        text = """
        Risk Factors
        
        The company faces various risks.
        
        Financial Statements
        
        Revenue was Rs. 1000 crore.
        """
        
        chunks = chunker.chunk_document(text, extract_sections=True)
        
        # Should create chunks with section types
        sections = set(c['section_type'] for c in chunks)
        assert len(sections) > 0


class TestVectorStore:
    """Test vector store functionality"""
    
    def test_vector_store_initialization(self):
        """Test vector store init"""
        from src.embeddings.vector_store import VectorStore
        
        vs = VectorStore()
        assert vs.index.ntotal == 0
    
    def test_add_and_search(self):
        """Test adding and searching vectors"""
        from src.embeddings.vector_store import VectorStore
        from src.embeddings.embedder import Embedder
        
        embedder = Embedder()
        vs = VectorStore()
        
        # Create sample chunks
        chunks = [
            {'text': 'Financial data', 'section_type': 'financials', 'global_chunk_id': 0},
            {'text': 'Risk information', 'section_type': 'risks', 'global_chunk_id': 1},
            {'text': 'Business model', 'section_type': 'business', 'global_chunk_id': 2}
        ]
        
        # Add embeddings
        chunks = embedder.embed_chunks(chunks)
        vs.add_chunks(chunks)
        
        assert vs.index.ntotal == 3
        
        # Search
        query_emb = embedder.embed_single("What are the financials?")
        results = vs.search(query_emb, top_k=2)
        
        assert len(results) > 0
        assert all('similarity_score' in r for r in results)


class TestFinancialCalculator:
    """Test financial calculations"""
    
    def test_calculator_initialization(self):
        """Test calculator init"""
        from src.analysis.financial_calculator import FinancialCalculator
        
        calc = FinancialCalculator()
        assert calc is not None
    
    def test_basic_metrics(self):
        """Test basic financial metrics"""
        from src.analysis.financial_calculator import FinancialCalculator
        
        calc = FinancialCalculator()
        
        data = {
            'revenue': {2021: 800, 2022: 900, 2023: 1000},
            'ebitda': {2021: 150, 2022: 180, 2023: 200},
            'pat': {2021: 80, 2022: 100, 2023: 120}
        }
        
        metrics = calc.calculate_all_metrics(data)
        
        assert 'basic_metrics' in metrics
        assert 'ebitda_margin' in metrics['basic_metrics']
    
    def test_growth_calculation(self):
        """Test growth metrics calculation"""
        from src.analysis.financial_calculator import FinancialCalculator
        
        calc = FinancialCalculator()
        
        data = {
            'revenue': {2021: 800, 2022: 900, 2023: 1000}
        }
        
        metrics = calc.calculate_all_metrics(data)
        growth = metrics['growth_metrics']
        
        assert 'revenue_yoy' in growth
        assert 'revenue_cagr_3y' in growth
    
    def test_ratios(self):
        """Test financial ratios"""
        from src.analysis.financial_calculator import FinancialCalculator
        
        calc = FinancialCalculator()
        
        data = {
            'total_debt': {2023: 200},
            'equity': {2023: 400},
            'current_assets': {2023: 300},
            'current_liabilities': {2023: 150}
        }
        
        metrics = calc.calculate_all_metrics(data)
        ratios = metrics['ratios']
        
        # Debt-to-equity should be 0.5
        assert abs(ratios['debt_to_equity'][2023] - 0.5) < 0.01
        
        # Current ratio should be 2.0
        assert abs(ratios['current_ratio'][2023] - 2.0) < 0.01
    
    def test_no_llm_usage(self):
        """Verify NO LLM is used in calculations"""
        from src.analysis.financial_calculator import FinancialCalculator
        
        # This test ensures the calculator module doesn't import LLM
        calc = FinancialCalculator()
        
        # Calculator should not have any LLM attributes
        assert not hasattr(calc, 'llm')
        assert not hasattr(calc, 'model')


class TestRecommendationEngine:
    """Test recommendation engine"""
    
    def test_scoring(self):
        """Test multi-factor scoring"""
        from src.recommendation.scorer import RecommendationEngine
        
        engine = RecommendationEngine()
        
        analysis = {
            'financials': {
                'basic_metrics': {'ebitda_margin': {2023: 20}},
                'growth_metrics': {'revenue_cagr_3y': 15},
                'ratios': {'debt_to_equity': {2023: 0.5}}
            },
            'risks': {'risk_score': 40}
        }
        
        scores = engine.calculate_scores(analysis)
        
        assert 'business_score' in scores
        assert 'financial_score' in scores
        assert all(0 <= score <= 100 for score in scores.values())
    
    def test_stance_determination(self):
        """Test investment stance logic"""
        from src.recommendation.scorer import RecommendationEngine
        
        engine = RecommendationEngine()
        
        assert engine.determine_stance(80) == 'Conservative - Positive'
        assert engine.determine_stance(65) == 'Neutral'
        assert engine.determine_stance(55) == 'Aggressive - Speculative'
        assert engine.determine_stance(45) == 'Avoid'


class TestIntegration:
    """Integration tests"""
    
    def test_end_to_end_chunk_search(self):
        """Test complete chunking -> embedding -> search pipeline"""
        from src.embeddings.chunker import SemanticChunker
        from src.embeddings.embedder import Embedder
        from src.embeddings.vector_store import VectorStore
        
        # Sample text
        text = """
        Risk Factors: Customer concentration is a major risk.
        
        Financial Performance: Revenue grew 25% to Rs. 1000 crore.
        """
        
        # Chunk
        chunker = SemanticChunker(chunk_size=50)
        chunks = chunker.chunk_document(text, extract_sections=True)
        
        # Embed
        embedder = Embedder()
        chunks = embedder.embed_chunks(chunks)
        
        # Store
        vs = VectorStore()
        vs.add_chunks(chunks)
        
        # Search
        query_emb = embedder.embed_single("What are the risks?")
        results = vs.search(query_emb, top_k=2)
        
        assert len(results) > 0
        # Result should mention risk/customer
        assert any('risk' in r['text'].lower() or 'customer' in r['text'].lower() 
                  for r in results)


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("RUNNING TEST SUITE FOR IPO INTELLIGENCE PLATFORM")
    print("="*70 + "\n")
    
    # Run with pytest
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == "__main__":
    run_all_tests()
