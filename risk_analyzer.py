"""
Risk Analyzer
Extracts and classifies risks from IPO prospectus using RAG + LLM
"""

from typing import List, Dict, Tuple
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskAnalyzer:
    """
    Analyze and classify risks from prospectus
    """
    
    def __init__(self, vector_store, embedder, llm_client):
        self.vector_store = vector_store
        self.embedder = embedder
        self.llm = llm_client
        
        self.risk_categories = {
            'business_risk': ['business model', 'operations', 'product'],
            'financial_risk': ['debt', 'cash flow', 'profitability', 'liquidity'],
            'operational_risk': ['supply chain', 'manufacturing', 'capacity'],
            'regulatory_risk': ['government', 'regulation', 'compliance', 'policy'],
            'legal_risk': ['litigation', 'legal proceedings', 'lawsuit'],
            'market_risk': ['competition', 'market share', 'pricing'],
            'promoter_risk': ['promoter', 'management', 'related party'],
            'customer_concentration_risk': ['customer concentration', 'major customers']
        }
    
    def analyze_all_risks(self) -> Dict:
        """
        Comprehensive risk analysis
        """
        logger.info("Analyzing all risk factors...")
        
        # Get all risks from risk section
        risks = self.extract_risk_factors()
        
        # Classify risks
        classified_risks = self.classify_risks(risks)
        
        # Assess severity
        severity_analysis = self.assess_severity(classified_risks)
        
        # Generate summary
        summary = self.generate_risk_summary(severity_analysis)
        
        return {
            'all_risks': risks,
            'classified_risks': classified_risks,
            'severity_analysis': severity_analysis,
            'summary': summary,
            'total_risks': len(risks)
        }
    
    def extract_risk_factors(self, top_k: int = 20) -> List[Dict]:
        """
        Extract risk factors from prospectus
        """
        logger.info("Extracting risk factors...")
        
        # Query for risks
        query = "What are all the risk factors mentioned in the prospectus?"
        query_emb = self.embedder.embed_single(query)
        
        # Search in risk section
        chunks = self.vector_store.search_by_section(
            query_emb,
            section_type='risks',
            top_k=top_k
        )
        
        if not chunks:
            # Fallback to general search
            chunks = self.vector_store.search(query_emb, top_k=top_k)
        
        # Extract individual risks using LLM
        risks = self._extract_individual_risks(chunks)
        
        return risks
    
    def _extract_individual_risks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Use LLM to extract individual risk items from chunks
        """
        context = '\n\n'.join([c['text'] for c in chunks[:10]])
        
        prompt = f"""From the following risk factors section of an IPO prospectus, extract individual risks.

Risk Factors Text:
{context}

For each risk, provide:
1. Risk title (brief)
2. Risk description (one sentence)

Format your response as a numbered list.

