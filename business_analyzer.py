"""
Business Analyzer
Uses LLM to analyze business model, market position, and strategy from prospectus
CRITICAL: LLM for reasoning ONLY, not for numbers
"""

from typing import Dict, List, Optional
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BusinessAnalyzer:
    """
    Analyze business aspects using RAG with LLM
    """
    
    def __init__(self, vector_store, embedder, llm_client):
        """
        Initialize analyzer
        
        Args:
            vector_store: VectorStore instance
            embedder: Embedder instance
            llm_client: OllamaClient instance
        """
        self.vector_store = vector_store
        self.embedder = embedder
        self.llm = llm_client
    
    def analyze_business_model(self, top_k: int = 10) -> Dict:
        """
        Analyze business model from prospectus
        
        Returns:
            Dictionary with business model analysis
        """
        logger.info("Analyzing business model...")
        
        queries = [
            "What is the company's business model and how does it generate revenue?",
            "What products or services does the company offer?",
            "What is the company's value proposition?"
        ]
        
        # Retrieve relevant chunks
        all_chunks = []
        for query in queries:
            query_emb = self.embedder.embed_single(query)
            chunks = self.vector_store.search_by_section(
                query_emb, 
                section_type='business',
                top_k=top_k
            )
            all_chunks.extend(chunks)
        
        # Remove duplicates
        seen_ids = set()
        unique_chunks = []
        for chunk in all_chunks:
            chunk_id = chunk.get('global_chunk_id')
            if chunk_id not in seen_ids:
                seen_ids.add(chunk_id)
                unique_chunks.append(chunk)
        
        # Analyze with LLM
        analysis = self._generate_business_analysis(unique_chunks[:15])
        
        return {
            'business_model': analysis,
            'num_sources': len(unique_chunks),
            'confidence': 'high' if len(unique_chunks) >= 5 else 'medium'
        }
    
    def analyze_market_position(self, top_k: int = 10) -> Dict:
        """
        Analyze market position and competitive landscape
        """
        logger.info("Analyzing market position...")
        
        queries = [
            "What is the company's market position and market share?",
            "Who are the main competitors?",
            "What are the competitive advantages?"
        ]
        
        all_chunks = []
        for query in queries:
            query_emb = self.embedder.embed_single(query)
            chunks = self.vector_store.search_by_section(
                query_emb,
                section_type='business',
                top_k=top_k
            )
            all_chunks.extend(chunks)
        
        # Deduplicate
        unique_chunks = self._deduplicate_chunks(all_chunks)
        
        analysis = self._generate_market_analysis(unique_chunks[:15])
        
        return {
            'market_position': analysis,
            'num_sources': len(unique_chunks)
        }
    
    def analyze_operations(self, top_k: int = 10) -> Dict:
        """
        Analyze operational aspects
        """
        logger.info("Analyzing operations...")
        
        queries = [
            "What is the manufacturing capacity and utilization?",
            "What is the supply chain structure?",
            "What are the operational dependencies?"
        ]
        
        all_chunks = []
        for query in queries:
            query_emb = self.embedder.embed_single(query)
            chunks = self.vector_store.search_by_section(
                query_emb,
                section_type='business',
                top_k=top_k
            )
            all_chunks.extend(chunks)
        
        unique_chunks = self._deduplicate_chunks(all_chunks)
        
        analysis = self._generate_operations_analysis(unique_chunks[:15])
        
        return {
            'operations': analysis,
            'num_sources': len(unique_chunks)
        }
    
    def analyze_customers(self, top_k: int = 10) -> Dict:
        """
        Analyze customer base and concentration
        """
        logger.info("Analyzing customer base...")
        
        queries = [
            "Who are the major customers?",
            "What is the customer concentration?",
            "Is there customer dependency risk?"
        ]
        
        all_chunks = []
        for query in queries:
            query_emb = self.embedder.embed_single(query)
            chunks = self.vector_store.search(query_emb, top_k=top_k)
            all_chunks.extend(chunks)
        
        unique_chunks = self._deduplicate_chunks(all_chunks)
        
        analysis = self._generate_customer_analysis(unique_chunks[:10])
        
        return {
            'customers': analysis,
            'num_sources': len(unique_chunks)
        }
    
    def comprehensive_business_analysis(self) -> Dict:
        """
        Run complete business analysis
        """
        logger.info("Running comprehensive business analysis...")
        
        return {
            'business_model': self.analyze_business_model(),
            'market_position': self.analyze_market_position(),
            'operations': self.analyze_operations(),
            'customers': self.analyze_customers(),
            'summary': self._generate_executive_summary()
        }
    
    def _generate_business_analysis(self, chunks: List[Dict]) -> str:
        """
        Generate business model analysis using LLM
        """
        context = self._build_context(chunks)
        
        prompt = f"""Based on the following excerpts from an IPO prospectus, analyze the company's business model.

Context:
{context}

Provide a structured analysis covering:
1. Core Business Model (how the company makes money)
2. Key Products/Services
3. Value Proposition
4. Revenue Streams

CRITICAL: Base your analysis ONLY on the provided context. Do not make up information.
If certain details are not available, state that clearly.

Analysis:"""
        
        system_prompt = """You are a business analyst specializing in IPO prospectus analysis.
Your role is to extract and synthesize information about business models.
NEVER invent facts or numbers. Only use information from the provided context."""
        
        response = self.llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.1,
            max_tokens=1024
        )
        
        return response.strip()
    
    def _generate_market_analysis(self, chunks: List[Dict]) -> str:
        """
        Generate market position analysis
        """
        context = self._build_context(chunks)
        
        prompt = f"""Analyze the company's market position based on this prospectus information:

{context}

Cover:
1. Market Position & Share
2. Competitive Landscape
3. Key Competitors (if mentioned)
4. Competitive Advantages
5. Market Trends

Only use information from the context. State if information is unavailable.

Analysis:"""
        
        response = self.llm.generate(
            prompt=prompt,
            system_prompt="You are a market analyst. Extract facts from context only.",
            temperature=0.1
        )
        
        return response.strip()
    
    def _generate_operations_analysis(self, chunks: List[Dict]) -> str:
        """
        Generate operations analysis
        """
        context = self._build_context(chunks)
        
        prompt = f"""Analyze operational aspects from this prospectus:

{context}

Focus on:
1. Manufacturing/Operations Capacity
2. Capacity Utilization
3. Supply Chain Dependencies
4. Key Operational Risks
5. Expansion Plans

Base analysis strictly on provided context.

Analysis:"""
        
        response = self.llm.generate(
            prompt=prompt,
            temperature=0.1
        )
        
        return response.strip()
    
    def _generate_customer_analysis(self, chunks: List[Dict]) -> str:
        """
        Generate customer base analysis
        """
        context = self._build_context(chunks)
        
        prompt = f"""Analyze the customer base from prospectus:

{context}

Address:
1. Major Customers (if disclosed)
2. Customer Concentration Risk
3. Geographic Distribution
4. Customer Dependencies

Extract only what is stated in the context.

Analysis:"""
        
        response = self.llm.generate(prompt=prompt, temperature=0.1)
        return response.strip()
    
    def _generate_executive_summary(self) -> str:
        """
        Generate executive summary of business
        """
        # This would combine all analyses
        return "Executive summary of business analysis"
    
    def _build_context(self, chunks: List[Dict]) -> str:
        """
        Build context from chunks
        """
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            text = chunk['text']
            context_parts.append(f"[Excerpt {i}]\n{text}")
        
        return "\n\n".join(context_parts)
    
    def _deduplicate_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Remove duplicate chunks
        """
        seen_ids = set()
        unique = []
        
        for chunk in chunks:
            chunk_id = chunk.get('global_chunk_id')
            if chunk_id not in seen_ids:
                seen_ids.add(chunk_id)
                unique.append(chunk)
        
        return unique


def main():
    """Test business analyzer"""
    print("Business Analyzer - Requires running vector store and LLM")
    print("This module integrates with the RAG pipeline")


if __name__ == "__main__":
    main()
