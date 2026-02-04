"""
Table Extractor Module
Specialized extraction for financial tables from IPO prospectuses
"""

import pandas as pd
from typing import List, Dict, Optional
import re
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TableExtractor:
    """
    Extract and process financial tables from prospectus
    """
    
    def __init__(self):
        self.financial_keywords = [
            'revenue', 'income', 'sales', 'turnover',
            'ebitda', 'ebit', 'profit', 'loss', 'pat',
            'assets', 'liabilities', 'equity', 'capital',
            'cash flow', 'operating', 'investing', 'financing'
        ]
        
        self.year_pattern = re.compile(r'\b(20\d{2}|FY\s*\d{2})\b')
    
    def extract_financial_statements(self, tables: List[Dict]) -> Dict:
        """
        Extract P&L, Balance Sheet, and Cash Flow statements
        
        Args:
            tables: List of table dictionaries from PDF parser
            
        Returns:
            Dictionary with financial statements
        """
        statements = {
            'profit_loss': None,
            'balance_sheet': None,
            'cash_flow': None
        }
        
        for table in tables:
            if table['type'] != 'financial':
                continue
            
            df = table['data']
            statement_type = self._identify_statement_type(df)
            
            if statement_type and statements[statement_type] is None:
                statements[statement_type] = self._process_financial_table(df)
        
        return statements
    
    def _identify_statement_type(self, df: pd.DataFrame) -> Optional[str]:
        """
        Identify type of financial statement
        """
        # Check column headers and first column
        header_text = ' '.join([str(col).lower() for col in df.columns])
        first_col_text = ' '.join([str(val).lower() for val in df.iloc[:, 0].values])
        
        combined_text = header_text + ' ' + first_col_text
        
        # Profit & Loss indicators
        if any(word in combined_text for word in ['revenue', 'income statement', 'profit', 'expenditure']):
            return 'profit_loss'
        
        # Balance Sheet indicators
        elif any(word in combined_text for word in ['balance sheet', 'assets', 'liabilities', 'equity']):
            return 'balance_sheet'
        
        # Cash Flow indicators
        elif any(word in combined_text for word in ['cash flow', 'operating activities', 'investing activities']):
            return 'cash_flow'
        
        return None
    
    def _process_financial_table(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and process financial table
        """
        # Make copy
        df = df.copy()
        
        # Identify year columns
        year_cols = []
        for col in df.columns[1:]:  # Skip first column (usually labels)
            if self.year_pattern.search(str(col)):
                year_cols.append(col)
        
        # Keep only year columns plus first column
        if year_cols:
            df = df[[df.columns[0]] + year_cols]
        
        # Convert numeric columns
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove completely empty rows
        df = df.dropna(how='all', subset=df.columns[1:])
        
        # Clean row labels
        df.iloc[:, 0] = df.iloc[:, 0].str.strip()
        
        return df
    
    def extract_metric_timeseries(self, df: pd.DataFrame, metric_name: str) -> Dict:
        """
        Extract time series for specific metric
        
        Args:
            df: Financial statement DataFrame
            metric_name: Name of metric to extract
            
        Returns:
            Dictionary of {year: value}
        """
        if df is None or df.empty:
            return {}
        
        # Find row containing metric
        metric_patterns = {
            'revenue': ['revenue', 'total revenue', 'net revenue', 'sales', 'total income'],
            'ebitda': ['ebitda', 'earnings before interest'],
            'ebit': ['ebit', 'operating profit'],
            'pat': ['pat', 'profit after tax', 'net profit'],
            'total_assets': ['total assets'],
            'total_liabilities': ['total liabilities'],
            'equity': ['equity', 'shareholders equity', 'total equity'],
            'total_debt': ['total debt', 'borrowings'],
            'cash': ['cash', 'cash and cash equivalents']
        }
        
        patterns = metric_patterns.get(metric_name, [metric_name])
        
        # Search for metric in first column
        for idx, row_label in enumerate(df.iloc[:, 0]):
            row_label_lower = str(row_label).lower()
            
            for pattern in patterns:
                if pattern in row_label_lower:
                    # Extract values from this row
                    row = df.iloc[idx]
                    
                    timeseries = {}
                    for col in df.columns[1:]:
                        year = self._extract_year(col)
                        if year and pd.notna(row[col]):
                            timeseries[year] = float(row[col])
                    
                    if timeseries:
                        return timeseries
        
        return {}
    
    def _extract_year(self, column_name: str) -> Optional[int]:
        """
        Extract year from column name
        """
        match = self.year_pattern.search(str(column_name))
        if match:
            year_str = match.group(1)
            
            # Handle FY format
            if 'FY' in year_str.upper():
                year_digits = re.search(r'\d{2}', year_str)
                if year_digits:
                    year = int(year_digits.group())
                    # Convert 2-digit to 4-digit (assuming 20XX)
                    return 2000 + year
            else:
                return int(year_str)
        
        return None
    
    def build_financial_data_dict(self, statements: Dict) -> Dict:
        """
        Build complete financial data dictionary
        
        Args:
            statements: Dictionary with P&L, Balance Sheet, Cash Flow
            
        Returns:
            Dictionary with all metrics as time series
        """
        financial_data = {}
        
        # Extract from P&L
        if statements['profit_loss'] is not None:
            pl_df = statements['profit_loss']
            
            metrics = ['revenue', 'ebitda', 'ebit', 'pat']
            for metric in metrics:
                financial_data[metric] = self.extract_metric_timeseries(pl_df, metric)
        
        # Extract from Balance Sheet
        if statements['balance_sheet'] is not None:
            bs_df = statements['balance_sheet']
            
            metrics = ['total_assets', 'total_liabilities', 'equity', 'total_debt', 'cash']
            for metric in metrics:
                financial_data[metric] = self.extract_metric_timeseries(bs_df, metric)
        
        # Extract from Cash Flow
        if statements['cash_flow'] is not None:
            cf_df = statements['cash_flow']
            
            # Cash flow metrics are more complex - would need specific extraction
            # For now, placeholder
            financial_data['operating_cash_flow'] = {}
            financial_data['investing_cash_flow'] = {}
            financial_data['financing_cash_flow'] = {}
        
        # Calculate derived metrics
        financial_data['current_assets'] = {}
        financial_data['current_liabilities'] = {}
        
        return financial_data


def main():
    """Test table extractor"""
    
    # Sample financial table
    sample_data = {
        'Particulars': ['Revenue', 'EBITDA', 'PAT', 'Total Assets', 'Equity'],
        'FY 2021': [800, 150, 80, 1000, 400],
        'FY 2022': [900, 180, 100, 1100, 480],
        'FY 2023': [1000, 200, 120, 1200, 580]
    }
    
    df = pd.DataFrame(sample_data)
    
    extractor = TableExtractor()
    
    # Test metric extraction
    revenue = extractor.extract_metric_timeseries(df, 'revenue')
    print("\nRevenue Time Series:")
    print(revenue)
    
    ebitda = extractor.extract_metric_timeseries(df, 'ebitda')
    print("\nEBITDA Time Series:")
    print(ebitda)


if __name__ == "__main__":
    main()
