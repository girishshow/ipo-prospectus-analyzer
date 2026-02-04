"""
Recommendation Engine
Multi-factor scoring and investment recommendation generation
"""

from typing import Dict, Optional
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Generate investment recommendations based on multi-factor analysis
    """
    
    def __init__(self, llm_client=None):
        self.llm = llm_client
        
        # Scoring weights
        self.weights = {
            'business_score': 0.25,
            'financial_score': 0.30,
            'industry_score': 0.20,
            'risk_score': 0.15,
            'valuation_score': 0.10
        }
        
        # Thresholds for recommendations
        self.thresholds = {
            'conservative': 75,
            'neutral': 60,
            'aggressive': 50
        }
    
    def generate_recommendation(self, analysis_results: Dict) -> Dict:
        """
        Generate investment recommendation
        
        Args:
            analysis_results: Dictionary with all analysis outputs
            
        Returns:
            Recommendation with scoring and explanation
        """
        logger.info("Generating investment recommendation...")
        
        # Calculate individual scores
        scores = self.calculate_scores(analysis_results)
        
        # Calculate overall score
        overall_score = self.calculate_overall_score(scores)
        
        # Determine stance
        stance = self.determine_stance(overall_score)
        
        # Generate explanation
        explanation = self.generate_explanation(scores, stance, analysis_results)
        
        # Determine suitability
        suitability = self.determine_suitability(scores, stance)
        
        return {
            'scores': scores,
            'overall_score': overall_score,
            'stance': stance,
            'explanation': explanation,
            'suitability': suitability,
            'key_strengths': self.extract_key_strengths(analysis_results, scores),
            'key_concerns': self.extract_key_concerns(analysis_results, scores)
        }
    
    def calculate_scores(self, analysis: Dict) -> Dict:
        """
        Calculate individual component scores (0-100)
        """
        scores = {}
        
        # Business score
        scores['business_score'] = self._score_business(analysis.get('business', {}))
        
        # Financial score
        scores['financial_score'] = self._score_financials(analysis.get('financials', {}))
        
        # Industry score
        scores['industry_score'] = self._score_industry(analysis.get('industry', {}))
        
        # Risk score (inverted - lower risk = higher score)
        scores['risk_score'] = self._score_risk(analysis.get('risks', {}))
        
        # Valuation score
        scores['valuation_score'] = self._score_valuation(analysis.get('valuation', {}))
        
        logger.info(f"Component scores: {scores}")
        return scores
    
    def _score_business(self, business_analysis: Dict) -> float:
        """
        Score business quality (0-100)
        
        Factors:
        - Business model clarity
        - Market position
        - Competitive advantages
        - Customer diversification
        """
        # Placeholder - would analyze business_analysis content
        # For now, return moderate score
        return 70.0
    
    def _score_financials(self, financial_data: Dict) -> float:
        """
        Score financial health (0-100)
        
        Factors:
        - Revenue growth
        - Profitability margins
        - Cash flow
        - Balance sheet strength
        """
        score = 50.0  # Base score
        
        metrics = financial_data.get('basic_metrics', {})
        growth = financial_data.get('growth_metrics', {})
        ratios = financial_data.get('ratios', {})
        
        # Revenue growth
        revenue_cagr = growth.get('revenue_cagr_3y')
        if revenue_cagr:
            if revenue_cagr > 20:
                score += 15
            elif revenue_cagr > 10:
                score += 10
            elif revenue_cagr > 5:
                score += 5
        
        # Margins
        ebitda_margin = metrics.get('ebitda_margin', {})
        if ebitda_margin:
            latest_margin = list(ebitda_margin.values())[-1] if ebitda_margin else 0
            if latest_margin > 20:
                score += 15
            elif latest_margin > 10:
                score += 10
            elif latest_margin > 5:
                score += 5
        
        # Debt levels
        de_ratio = ratios.get('debt_to_equity', {})
        if de_ratio:
            latest_de = list(de_ratio.values())[-1] if de_ratio else 0
            if latest_de < 0.5:
                score += 10
            elif latest_de < 1.0:
                score += 5
            elif latest_de > 2.0:
                score -= 10
        
        return min(max(score, 0), 100)
    
    def _score_industry(self, industry_data: Dict) -> float:
        """
        Score industry attractiveness (0-100)
        """
        # Placeholder
        return 65.0
    
    def _score_risk(self, risk_analysis: Dict) -> float:
        """
        Score risk profile (0-100, higher = lower risk)
        """
        if not risk_analysis:
            return 50.0
        
        # Get risk score from analyzer (0-100, higher = more risk)
        risk_score = risk_analysis.get('risk_score', 50)
        
        # Invert it (we want higher score = better)
        inverted_score = 100 - risk_score
        
        return inverted_score
    
    def _score_valuation(self, valuation_data: Dict) -> float:
        """
        Score valuation attractiveness (0-100)
        """
        # Placeholder
        return 60.0
    
    def calculate_overall_score(self, scores: Dict) -> float:
        """
        Calculate weighted overall score
        """
        overall = sum(
            scores.get(component, 50) * weight
            for component, weight in self.weights.items()
        )
        
        return round(overall, 1)
    
    def determine_stance(self, overall_score: float) -> str:
        """
        Determine investment stance based on score
        """
        if overall_score >= self.thresholds['conservative']:
            return 'Conservative - Positive'
        elif overall_score >= self.thresholds['neutral']:
            return 'Neutral'
        elif overall_score >= self.thresholds['aggressive']:
            return 'Aggressive - Speculative'
        else:
            return 'Avoid'
    
    def generate_explanation(self, scores: Dict, stance: str, 
                           analysis: Dict) -> str:
        """
        Generate explanation using LLM
        """
        if not self.llm:
            return self._generate_template_explanation(scores, stance)
        
        # Build context
        context = f"""Investment Recommendation Analysis:

