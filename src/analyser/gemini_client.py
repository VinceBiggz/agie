"""
Gemini API client for AI-powered risk analysis with rate limiting.

This module handles communication with Google's Gemini 1.5 Flash API,
providing structured prompts for governance risk assessment with
intelligent rate limiting to stay within API quotas.

Rate Limits:
- 15 requests per minute (RPM)
- 1,500 requests per day
- 1M tokens per minute (TPM)

@author: Vincent Wachira
@date: 2025-02-14
@version: 0.1.0
@license: MIT
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google import genai
from google.genai import types
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


class GeminiClientError(Exception):
    """Custom exception for Gemini API client errors."""
    pass


class RateLimiter:
    """
    Token bucket rate limiter for API calls.
    
    Implements token bucket algorithm to prevent exceeding rate limits.
    
    Attributes:
        max_requests: Maximum requests allowed in time window
        time_window: Time window in seconds
        tokens: Current available tokens
        last_refill: Last time tokens were refilled
    """
    
    def __init__(self, max_requests: int = 15, time_window: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Max requests per time window (default: 15/min)
            time_window: Time window in seconds (default: 60s)
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.tokens = max_requests
        self.last_refill = datetime.now()
        
        logger.info(f"RateLimiter initialized: {max_requests} requests per {time_window}s")
    
    def acquire(self) -> None:
        """
        Acquire a token for API call. Blocks if rate limit reached.
        
        Uses token bucket algorithm:
        - Tokens refill over time
        - If no tokens available, waits until refill
        - Ensures we stay under rate limits
        """
        # Refill tokens based on time passed
        now = datetime.now()
        time_passed = (now - self.last_refill).total_seconds()
        
        # Refill tokens proportionally to time passed
        tokens_to_add = (time_passed / self.time_window) * self.max_requests
        self.tokens = min(self.max_requests, self.tokens + tokens_to_add)
        self.last_refill = now
        
        # If no tokens available, wait
        if self.tokens < 1:
            wait_time = (1 - self.tokens) * (self.time_window / self.max_requests)
            logger.warning(f"Rate limit approaching - waiting {wait_time:.2f}s")
            time.sleep(wait_time)
            self.tokens = 1
        
        # Consume one token
        self.tokens -= 1
        logger.debug(f"Token acquired - {self.tokens:.2f} tokens remaining")


class GeminiClient:
    """
    Client for interacting with Gemini API for risk analysis.
    
    This class provides methods for analyzing AI use cases and risks
    using structured prompts with built-in rate limiting.
    
    Features:
    - Automatic rate limiting (15 RPM)
    - Retry logic with exponential backoff
    - Structured JSON output parsing
    - Comprehensive error handling
    
    Example:
        >>> client = GeminiClient()
        >>> analysis = client.analyze_use_case("Deploy chatbot for customer support")
        >>> print(f"Found {len(analysis.ai_risks)} AI risks")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash",
        rate_limit_rpm: int = 15
    ):
        """
        Initialize Gemini API client with rate limiting.
        
        Args:
            api_key: Google API key. If None, loads from GOOGLE_API_KEY env var
            model: Gemini model to use (default: gemini-2.0-flash-exp)
            rate_limit_rpm: Rate limit in requests per minute (default: 15)
            
        Raises:
            GeminiClientError: If API key is not provided or found in environment
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            error_msg = (
                "GOOGLE_API_KEY not found. "
                "Set it in .env file or pass as argument."
            )
            logger.critical(error_msg)
            raise GeminiClientError(error_msg)
        
        self.model_name = model
        
        # Create Gemini client (new SDK architecture)
        self.client = genai.Client(api_key=self.api_key)
        
        # Initialize rate limiter
        self.rate_limiter = RateLimiter(max_requests=rate_limit_rpm, time_window=60)
        
        logger.info(f"GeminiClient initialized with model: {self.model_name}")
        logger.info(f"Rate limit: {rate_limit_rpm} requests/minute")
        logger.debug(f"API key present: {bool(self.api_key)}")
    
    def analyze_use_case(
        self,
        use_case_description: str,
        context: Optional[Dict] = None,
        max_retries: int = 3
    ) -> AIRiskAnalysis:
        """
        Analyze AI use case for governance risks and control gaps.
        
        Args:
            use_case_description: Description of the AI use case to analyze
            context: Optional additional context (industry, data types, etc.)
            max_retries: Maximum retry attempts on failure (default: 3)
            
        Returns:
            AIRiskAnalysis object with structured findings
            
        Raises:
            GeminiClientError: If API call fails after retries
            
        Example:
            >>> client = GeminiClient()
            >>> analysis = client.analyze_use_case(
            ...     "Using AI for loan approval decisions",
            ...     context={"industry": "financial services"}
            ... )
        """
        logger.info(f"Analyzing AI use case: {use_case_description[:100]}...")
        
        # Build the prompt
        prompt = self._build_prompt(use_case_description, context)
        
        # Make API call with retries and rate limiting
        for attempt in range(max_retries):
            try:
                # Acquire rate limit token (blocks if necessary)
                self.rate_limiter.acquire()
                
                # Make API call
                response_text = self._call_api(prompt)
                logger.info("API call successful")
                
                # Parse response
                analysis = self._parse_response(response_text)
                logger.info(f"Analysis complete: {len(analysis.ai_risks)} risks identified")
                
                return analysis
                
            except Exception as e:
                attempt_num = attempt + 1
                logger.warning(f"API call attempt {attempt_num}/{max_retries} failed: {e}")
                
                if attempt_num < max_retries:
                    # Exponential backoff: 2^attempt seconds
                    wait_time = 2 ** attempt
                    logger.info(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    error_msg = f"API call failed after {max_retries} attempts: {e}"
                    logger.error(error_msg)
                    raise GeminiClientError(error_msg)
    
    def _build_prompt(
        self,
        use_case_description: str,
        context: Optional[Dict] = None
    ) -> str:
        """
        Build comprehensive prompt for AI governance analysis.
        
        Args:
            use_case_description: AI use case description
            context: Optional context dictionary
            
        Returns:
            Complete prompt string
        """
        prompt = """You are an expert in AI governance, information security, and ISO 27001 compliance.