Extracted Risks:"""
        
        response = self.llm.generate(
            prompt=prompt,
            system_prompt="Extract risks from prospectus. Be factual and concise.",
            temperature=0.1,
            max_tokens=2048
        )
        
        # Parse response into structured format
        risks = self._parse_risk_response(response)
        
        return risks
    
    def _parse_risk_response(self, response: str) -> List[Dict]:
        """
        Parse LLM response into structured risk list
        """
        risks = []
        lines = response.split('\n')
        
        current_risk = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if it's a numbered item
            if line[0].isdigit() or line.startswith('-'):
                # Extract risk title and description
                # Simple parsing - could be improved
                parts = line.split(':', 1)
                if len(parts) == 2:
                    title = parts[0].strip('0123456789.-) ')
                    description = parts[1].strip()
                else:
                    title = line.strip('0123456789.-) ')
                    description = ""
                
                risks.append({
                    'title': title,
                    'description': description,
                    'category': None,  # Will be set in classification
                    'severity': None   # Will be set in severity analysis
                })
        
        return risks
    
    def classify_risks(self, risks: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Classify risks into categories
        """
        logger.info("Classifying risks...")
        
        classified = {category: [] for category in self.risk_categories.keys()}
        classified['other'] = []
        
        for risk in risks:
            category = self._classify_single_risk(risk)
            risk['category'] = category
            classified[category].append(risk)
        
        return classified
    
    def _classify_single_risk(self, risk: Dict) -> str:
        """
        Classify a single risk into category
        """
        risk_text = (risk['title'] + ' ' + risk['description']).lower()
        
        # Score each category
        category_scores = {}
        for category, keywords in self.risk_categories.items():
            score = sum(1 for keyword in keywords if keyword in risk_text)
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score
        if category_scores:
            return max(category_scores, key=category_scores.get)
        else:
            return 'other'
    
    def assess_severity(self, classified_risks: Dict[str, List[Dict]]) -> Dict:
        """
        Assess severity of each risk
        """
        logger.info("Assessing risk severity...")
        
        severity_analysis = {}
        
        for category, risks in classified_risks.items():
            if not risks:
                continue
            
            # Assess each risk
            for risk in risks:
                severity = self._assess_risk_severity(risk)
                risk['severity'] = severity
            
            # Category-level summary
            severity_counts = {
                'high': sum(1 for r in risks if r['severity'] == 'High'),
                'medium': sum(1 for r in risks if r['severity'] == 'Medium'),
                'low': sum(1 for r in risks if r['severity'] == 'Low')
            }
            
            severity_analysis[category] = {
                'risks': risks,
                'count': len(risks),
                'severity_breakdown': severity_counts
            }
        
        return severity_analysis
    
    def _assess_risk_severity(self, risk: Dict) -> str:
        """
        Assess severity of a single risk
        
        Uses keyword-based heuristics
        """
        text = (risk['title'] + ' ' + risk['description']).lower()
        
        # High severity indicators
        high_indicators = [
            'significant', 'material', 'substantial', 'major',
            'critical', 'severe', 'adversely affect', 'inability',
            'failure', 'default', 'litigation', 'regulatory action'
        ]
        
        # Medium severity indicators
        medium_indicators = [
            'may affect', 'could impact', 'potential', 'possible',
            'risk of', 'uncertainty', 'dependent', 'reliant'
        ]
        
        # Count indicators
        high_count = sum(1 for indicator in high_indicators if indicator in text)
        medium_count = sum(1 for indicator in medium_indicators if indicator in text)
        
        # Determine severity
        if high_count >= 2:
            return 'High'
        elif high_count >= 1 or medium_count >= 2:
            return 'Medium'
        else:
            return 'Low'
    
    def generate_risk_summary(self, severity_analysis: Dict) -> str:
        """
        Generate risk summary using LLM
        """
        # Prepare summary of key risks
        key_risks = []
        for category, data in severity_analysis.items():
            high_risks = [r for r in data['risks'] if r['severity'] == 'High']
            if high_risks:
                key_risks.extend(high_risks[:2])  # Top 2 from each category
        
        if not key_risks:
            return "No major risks identified in prospectus."
        
        # Build context
        risk_list = '\n'.join([
            f"- {r['title']}: {r['description']} [Category: {r['category']}, Severity: {r['severity']}]"
            for r in key_risks[:10]
        ])
        
        prompt = f"""Summarize the key risks for this IPO based on the following risk factors:

{risk_list}

Provide a concise executive summary of the major risks an investor should be aware of.
Focus on the most material risks.

Summary:"""
        
        response = self.llm.generate(
            prompt=prompt,
            system_prompt="Summarize IPO risks clearly and objectively.",
            temperature=0.2,
            max_tokens=512
        )
        
        return response.strip()
    
    def get_risk_score(self, severity_analysis: Dict) -> float:
        """
        Calculate overall risk score (0-100, lower is better)
        
        More high-severity risks = higher score (worse)
        """
        total_risks = 0
        weighted_sum = 0
        
        weights = {'High': 3, 'Medium': 2, 'Low': 1}
        
        for category, data in severity_analysis.items():
            for risk in data['risks']:
                severity = risk['severity']
                weighted_sum += weights.get(severity, 1)
                total_risks += 1
        
        if total_risks == 0:
            return 0
        
        # Normalize to 0-100 scale
        # Assume average risk has score of 2 (medium)
        avg_weight = weighted_sum / total_risks
        
        # Convert to 0-100 where 100 = highest risk
        risk_score = min((avg_weight / 3) * 100, 100)
        
        return risk_score


def main():
    """Test risk analyzer"""
    print("Risk Analyzer Module")
    print("Integrates with RAG pipeline for risk extraction and classification")


if __name__ == "__main__":
    main()
