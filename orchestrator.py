"""
Analysis Orchestrator
Coordinates all analysis modules to generate complete IPO analysis
"""

import json
from typing import Dict, Optional
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IPOAnalysisOrchestrator:
    """
    Orchestrates complete IPO analysis pipeline
    """
    
    def __init__(self, company_name: str, output_dir: Path):
        self.company_name = company_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Components (initialized when needed)
        self.vector_store = None
        self.embedder = None
        self.llm = None
        self.pdf_parser = None
        
        # Analysis results
        self.results = {}
    
    def initialize_components(self):
        """
        Initialize all required components
        """
        logger.info("Initializing analysis components...")
        
        try:
            from src.embeddings.embedder import Embedder
            from src.embeddings.vector_store import VectorStore
            from src.llm.ollama_client import OllamaClient
            
            self.embedder = Embedder()
            self.vector_store = VectorStore()
            self.llm = OllamaClient()
            
            logger.info("Components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing components: {e}")
            return False
    
    def run_complete_analysis(self, pdf_path: Path) -> Dict:
        """
        Run complete analysis pipeline
        
        Args:
            pdf_path: Path to IPO prospectus PDF
            
        Returns:
            Dictionary with all analysis results
        """
        logger.info(f"Starting complete analysis for {self.company_name}")
        
        # Step 1: Process PDF
        logger.info("Step 1/7: Processing PDF...")
        processed_data = self.process_pdf(pdf_path)
        if not processed_data:
            logger.error("PDF processing failed")
            return {}
        
        # Step 2: Build vector store
        logger.info("Step 2/7: Building vector store...")
        if not self.build_vector_store(processed_data):
            logger.error("Vector store creation failed")
            return {}
        
        # Step 3: Business analysis
        logger.info("Step 3/7: Analyzing business...")
        self.results['business'] = self.analyze_business()
        
        # Step 4: Financial analysis
        logger.info("Step 4/7: Analyzing financials...")
        self.results['financials'] = self.analyze_financials(processed_data)
        
        # Step 5: Risk analysis
        logger.info("Step 5/7: Analyzing risks...")
        self.results['risks'] = self.analyze_risks()
        
        # Step 6: IPO details
        logger.info("Step 6/7: Extracting IPO details...")
        self.results['ipo_details'] = self.analyze_ipo_details()
        
        # Step 7: Generate recommendation
        logger.info("Step 7/7: Generating recommendation...")
        self.results['recommendation'] = self.generate_recommendation()
        
        # Save results
        self.save_results()
        
        logger.info("Analysis complete!")
        return self.results
    
    def process_pdf(self, pdf_path: Path) -> Optional[Dict]:
        """
        Process PDF and extract data
        """
        try:
            from src.processing.pdf_parser import PDFParser
            
            with PDFParser(pdf_path) as parser:
                data = parser.extract_all()
            
            return data
            
        except Exception as e:
            logger.error(f"Error processing PDF: {e}")
            return None
    
    def build_vector_store(self, processed_data: Dict) -> bool:
        """
        Build vector store from processed data
        """
        try:
            from src.embeddings.chunker import SemanticChunker
            
            # Chunk text
            chunker = SemanticChunker()
            full_text = '\n\n'.join(processed_data['text'])
            chunks = chunker.chunk_document(full_text, extract_sections=True)
            
            # Add table chunks
            for table in processed_data.get('tables', []):
                table_chunk = chunker.chunk_table(table)
                chunks.append(table_chunk)
            
            # Create embeddings
            chunks = self.embedder.embed_chunks(chunks)
            
            # Build vector store
            self.vector_store.add_chunks(chunks)
            
            # Save vector store
            vs_path = self.output_dir / f"{self.company_name}_vectorstore"
            self.vector_store.save(vs_path)
            
            logger.info(f"Vector store built with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error building vector store: {e}")
            return False
    
    def analyze_business(self) -> Dict:
        """
        Run business analysis
        """
        try:
            from src.analysis.business_analyzer import BusinessAnalyzer
            
            analyzer = BusinessAnalyzer(self.vector_store, self.embedder, self.llm)
            analysis = analyzer.comprehensive_business_analysis()
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in business analysis: {e}")
            return {'error': str(e)}
    
    def analyze_financials(self, processed_data: Dict) -> Dict:
        """
        Run financial analysis (NO LLM)
        """
        try:
            from src.analysis.financial_calculator import FinancialCalculator
            from src.processing.table_extractor import TableExtractor
            
            # Extract financial tables
            extractor = TableExtractor()
            statements = extractor.extract_financial_statements(
                processed_data.get('tables', [])
            )
            
            # Build financial data
            financial_data = extractor.build_financial_data_dict(statements)
            
            # Calculate metrics
            calculator = FinancialCalculator()
            metrics = calculator.calculate_all_metrics(financial_data)
            
            return {
                'raw_data': financial_data,
                'metrics': metrics,
                'statements': {k: v.to_dict() if v is not None else None 
                              for k, v in statements.items()}
            }
            
        except Exception as e:
            logger.error(f"Error in financial analysis: {e}")
            return {'error': str(e)}
    
    def analyze_risks(self) -> Dict:
        """
        Run risk analysis
        """
        try:
            from src.analysis.risk_analyzer import RiskAnalyzer
            
            analyzer = RiskAnalyzer(self.vector_store, self.embedder, self.llm)
            risk_analysis = analyzer.analyze_all_risks()
            
            # Calculate risk score
            risk_score = analyzer.get_risk_score(
                risk_analysis.get('severity_analysis', {})
            )
            risk_analysis['risk_score'] = risk_score
            
            return risk_analysis
            
        except Exception as e:
            logger.error(f"Error in risk analysis: {e}")
            return {'error': str(e)}
    
    def analyze_ipo_details(self) -> Dict:
        """
        Extract IPO details
        """
        try:
            # Query for IPO details
            query = "What is the IPO size, fresh issue, offer for sale, and use of proceeds?"
            query_emb = self.embedder.embed_single(query)
            
            chunks = self.vector_store.search_by_section(
                query_emb,
                section_type='ipo_details',
                top_k=10
            )
            
            if not chunks:
                chunks = self.vector_store.search(query_emb, top_k=10)
            
            # Use LLM to extract details
            context = '\n\n'.join([c['text'] for c in chunks[:5]])
            
            prompt = f"""Extract IPO details from this prospectus text:

{context}

Provide:
1. Total issue size
2. Fresh issue amount
3. Offer for sale amount
4. Use of proceeds (breakdown)
5. Price band (if mentioned)

Format clearly. State if information not available.

IPO Details:"""
            
            response = self.llm.generate(
                prompt=prompt,
                system_prompt="Extract IPO details from prospectus text.",
                temperature=0.1
            )
            
            return {
                'extracted_details': response.strip(),
                'num_sources': len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Error extracting IPO details: {e}")
            return {'error': str(e)}
    
    def generate_recommendation(self) -> Dict:
        """
        Generate investment recommendation
        """
        try:
            from src.recommendation.scorer import RecommendationEngine
            
            engine = RecommendationEngine(self.llm)
            recommendation = engine.generate_recommendation(self.results)
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error generating recommendation: {e}")
            return {'error': str(e)}
    
    def save_results(self):
        """
        Save analysis results to file
        """
        output_file = self.output_dir / f"{self.company_name}_analysis.json"
        
        # Prepare serializable results
        serializable_results = self._make_serializable(self.results)
        
        with open(output_file, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        logger.info(f"Results saved to {output_file}")
    
    def _make_serializable(self, obj):
        """
        Convert objects to JSON-serializable format
        """
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        else:
            return str(obj)
    
    def load_existing_analysis(self) -> Optional[Dict]:
        """
        Load previously saved analysis
        """
        output_file = self.output_dir / f"{self.company_name}_analysis.json"
        
        if output_file.exists():
            with open(output_file, 'r') as f:
                return json.load(f)
        
        return None


def main():
    """
    Example usage
    """
    import sys
    from pathlib import Path
    
    if len(sys.argv) < 3:
        print("Usage: python orchestrator.py <company_name> <pdf_path>")
        sys.exit(1)
    
    company_name = sys.argv[1]
    pdf_path = Path(sys.argv[2])
    
    if not pdf_path.exists():
        print(f"Error: PDF not found: {pdf_path}")
        sys.exit(1)
    
    # Create orchestrator
    output_dir = Path("data/processed")
    orchestrator = IPOAnalysisOrchestrator(company_name, output_dir)
    
    # Initialize
    if not orchestrator.initialize_components():
        print("Failed to initialize components")
        sys.exit(1)
    
    # Run analysis
    print(f"\nAnalyzing {company_name}...")
    print("="*80)
    
    results = orchestrator.run_complete_analysis(pdf_path)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"\nResults saved to: {output_dir}/{company_name}_analysis.json")
    
    # Print summary
    if 'recommendation' in results:
        rec = results['recommendation']
        print(f"\nOverall Score: {rec.get('overall_score', 'N/A')}/100")
        print(f"Stance: {rec.get('stance', 'N/A')}")


if __name__ == "__main__":
    main()
