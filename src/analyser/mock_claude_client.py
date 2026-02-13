"""
Mock Claude API client for development and testing.

This module provides a mock implementation of ClaudeClient that returns
realistic AI governance analysis without making actual API calls.
Useful for development when API credits are not available.

@author: Vincent Wachira
@date: 2025-02-14
@version: 0.1.0
@license: MIT
"""

import sys
import time
import random
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.logger import logger


@dataclass
class AIRiskAnalysis:
    """
    Structured output from AI risk analysis.
    
    Attributes:
        ai_risks: List of AI-specific governance risks identified
        iso_domains: ISO 27001 control domains affected
        governance_gaps: Specific governance weaknesses
        recommendations: Prioritized remediation actions
        confidence_score: AI confidence in analysis (0-1)
    """
    ai_risks: List[str]
    iso_domains: List[str]
    governance_gaps: List[str]
    recommendations: List[str]
    confidence_score: float


class ClaudeClientError(Exception):
    """Custom exception for Claude API client errors."""
    pass


class ClaudeClient:
    """
    Mock Claude API client for development without API credits.
    
    This class provides the same interface as the real ClaudeClient
    but returns pre-defined realistic responses instead of calling the API.
    
    🎭 MOCK MODE: This is a development-only implementation!
    Switch to real claude_client.py when API credits are available.
    
    Example:
        >>> client = ClaudeClient()
        >>> analysis = client.analyze_use_case("Deploy chatbot for customer support")
        >>> print(f"Found {len(analysis.ai_risks)} AI risks")
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize mock Claude API client.
        
        Args:
            api_key: Not used in mock (kept for interface compatibility)
            model: Not used in mock (kept for interface compatibility)
        """
        self.api_key = "mock-api-key"
        self.model = model
        
        logger.warning("🎭 MOCK MODE: Using mock Claude client (no real API calls)")
        logger.info(f"Mock ClaudeClient initialized with model: {self.model}")
    
    def analyze_use_case(
        self,
        use_case_description: str,
        context: Optional[Dict] = None
    ) -> AIRiskAnalysis:
        """
        Mock analyze AI use case for governance risks.
        
        Returns realistic but pre-defined analysis based on common patterns.
        
        Args:
            use_case_description: Description of the AI use case to analyze
            context: Optional additional context (affects which template is used)
            
        Returns:
            AIRiskAnalysis object with mock findings
            
        Example:
            >>> client = ClaudeClient()
            >>> analysis = client.analyze_use_case(
            ...     "Using AI for loan approval decisions",
            ...     context={"industry": "financial services"}
            ... )
        """
        logger.info(f"🎭 Mock analyzing AI use case: {use_case_description[:100]}...")
        
        # Simulate API call delay (realistic behavior)
        time.sleep(1.5)
        
        # Determine which template to use based on keywords
        analysis = self._generate_mock_analysis(use_case_description, context)
        
        logger.info(f"🎭 Mock analysis complete: {len(analysis.ai_risks)} risks identified")
        
        return analysis
    
    def _generate_mock_analysis(
        self,
        use_case_description: str,
        context: Optional[Dict] = None
    ) -> AIRiskAnalysis:
        """
        Generate realistic mock analysis based on use case keywords.
        
        Args:
            use_case_description: Use case text
            context: Optional context
            
        Returns:
            AIRiskAnalysis with contextually appropriate risks
        """
        use_case_lower = use_case_description.lower()
        
        # Detect use case type and return appropriate template
        if any(word in use_case_lower for word in ['chatbot', 'customer support', 'chat', 'support']):
            return self._chatbot_template()
        
        elif any(word in use_case_lower for word in ['loan', 'credit', 'approval', 'lending', 'scoring']):
            return self._credit_scoring_template()
        
        elif any(word in use_case_lower for word in ['hiring', 'recruitment', 'resume', 'candidate']):
            return self._hiring_template()
        
        elif any(word in use_case_lower for word in ['fraud', 'detection', 'transaction', 'monitoring']):
            return self._fraud_detection_template()
        
        else:
            return self._generic_template()
    
    def _chatbot_template(self) -> AIRiskAnalysis:
        """Mock analysis for chatbot/customer support use cases."""
        return AIRiskAnalysis(
            ai_risks=[
                "Model hallucinations may provide incorrect information to customers",
                "Lack of explainability in decision-making for escalations",
                "Potential for bias in sentiment analysis affecting customer treatment",
                "Third-party AI model dependencies introduce supply chain risk",
                "Model drift over time may degrade response quality without monitoring"
            ],
            iso_domains=[
                "A.5 - Information Security Policies",
                "A.8 - Asset Management (customer data handling)",
                "A.12 - Operations Security (logging, monitoring)",
                "A.13 - Communications Security",
                "A.15 - Supplier Relationships (third-party AI models)",
                "A.18 - Compliance (data protection, GDPR)"
            ],
            governance_gaps=[
                "No documented AI model validation or testing procedure",
                "Insufficient logging of AI decisions for audit trail",
                "Lack of human oversight for high-risk customer interactions",
                "No process for handling AI-generated misinformation",
                "Missing data retention and privacy controls for conversation logs"
            ],
            recommendations=[
                "Implement real-time model monitoring with alerting for hallucinations",
                "Establish human-in-the-loop review for sensitive customer issues",
                "Create comprehensive AI decision logging (inputs, outputs, confidence scores)",
                "Document model validation procedures aligned with ISO 27001 A.12.1",
                "Implement data minimization and retention policies for conversation logs",
                "Conduct regular bias testing with diverse customer scenarios"
            ],
            confidence_score=0.88
        )
    
    def _credit_scoring_template(self) -> AIRiskAnalysis:
        """Mock analysis for credit/loan approval use cases."""
        return AIRiskAnalysis(
            ai_risks=[
                "Algorithmic bias may lead to discriminatory lending decisions",
                "Lack of model explainability violates fair lending regulations",
                "Training data may reflect historical bias in lending practices",
                "Model drift could cause inconsistent credit decisions over time",
                "Third-party data sources may introduce unvalidated risk factors"
            ],
            iso_domains=[
                "A.5 - Information Security Policies",
                "A.8 - Asset Management (sensitive financial data)",
                "A.9 - Access Control (model access, data access)",
                "A.12 - Operations Security (model monitoring)",
                "A.18 - Compliance (fair lending laws, FCRA, ECOA)"
            ],
            governance_gaps=[
                "No documented fairness testing or bias mitigation strategy",
                "Insufficient explainability mechanisms (SHAP, LIME, etc.)",
                "Lack of adverse action notice generation with AI explanations",
                "No documented model retraining and drift monitoring procedures",
                "Missing audit trail for model decisions and appeals process"
            ],
            recommendations=[
                "Implement comprehensive bias testing across protected classes",
                "Deploy explainable AI framework (SHAP/LIME) for all credit decisions",
                "Establish model governance committee with legal, compliance, and data science",
                "Create automated fairness monitoring with regulatory thresholds",
                "Document model card with training data sources, limitations, and performance metrics",
                "Implement human review process for borderline cases and appeals"
            ],
            confidence_score=0.92
        )
    
    def _hiring_template(self) -> AIRiskAnalysis:
        """Mock analysis for hiring/recruitment use cases."""
        return AIRiskAnalysis(
            ai_risks=[
                "Resume screening AI may perpetuate historical hiring bias",
                "Lack of transparency in candidate ranking algorithms",
                "Training data may reflect past discriminatory practices",
                "Model may inadvertently filter protected class candidates",
                "Limited explainability for rejected candidates"
            ],
            iso_domains=[
                "A.5 - Information Security Policies",
                "A.7 - Human Resource Security",
                "A.8 - Asset Management (candidate PII)",
                "A.12 - Operations Security",
                "A.18 - Compliance (employment law, EEOC guidelines)"
            ],
            governance_gaps=[
                "No documented AI fairness testing for protected classes",
                "Insufficient explainability for candidate rejections",
                "Lack of human oversight in final hiring decisions",
                "Missing documentation of training data sources and bias mitigation",
                "No process for candidates to challenge AI-driven decisions"
            ],
            recommendations=[
                "Conduct disparate impact testing across gender, race, age demographics",
                "Implement explainable AI for candidate ranking decisions",
                "Require human review for all final hiring decisions",
                "Document model limitations and post-deployment monitoring plan",
                "Create candidate notification process about AI usage in screening",
                "Establish regular bias audits with third-party validation"
            ],
            confidence_score=0.85
        )
    
    def _fraud_detection_template(self) -> AIRiskAnalysis:
        """Mock analysis for fraud detection use cases."""
        return AIRiskAnalysis(
            ai_risks=[
                "High false positive rate may impact legitimate customer transactions",
                "Model drift as fraudsters adapt to detection patterns",
                "Adversarial attacks could evade fraud detection",
                "Lack of explainability for flagged transactions affects customer trust",
                "Real-time processing requirements may compromise security checks"
            ],
            iso_domains=[
                "A.8 - Asset Management (transaction data)",
                "A.12 - Operations Security (real-time monitoring)",
                "A.13 - Communications Security",
                "A.16 - Incident Management",
                "A.17 - Business Continuity",
                "A.18 - Compliance (PCI-DSS, financial regulations)"
            ],
            governance_gaps=[
                "No documented false positive/negative monitoring",
                "Insufficient model retraining procedures as fraud patterns evolve",
                "Lack of adversarial testing against evasion techniques",
                "Missing customer communication process for false positives",
                "No documented escalation procedures for high-risk detections"
            ],
            recommendations=[
                "Implement continuous model monitoring with adaptive retraining",
                "Establish clear thresholds and human review for high-value transactions",
                "Conduct regular adversarial testing and red team exercises",
                "Create customer-friendly explanation mechanisms for fraud flags",
                "Document incident response procedures for fraud detection failures",
                "Implement A/B testing framework for model improvements"
            ],
            confidence_score=0.90
        )
    
    def _generic_template(self) -> AIRiskAnalysis:
        """Generic mock analysis for unrecognized use cases."""
        return AIRiskAnalysis(
            ai_risks=[
                "Potential for model bias affecting decision outcomes",
                "Lack of explainability may hinder accountability",
                "Model performance may degrade over time without monitoring",
                "Data quality issues could compromise model reliability",
                "Third-party dependencies introduce supply chain risks"
            ],
            iso_domains=[
                "A.5 - Information Security Policies",
                "A.8 - Asset Management",
                "A.12 - Operations Security",
                "A.14 - System Acquisition and Development",
                "A.18 - Compliance"
            ],
            governance_gaps=[
                "No documented AI model validation procedures",
                "Insufficient logging and monitoring of AI decisions",
                "Lack of defined roles and responsibilities for AI governance",
                "Missing incident response procedures for AI failures",
                "No documented model risk management framework"
            ],
            recommendations=[
                "Establish AI governance framework with clear ownership",
                "Implement comprehensive logging of model inputs and outputs",
                "Create model performance monitoring dashboard",
                "Document model limitations and approved use cases",
                "Develop incident response procedures for AI-related issues",
                "Conduct regular model validation and bias testing"
            ],
            confidence_score=0.75
        )


