"""
Risk analyser integration module.

This module orchestrates the complete risk analysis workflow:
1. Parse risk register CSV
2. analyser AI use case with Claude
3. Combine results for comprehensive governance assessment

@author: Vincent Wachira
@date: 2025-02-14
@version: 0.1.0
@license: MIT
"""

from __future__ import annotations 
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import pandas as pd

from typing import Dict, List, Optional, TYPE_CHECKING

# Type hint imports (only used for type checking, not runtime)
if TYPE_CHECKING:
    from src.analyser.gemini_client import AIRiskAnalysis

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.parsers.csv_parser import CSVParser, CSVParserError
from src.logger import logger


@dataclass
class ComprehensiveRiskAssessment:
    """
    Complete risk assessment combining CSV risks and AI analysis.
    
    Attributes:
        organizational_risks: Risks from CSV risk register
        ai_governance_analysis: AI-specific governance findings from Claude
        summary_statistics: Aggregated metrics
        high_priority_items: Top risks requiring immediate attention
    """
    organizational_risks: pd.DataFrame
    ai_governance_analysis: 'AIRiskAnalysis'
    summary_statistics: Dict
    high_priority_items: List[Dict]


class RiskanalyserError(Exception):
    """Custom exception for risk analyser errors."""
    pass


class Riskanalyser:
    """
    Orchestrates complete AI governance risk analysis.
    
    This class integrates CSV parsing and Claude API analysis to provide
    comprehensive governance assessments for AI use cases.
    
    Example:
        >>> analyser = Riskanalyser()
        >>> assessment = analyser.analyser(
        ...     risk_register_path='data/risks.csv',
        ...     use_case_description='Deploy AI chatbot'
        ... )
        >>> print(f"Found {len(assessment.high_priority_items)} high-priority risks")
    """
    def __init__(self, ai_provider: str = 'gemini'):
        """
        Initialize risk analyser with specified AI provider.
        
        Args:
            ai_provider: Which AI to use ('gemini', 'claude', or 'mock')
        """
        self.csv_parser = CSVParser()
        self.ai_provider = ai_provider.lower()
        
        # Import and initialize the appropriate AI client
        if self.ai_provider == 'gemini':
            from src.analyser.gemini_client import GeminiClient, GeminiClientError
            self.ai_client = GeminiClient()
            self.AIClientError = GeminiClientError
            logger.info("🤖 AI Provider: Gemini 2.5 Flash (Google)")
            
        elif self.ai_provider == 'claude':
            from src.analyser.claude_client import ClaudeClient, ClaudeClientError
            self.ai_client = ClaudeClient()
            self.AIClientError = ClaudeClientError
            logger.info("🤖 AI Provider: Claude Sonnet 4 (Anthropic)")
            
        elif self.ai_provider == 'mock':
            from src.analyser.mock_claude_client import ClaudeClient as MockClient, ClaudeClientError as MockError
            self.ai_client = MockClient()
            self.AIClientError = MockError
            logger.warning("🎭 AI Provider: Mock Mode (Offline)")
            
        else:
            error_msg = f"Invalid AI provider: {ai_provider}"
            logger.error(error_msg)
            raise RiskanalyserError(error_msg)
        
        logger.info(f"Riskanalyser initialized with {self.ai_provider} provider")
    
    def analyse(
        self,
        risk_register_path: Path | str,
        use_case_description: str,
        context: Optional[Dict] = None
    ) -> ComprehensiveRiskAssessment:
        """
        Perform comprehensive risk analysis.
        
        Args:
            risk_register_path: Path to CSV risk register file
            use_case_description: Description of AI use case to analyser
            context: Optional context (industry, data types, etc.)
            
        Returns:
            ComprehensiveRiskAssessment with combined findings
            
        Raises:
            RiskanalyserError: If analysis fails at any stage
            
        Example:
            >>> analyser = Riskanalyser()
            >>> assessment = analyser.analyser(
            ...     'data/sample_risk_register.csv',
            ...     'Using AI for customer support chatbot',
            ...     {'industry': 'financial services'}
            ... )
        """
        logger.info("=" * 70)
        logger.info("STARTING COMPREHENSIVE RISK ANALYSIS")
        logger.info("=" * 70)
        
        # Step 1: Parse risk register
        logger.info("Step 1/4: Parsing risk register...")
        try:
            risk_data = self.csv_parser.parse(risk_register_path)
            csv_summary = self.csv_parser.get_summary(risk_data)
            logger.info(f"✓ Loaded {csv_summary['total_risks']} organizational risks")
        except CSVParserError as e:
            error_msg = f"Failed to parse risk register: {e}"
            logger.error(error_msg)
            raise RiskanalyserError(error_msg)
        
        # Step 2: analyser AI use case
        logger.info("Step 2/4: Analyzing AI use case with governance framework...")
        try:
            ai_analysis = self.ai_client.analyze_use_case(
                use_case_description,
                context
            )
            logger.info(f"✓ Identified {len(ai_analysis.ai_risks)} AI-specific risks")
        except self.AIClientError as e:
            error_msg = f"Failed to analyze use case: {e}"
            logger.error(error_msg)
            raise RiskanalyserError(error_msg)
        
        # Step 3: Generate summary statistics
        logger.info("Step 3/4: Generating summary statistics...")
        summary_stats = self._generate_summary_statistics(risk_data, ai_analysis)
        logger.info(f"✓ Analysis complete - Overall risk score: {summary_stats['overall_risk_score']:.2f}")
        
        # Step 4: Identify high-priority items
        logger.info("Step 4/4: Identifying high-priority action items...")
        high_priority = self._identify_high_priority_items(risk_data, ai_analysis)
        logger.info(f"✓ Found {len(high_priority)} high-priority items")
        
        # Create comprehensive assessment
        assessment = ComprehensiveRiskAssessment(
            organizational_risks=risk_data,
            ai_governance_analysis=ai_analysis,
            summary_statistics=summary_stats,
            high_priority_items=high_priority
        )
        
        logger.info("=" * 70)
        logger.info("ANALYSIS COMPLETE")
        logger.info("=" * 70)
        
        return assessment
    
    def _generate_summary_statistics(
        self,
        risk_data: pd.DataFrame,
        ai_analysis: AIRiskAnalysis
    ) -> Dict:
        """
        Generate summary statistics from combined analysis.
        
        Args:
            risk_data: Parsed risk register DataFrame
            ai_analysis: AI governance analysis results
            
        Returns:
            Dictionary with summary metrics
        """
        # Calculate from CSV data
        total_org_risks = len(risk_data)
        avg_risk_score = risk_data['risk_score'].mean()
        high_risk_count = len(risk_data[risk_data['risk_score'] >= 15])
        
        # Count AI-specific findings
        total_ai_risks = len(ai_analysis.ai_risks)
        total_iso_domains = len(ai_analysis.iso_domains)
        total_governance_gaps = len(ai_analysis.governance_gaps)
        
        # Calculate overall risk score (weighted combination)
        # 60% from CSV risks, 40% from AI analysis severity
        csv_component = (avg_risk_score / 25) * 0.6  # Normalize to 0-1, weight 60%
        ai_component = (1 - ai_analysis.confidence_score) * 0.4  # Lower confidence = higher risk
        overall_risk_score = (csv_component + ai_component) * 10  # Scale to 0-10
        
        summary = {
            'total_organizational_risks': total_org_risks,
            'total_ai_risks': total_ai_risks,
            'total_governance_gaps': total_governance_gaps,
            'iso_domains_affected': total_iso_domains,
            'high_risk_items': high_risk_count,
            'average_risk_score': round(avg_risk_score, 2),
            'overall_risk_score': round(overall_risk_score, 2),
            'ai_analysis_confidence': ai_analysis.confidence_score,
            'risk_categories': risk_data['category'].value_counts().to_dict() if 'category' in risk_data.columns else {}
        }
        
        logger.debug(f"Summary statistics: {summary}")
        return summary
    
    def _identify_high_priority_items(
        self,
        risk_data: pd.DataFrame,
        ai_analysis: AIRiskAnalysis
    ) -> List[Dict]:
        """
        Identify high-priority items requiring immediate attention.
        
        Args:
            risk_data: Parsed risk register DataFrame
            ai_analysis: AI governance analysis results
            
        Returns:
            List of high-priority items with details
        """
        high_priority = []
        
        # 1. High-risk items from CSV (score >= 15)
        high_csv_risks = risk_data[risk_data['risk_score'] >= 15]
        for _, risk in high_csv_risks.iterrows():
            high_priority.append({
                'source': 'organizational_risk_register',
                'priority': 'HIGH',
                'risk_id': risk['risk_id'],
                'description': risk['risk_description'],
                'risk_score': int(risk['risk_score']),
                'action': risk.get('mitigation', 'No mitigation documented')
            })
        
        # 2. Critical AI governance gaps (first 3 from Claude)
        for i, gap in enumerate(ai_analysis.governance_gaps[:3], 1):
            high_priority.append({
                'source': 'ai_governance_analysis',
                'priority': 'HIGH',
                'risk_id': f'AI-GAP-{i:03d}',
                'description': gap,
                'risk_score': None,  # Qualitative, not quantified
                'action': ai_analysis.recommendations[i-1] if i <= len(ai_analysis.recommendations) else 'Review required'
            })
        
        # 3. Top AI-specific risks (first 2)
        for i, risk in enumerate(ai_analysis.ai_risks[:2], 1):
            high_priority.append({
                'source': 'ai_risk_analysis',
                'priority': 'MEDIUM',
                'risk_id': f'AI-RISK-{i:03d}',
                'description': risk,
                'risk_score': None,
                'action': 'Implement AI risk controls'
            })
        
        logger.debug(f"Identified {len(high_priority)} high-priority items")
        return high_priority
    
    def get_assessment_summary(self, assessment: ComprehensiveRiskAssessment) -> str:
        """
        Generate human-readable summary of assessment.
        
        Args:
            assessment: Complete risk assessment
            
        Returns:
            Formatted summary string
        """
        summary_lines = [
            "=" * 70,
            "RISK ASSESSMENT SUMMARY",
            "=" * 70,
            "",
            f"Overall Risk Score: {assessment.summary_statistics['overall_risk_score']:.1f}/10",
            f"Total Organizational Risks: {assessment.summary_statistics['total_organizational_risks']}",
            f"AI-Specific Risks: {assessment.summary_statistics['total_ai_risks']}",
            f"Governance Gaps: {assessment.summary_statistics['total_governance_gaps']}",
            f"ISO 27001 Domains Affected: {assessment.summary_statistics['iso_domains_affected']}",
            f"High-Priority Items: {len(assessment.high_priority_items)}",
            "",
            "Key ISO 27001 Domains:",
        ]
        
        for domain in assessment.ai_governance_analysis.iso_domains:
            summary_lines.append(f"  • {domain}")
        
        summary_lines.extend([
            "",
            "High-Priority Action Items:",
        ])
        
        for item in assessment.high_priority_items[:5]:  # Top 5
            summary_lines.append(f"  {item['priority']}: {item['description'][:80]}...")
        
        summary_lines.append("=" * 70)
        
        return "\n".join(summary_lines)


