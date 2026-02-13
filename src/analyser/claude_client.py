"""
Claude API client for AI-powered risk analysis.

This module handles communication with Anthropic's Claude API,
providing structured prompts for governance risk assessment.

@author: Vincent Wachira
@date: 2025-02-14
@version: 0.1.0
@license: MIT
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from anthropic import Anthropic, APIError, APIConnectionError, RateLimitError
from dotenv import load_dotenv

from src.logger import logger

# Load environment variables
load_dotenv()


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
    Client for interacting with Claude API for risk analysis.
    
    This class provides methods for analyzing AI use cases and risks
    using structured prompts to ensure consistent, parseable outputs.
    
    Example:
        >>> client = ClaudeClient()
        >>> analysis = client.analyze_use_case("Deploy chatbot for customer support")
        >>> print(f"Found {len(analysis.ai_risks)} AI risks")
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize Claude API client.
        
        Args:
            api_key: Anthropic API key. If None, loads from ANTHROPIC_API_KEY env var
            model: Claude model to use (default: Claude Sonnet 4)
            
        Raises:
            ClaudeClientError: If API key is not provided or found in environment
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        
        if not self.api_key:
            error_msg = (
                "ANTHROPIC_API_KEY not found. "
                "Set it in .env file or pass as argument."
            )
            logger.critical(error_msg)
            raise ClaudeClientError(error_msg)
        
        self.model = model
        self.client = Anthropic(api_key=self.api_key)
        
        logger.info(f"ClaudeClient initialized with model: {self.model}")
        logger.debug(f"API key present: {bool(self.api_key)}")
    
    def analyze_use_case(
        self,
        use_case_description: str,
        context: Optional[Dict] = None
    ) -> AIRiskAnalysis:
        """
        Analyze AI use case for governance risks and control gaps.
        
        Args:
            use_case_description: Description of the AI use case to analyze
            context: Optional additional context (industry, data types, etc.)
            
        Returns:
            AIRiskAnalysis object with structured findings
            
        Raises:
            ClaudeClientError: If API call fails
            
        Example:
            >>> client = ClaudeClient()
            >>> analysis = client.analyze_use_case(
            ...     "Using AI for loan approval decisions",
            ...     context={"industry": "financial services"}
            ... )
        """
        logger.info(f"Analyzing AI use case: {use_case_description[:100]}...")
        
        # Build the system prompt for structured analysis
        system_prompt = self._build_system_prompt()
        
        # Build the user message with use case details
        user_message = self._build_user_message(use_case_description, context)
        
        # Make API call with error handling
        try:
            response = self._call_api(system_prompt, user_message)
            logger.info("API call successful")
            
        except RateLimitError as e:
            error_msg = f"Rate limit exceeded: {e}"
            logger.error(error_msg)
            raise ClaudeClientError(error_msg)
            
        except APIConnectionError as e:
            error_msg = f"API connection failed: {e}"
            logger.error(error_msg)
            raise ClaudeClientError(error_msg)
            
        except APIError as e:
            error_msg = f"API error: {e}"
            logger.error(error_msg)
            raise ClaudeClientError(error_msg)
        
        # Parse response into structured format
        analysis = self._parse_response(response)
        logger.info(f"Analysis complete: {len(analysis.ai_risks)} risks identified")
        
        return analysis
    
    def _build_system_prompt(self) -> str:
        """
        Build system prompt for AI governance analysis.
        
        This prompt instructs Claude to act as a governance expert and
        provide structured, consistent analysis.
        
        Returns:
            System prompt string
        """
        prompt = """You are an expert in AI governance, information security, and ISO 27001 compliance.

Your task is to analyze AI use cases and identify governance risks, control gaps, and compliance concerns.

For each use case, provide a structured analysis in JSON format with these fields:

{
  "ai_risks": ["List of AI-specific risks like bias, explainability, drift, etc."],
  "iso_domains": ["ISO 27001 domains affected: A.5-A.18"],
  "governance_gaps": ["Specific governance weaknesses"],
  "recommendations": ["Prioritized actions to address risks"],
  "confidence_score": 0.85
}