Your task is to analyze AI use cases and identify governance risks, control gaps, and compliance concerns.

Provide your analysis in JSON format with these exact fields:

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

Respond ONLY with valid JSON. No preamble, no markdown formatting, no explanations outside JSON.

---

AI Use Case to Analyze:

"""
        prompt += use_case_description
        
        if context:
            prompt += f"\n\nAdditional Context:\n{json.dumps(context, indent=2)}"
        
        logger.debug(f"Prompt built: {len(prompt)} characters")
        return prompt
    
    def _call_api(self, prompt: str) -> str:
        """
        Make API call to Gemini using new SDK.
        
        Args:
            prompt: Complete prompt text
            
        Returns:
            Gemini's response text
            
        Raises:
            Exception: On API errors
        """
        logger.debug(f"Calling Gemini API (model: {self.model_name})")
        
        start_time = time.time()
        
        # New SDK uses client.models.generate_content (stateless)
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        
        elapsed = time.time() - start_time
        
        logger.debug(f"Response received in {elapsed:.2f}s")
        
        return response.text
    
    def _parse_response(self, response_text: str) -> AIRiskAnalysis:
        """
        Parse Gemini's JSON response into structured object.
        
        Args:
            response_text: Raw response from Gemini
            
        Returns:
            AIRiskAnalysis object
            
        Raises:
            GeminiClientError: If response cannot be parsed
        """
        logger.debug("Parsing API response")
        
        try:
            # Clean up common formatting issues
            cleaned = response_text.strip()
            
            # Remove markdown code blocks if present
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
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
                raise GeminiClientError(error_msg)
            
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
            raise GeminiClientError(error_msg)
        
        except (KeyError, TypeError, ValueError) as e:
            error_msg = f"Invalid response structure: {e}"
            logger.error(error_msg)
            raise GeminiClientError(error_msg)


# Alias for compatibility with existing code
ClaudeClient = GeminiClient
ClaudeClientError = GeminiClientError


# Module-level test
if __name__ == "__main__":
    """Test Gemini API client with sample use case."""
    logger.info("Running Gemini API client test")
    
    try:
        # Initialize client
        client = GeminiClient()
        
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
        
        logger.info("Testing AI use case analysis with REAL Gemini API...")
        analysis = client.analyze_use_case(use_case, context)
        
        # Display results
        logger.info("=" * 60)
        logger.info("REAL AI ANALYSIS RESULTS (Gemini 1.5 Flash)")
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
        
        logger.info("✅ Gemini API client test successful!")
        logger.info("🎉 You're now using REAL AI - completely FREE!")
        
    except GeminiClientError as e:
        logger.error(f"❌ Test failed: {e}")
        
    except Exception as e:
        logger.critical(f"❌ Unexpected error: {e}", exc_info=True)