# Module-level test
if __name__ == "__main__":
    """Test risk analyser with sample data."""
    logger.info("Running Riskanalyser integration test")
    
    try:
        # Initialize analyser
        analyser = Riskanalyser()
        
        # Paths
        risk_register = Path(__file__).parent.parent.parent / 'data' / 'sample_risk_register.csv'
        
        # Use case
        use_case = """
        Deploy an AI-powered customer support chatbot that:
        - Handles 80% of customer inquiries automatically
        - Accesses customer PII and transaction history
        - Makes product recommendations
        - Escalates complex issues to human agents
        - Operates 24/7 across web and mobile channels
        """
        
        context = {
            'industry': 'Financial Services',
            'regulatory_requirements': 'GDPR, PCI-DSS, SOC2',
            'deployment': 'Cloud (AWS)',
            'data_classification': 'Confidential - PII, Financial'
        }
        
        # Run analysis
        logger.info("\nStarting comprehensive analysis...\n")
        assessment = analyser.analyser(risk_register, use_case, context)
        
        # Display summary
        summary = analyser.get_assessment_summary(assessment)
        print("\n" + summary + "\n")
        
        # Detailed high-priority items
        logger.info("Detailed High-Priority Items:")
        for i, item in enumerate(assessment.high_priority_items, 1):
            logger.info(f"\n{i}. [{item['priority']}] {item['risk_id']}")
            logger.info(f"   Description: {item['description']}")
            logger.info(f"   Action: {item['action']}")
        
        logger.info("\n✅ Riskanalyser integration test successful!")
        
        # Generate report
        logger.info("\n📝 Generating markdown report...")
        try:
            from src.outputs.markdown_report import MarkdownReportGenerator
            
            generator = MarkdownReportGenerator()
            report_path = generator.generate(assessment, output_path='agie_demo_report.md')
            
            logger.info(f"✅ Report generated: {report_path}")
            logger.info(f"📄 View your report: cat {report_path}")
            
        except ImportError as e:
            logger.warning(f"Report generator not available: {e}")
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
        
    except Exception as e:
        logger.critical(f"❌ Test failed: {e}", exc_info=True)