Focus on:
1. AI-specific risks (bias, fairness, explainability, model drift, third-party AI risk)
2. ISO 27001 control domains (A.5 through A.18)
3. Data protection and privacy concerns
4. Accountability and audit trail requirements
5. Third-party and vendor management

Be concise but specific. Provide actionable recommendations.

Respond ONLY with valid JSON. No preamble, no explanations outside JSON."""

        logger.debug("System prompt built")
        return prompt
    
    def _build_user_message(
        self,
        use_case_description: str,
        context: Optional[Dict] = None
    ) -> str:
        """
        Build user message with use case details.
        
        Args:
            use_case_description: AI use case description
            context: Optional context dictionary
            
        Returns:
            Formatted user message string
        """
        message = f"Analyze this AI use case for governance risks:\n\n{use_case_description}"
        
        if context:
            message += f"\n\nAdditional context:\n{json.dumps(context, indent=2)}"
        
        logger.debug(f"User message built: {len(message)} characters")
        return message
    
    def _call_api(self, system_prompt: str, user_message: str) -> str:
        """
        Make API call to Claude with error handling.
        
        Args:
            system_prompt: System instructions
            user_message: User query
            
        Returns:
            Claude's response text
            
        Raises:
            Various Anthropic API exceptions
        """
        logger.debug(f"Calling Claude API (model: {self.model})")
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        
        # Extract text from response
        response_text = response.content[0].text
        
        logger.debug(f"Response received: {len(response_text)} characters")
        logger.debug(f"Tokens used - Input: {response.usage.input_tokens}, Output: {response.usage.output_tokens}")
        
        return response_text
    
    def _parse_response(self, response_text: str) -> AIRiskAnalysis:
        """
        Parse Claude's JSON response into structured object.
        
        Args:
            response_text: Raw response from Claude
            
        Returns:
            AIRiskAnalysis object
            
        Raises:
            ClaudeClientError: If response cannot be parsed
        """
        logger.debug("Parsing API response")
        
        try:
            # Claude should return pure JSON, but might have markdown code blocks
            # Clean up common formatting issues
            cleaned = response_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]  # Remove ```json
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]  # Remove ```
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]  # Remove trailing ```
            cleaned = cleaned.strip()
            
            # Parse JSON
            data = json.loads(cleaned)
            
            # Validate required fields
            required_fields = ['ai_risks', 'iso_domains', 'governance_gaps', 
                             'recommendations', 'confidence_score']
            missing_fields = [f for f in required_fields if f not in data]
            
            if missing_fields:
                error_msg = f"Response missing required fields: {missing_fields}"
                logger.error(error_msg)
                raise ClaudeClientError(error_msg)
            
            # Create structured object
            analysis = AIRiskAnalysis(
                ai_risks=data['ai_risks'],
                iso_domains=data['iso_domains'],
                governance_gaps=data['governance_gaps'],
                recommendations=data['recommendations'],
                confidence_score=float(data['confidence_score'])
            )
            
            logger.debug("Response parsed successfully")
            return analysis
            
        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse JSON response: {e}"
            logger.error(error_msg)
            logger.debug(f"Raw response: {response_text}")
            raise ClaudeClientError(error_msg)
        
        except (KeyError, TypeError, ValueError) as e:
            error_msg = f"Invalid response structure: {e}"
            logger.error(error_msg)
            raise ClaudeClientError(error_msg)


# Module-level test
if __name__ == "__main__":
    """Test Claude API client with sample use case."""
    logger.info("Running Claude API client test")
    
    try:
        # Initialize client
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
        logger.info("ANALYSIS RESULTS")
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
        
        logger.info("✅ Claude API client test successful!")
        
    except ClaudeClientError as e:
        logger.error(f"❌ Test failed: {e}")
        
    except Exception as e:
        logger.critical(f"❌ Unexpected error: {e}", exc_info=True)