# Module-level test
if __name__ == "__main__":
    """Test mock Claude API client with sample use case."""
    logger.info("Running MOCK Claude API client test")
    
    try:
        # Initialize mock client
        client = ClaudeClient()
        
        # Test use case: AI chatbot for customer support
        use_case = """
        We are deploying an AI-powered chatbot for customer support that will:
        - Handle customer inquiries 24/7
        - Access customer data (names, account details, transaction history)
        - Make recommendations for products based on purchase history
        - Escalate complex issues to human agents
        - Store conversation logs for quality assurance
        """
        
        context = {
            "industry": "Financial Services",
            "data_sensitivity": "High (PII, financial data)",
            "deployment": "Cloud-based (AWS)",
            "user_base": "50,000+ customers"
        }
        
        logger.info("Testing AI use case analysis...")
        analysis = client.analyze_use_case(use_case, context)
        
        # Display results
        logger.info("=" * 60)
        logger.info("MOCK ANALYSIS RESULTS")
        logger.info("=" * 60)
        
        logger.info(f"\nAI Risks Identified ({len(analysis.ai_risks)}):")
        for i, risk in enumerate(analysis.ai_risks, 1):
            logger.info(f"  {i}. {risk}")
        
        logger.info(f"\nISO 27001 Domains Affected ({len(analysis.iso_domains)}):")
        for domain in analysis.iso_domains:
            logger.info(f"  - {domain}")
        
        logger.info(f"\nGovernance Gaps ({len(analysis.governance_gaps)}):")
        for i, gap in enumerate(analysis.governance_gaps, 1):
            logger.info(f"  {i}. {gap}")
        
        logger.info(f"\nRecommendations ({len(analysis.recommendations)}):")
        for i, rec in enumerate(analysis.recommendations, 1):
            logger.info(f"  {i}. {rec}")
        
        logger.info(f"\nConfidence Score: {analysis.confidence_score:.2f}")
        logger.info("=" * 60)
        
        logger.info("✅ Mock Claude API client test successful!")
        logger.info("🎭 Remember: This is mock data. Switch to real claude_client.py on Sunday!")
        
    except Exception as e:
        logger.critical(f"❌ Unexpected error: {e}", exc_info=True)