Overall Score: {self.calculate_overall_score(scores)}/100
Stance: {stance}

Component Scores:
- Business Quality: {scores['business_score']}/100
- Financial Health: {scores['financial_score']}/100
- Industry Attractiveness: {scores['industry_score']}/100
- Risk Profile: {scores['risk_score']}/100
- Valuation: {scores['valuation_score']}/100

Analysis Inputs:
{self._summarize_analysis(analysis)}
"""
        
        prompt = f"""{context}

Based on this analysis, provide a clear investment recommendation explanation that:

1. Explains the overall stance and what it means for investors
2. Highlights key factors supporting the recommendation
3. Notes important considerations or concerns
4. Describes which type of investor this IPO suits

Keep it concise and educational. This is NOT investment advice but analysis.

Explanation:"""
        
        response = self.llm.generate(
            prompt=prompt,
            system_prompt="You are an investment analyst providing educational analysis. Be balanced and clear.",
            temperature=0.2,
            max_tokens=1024
        )
        
        return response.strip()
    
    def _generate_template_explanation(self, scores: Dict, stance: str) -> str:
        """
        Generate explanation without LLM (template-based)
        """
        overall = self.calculate_overall_score(scores)
        
        explanation = f"""Based on multi-factor analysis, this IPO scores {overall}/100, indicating a '{stance}' outlook.

Scoring Breakdown:
- Business: {scores['business_score']}/100
- Financials: {scores['financial_score']}/100
- Industry: {scores['industry_score']}/100
- Risk: {scores['risk_score']}/100
- Valuation: {scores['valuation_score']}/100

