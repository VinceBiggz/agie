"""
CSV parser for risk register data with validation.

This module handles ingestion and validation of risk register CSV files,
ensuring data quality before analysis.

@author: Vincent Wachira
@date: 2025-02-14
@version: 0.1.0
@license: MIT
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

from src.logger import logger

@dataclass
class RiskRegisterSchema:
    """
    Expected schema for risk register CSV files.
    
    Attributes:
        required_columns: Column names that must exist in CSV
        optional_columns: Column names that are optional
        valid_likelihood_values: Acceptable likelihood ratings (1-5 scale)
        valid_impact_values: Acceptable impact ratings (1-5 scale)
    """
    required_columns: List[str] = None
    optional_columns: List[str] = None
    valid_likelihood_values: List[int] = None
    valid_impact_values: List[int] = None
    
    def __post_init__(self):
        """Initialize default schema values."""
        if self.required_columns is None:
            self.required_columns = [
                'risk_id',
                'risk_description',
                'likelihood',
                'impact'
            ]
        
        if self.optional_columns is None:
            self.optional_columns = [
                'category',
                'owner',
                'mitigation',
                'status'
            ]
        
        if self.valid_likelihood_values is None:
            self.valid_likelihood_values = [1, 2, 3, 4, 5]
        
        if self.valid_impact_values is None:
            self.valid_impact_values = [1, 2, 3, 4, 5]


class CSVParserError(Exception):
    """Custom exception for CSV parsing errors."""
    pass


class CSVParser:
    """
    Parser for risk register CSV files.
    
    This class handles loading, validation, and normalization of risk data
    from CSV files.
    
    Example:
        >>> parser = CSVParser()
        >>> df = parser.parse('data/risks.csv')
        >>> print(f"Loaded {len(df)} risks")
    """
    
    def __init__(self, schema: Optional[RiskRegisterSchema] = None):
        """
        Initialize CSV parser with optional custom schema.
        
        Args:
            schema: Custom schema definition. Uses default if None.
        """
        self.schema = schema or RiskRegisterSchema()
        logger.info("CSVParser initialized")
        logger.debug(f"Required columns: {self.schema.required_columns}")
    
    def parse(self, filepath: Path | str) -> pd.DataFrame:
        """
        Parse and validate risk register CSV file.
        
        Args:
            filepath: Path to CSV file (string or Path object)
            
        Returns:
            Validated pandas DataFrame with risk data
            
        Raises:
            CSVParserError: If file doesn't exist, format is invalid, or validation fails
            
        Example:
            >>> parser = CSVParser()
            >>> risks = parser.parse('data/sample_risk_register.csv')
        """
        filepath = Path(filepath)
        logger.info(f"Starting CSV parsing: {filepath}")
        
        # Step 1: Check file exists
        if not filepath.exists():
            error_msg = f"File not found: {filepath}"
            logger.error(error_msg)
            raise CSVParserError(error_msg)
        
        # Step 2: Load CSV
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Successfully loaded CSV: {len(df)} rows, {len(df.columns)} columns")
        except Exception as e:
            error_msg = f"Failed to read CSV file: {e}"
            logger.error(error_msg)
            raise CSVParserError(error_msg)
        
        # Step 3: Validate schema
        self._validate_schema(df)
        
        # Step 4: Validate data values
        self._validate_data(df)
        
        # Step 5: Normalize data
        df = self._normalize_data(df)
        
        logger.info(f"CSV parsing complete: {len(df)} valid risks loaded")
        return df
    
    def _validate_schema(self, df: pd.DataFrame) -> None:
        """
        Validate that required columns exist in DataFrame.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            CSVParserError: If required columns are missing
        """
        missing_columns = [
            col for col in self.schema.required_columns 
            if col not in df.columns
        ]
        
        if missing_columns:
            error_msg = f"Missing required columns: {missing_columns}"
            logger.error(error_msg)
            logger.debug(f"Available columns: {list(df.columns)}")
            raise CSVParserError(error_msg)
        
        logger.debug("Schema validation passed")
    
    def _validate_data(self, df: pd.DataFrame) -> None:
        """
        Validate data values in required columns.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            CSVParserError: If data validation fails
        """
        # Check for empty risk_id or risk_description
        if df['risk_id'].isna().any():
            error_msg = "Found empty risk_id values"
            logger.error(error_msg)
            raise CSVParserError(error_msg)
        
        if df['risk_description'].isna().any():
            error_msg = "Found empty risk_description values"
            logger.error(error_msg)
            raise CSVParserError(error_msg)
        
        # Validate likelihood values
        invalid_likelihood = df[
            ~df['likelihood'].isin(self.schema.valid_likelihood_values)
        ]
        if not invalid_likelihood.empty:
            error_msg = (
                f"Invalid likelihood values found. "
                f"Must be one of: {self.schema.valid_likelihood_values}"
            )
            logger.error(error_msg)
            logger.debug(f"Invalid rows: {invalid_likelihood['risk_id'].tolist()}")
            raise CSVParserError(error_msg)
        
        # Validate impact values
        invalid_impact = df[
            ~df['impact'].isin(self.schema.valid_impact_values)
        ]
        if not invalid_impact.empty:
            error_msg = (
                f"Invalid impact values found. "
                f"Must be one of: {self.schema.valid_impact_values}"
            )
            logger.error(error_msg)
            logger.debug(f"Invalid rows: {invalid_impact['risk_id'].tolist()}")
            raise CSVParserError(error_msg)
        
        logger.debug("Data validation passed")
    
    def _normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize data for consistent processing.
        
        Args:
            df: DataFrame to normalize
            
        Returns:
            Normalized DataFrame
        """
        # Strip whitespace from string columns
        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            df[col] = df[col].str.strip()
        
        # Ensure numeric types for likelihood and impact
        df['likelihood'] = df['likelihood'].astype(int)
        df['impact'] = df['impact'].astype(int)
        
        # Calculate risk score (likelihood × impact)
        df['risk_score'] = df['likelihood'] * df['impact']
        
        logger.debug("Data normalization complete")
        return df
    
    def get_summary(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Generate summary statistics for parsed risk data.
        
        Args:
            df: Parsed DataFrame
            
        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'total_risks': len(df),
            'average_likelihood': df['likelihood'].mean(),
            'average_impact': df['impact'].mean(),
            'average_risk_score': df['risk_score'].mean(),
            'high_risk_count': len(df[df['risk_score'] >= 15]),  # Score 15+ = High risk
            'columns': list(df.columns)
        }
        
        logger.debug(f"Summary generated: {summary}")
        return summary


# Module-level test
if __name__ == "__main__":
    """Test CSV parser with sample data."""
    logger.info("Running CSV parser module test")
    
    # This will fail initially (no sample file yet)
    # We'll create the sample CSV in the next step
    try:
        parser = CSVParser()
        sample_file = Path(__file__).parent.parent.parent / 'data' / 'sample_risk_register.csv'
        
        if sample_file.exists():
            df = parser.parse(sample_file)
            summary = parser.get_summary(df)
            
            logger.info("Test Results:")
            logger.info(f"  Total risks: {summary['total_risks']}")
            logger.info(f"  Avg risk score: {summary['average_risk_score']:.2f}")
            logger.info(f"  High risks: {summary['high_risk_count']}")
        else:
            logger.warning(f"Sample file not found: {sample_file}")
            logger.info("Create sample CSV to test parser")
    
    except Exception as e:
        logger.error(f"Test failed: {e}")