"""
        
        if stance == 'Conservative - Positive':
            explanation += "This IPO shows strong fundamentals across most parameters, suitable for conservative investors seeking quality."
        elif stance == 'Neutral':
            explanation += "This IPO has a balanced risk-reward profile. Suitable for moderate investors willing to accept some uncertainty."
        elif stance == 'Aggressive - Speculative':
            explanation += "This IPO carries elevated risks but may offer growth potential. Suitable only for aggressive investors."
        else:
            explanation += "This IPO has significant concerns. Investors should carefully evaluate before participating."
        
        return explanation
    
    def _summarize_analysis(self, analysis: Dict) -> str:
        """
        Create brief summary of analysis for LLM context
        """
        summary_parts = []
        
        if 'financials' in analysis:
            summary_parts.append("Financial metrics provided")
        
        if 'risks' in analysis:
            risk_count = analysis['risks'].get('total_risks', 0)
            summary_parts.append(f"{risk_count} risks identified")
        
        return '; '.join(summary_parts) if summary_parts else "Analysis available"
    
    def determine_suitability(self, scores: Dict, stance: str) -> str:
        """
        Determine investor suitability
        """
        overall = self.calculate_overall_score(scores)
        risk_score = scores['risk_score']
        
        if overall >= 75 and risk_score >= 70:
            return "Conservative investors seeking quality with lower risk"
        elif overall >= 60:
            return "Moderate investors comfortable with balanced risk-reward"
        elif overall >= 50:
            return "Aggressive investors with high risk tolerance"
        else:
            return "Not suitable for most retail investors"
    
    def extract_key_strengths(self, analysis: Dict, scores: Dict) -> list:
        """
        Extract key strengths from analysis
        """
        strengths = []
        
        # Check financial strengths
        if scores['financial_score'] >= 75:
            strengths.append("Strong financial performance and growth")
        
        # Check business strengths
        if scores['business_score'] >= 75:
            strengths.append("Robust business model and market position")
        
        # Check risk profile
        if scores['risk_score'] >= 75:
            strengths.append("Manageable risk profile")
        
        # Default if none
        if not strengths:
            strengths.append("Moderate fundamentals across parameters")
        
        return strengths[:4]  # Top 4
    
    def extract_key_concerns(self, analysis: Dict, scores: Dict) -> list:
        """
        Extract key concerns from analysis
        """
        concerns = []
        
        # Check for weak areas
        if scores['financial_score'] < 50:
            concerns.append("Weak financial performance or declining trends")
        
        if scores['risk_score'] < 50:
            concerns.append("Elevated risk factors")
        
        if scores['valuation_score'] < 40:
            concerns.append("Potentially expensive valuation")
        
        # Get risks from analysis
        if 'risks' in analysis:
            risk_summary = analysis['risks'].get('summary', '')
            if risk_summary and len(risk_summary) > 50:
                concerns.append("Multiple material risks identified")
        
        # Default if none
        if not concerns:
            concerns.append("Standard IPO investment risks apply")
        
        return concerns[:4]  # Top 4


def main():
    """Test recommendation engine"""
    
    # Sample analysis data
    sample_analysis = {
        'financials': {
            'basic_metrics': {
                'ebitda_margin': {2021: 18, 2022: 19, 2023: 20}
            },
            'growth_metrics': {
                'revenue_cagr_3y': 15
            },
            'ratios': {
                'debt_to_equity': {2021: 0.8, 2022: 0.7, 2023: 0.6}
            }
        },
        'risks': {
            'total_risks': 15,
            'risk_score': 45
        }
    }
    
    engine = RecommendationEngine()
    recommendation = engine.generate_recommendation(sample_analysis)
    
    print("\n" + "="*80)
    print("INVESTMENT RECOMMENDATION")
    print("="*80)
    print(f"\nOverall Score: {recommendation['overall_score']}/100")
    print(f"Stance: {recommendation['stance']}")
    print(f"\nSuitability: {recommendation['suitability']}")
    print(f"\nKey Strengths:")
    for s in recommendation['key_strengths']:
        print(f"  • {s}")
    print(f"\nKey Concerns:")
    for c in recommendation['key_concerns']:
        print(f"  • {c}")


if __name__ == "__main__":
    main()
