"""
Filament cost analysis and reporting module.

This module provides functionality for analyzing filament usage, costs,
and generating various reports for better cost management.
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
import logging
import statistics
from dataclasses import dataclass, asdict
from enum import Enum
import csv

from src.utils.error_logger import ErrorLogger

class TimePeriod(Enum):
    """Time periods for cost analysis reports."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    ALL_TIME = "all_time"

@dataclass
class CostReport:
    """Data class for storing cost analysis results."""
    period: str
    start_date: str
    end_date: str
    total_filament_used_g: float
    total_cost: float
    cost_per_gram: float
    filament_usage_by_type: Dict[str, float]  # {filament_type: grams_used}
    cost_by_type: Dict[str, float]  # {filament_type: cost}
    projects_completed: int
    cost_per_project: float
    most_used_filament: str
    least_used_filament: str
    
    def to_dict(self) -> Dict:
        """Convert the report to a dictionary."""
        return asdict(self)
    
    def to_json(self, pretty: bool = True) -> str:
        """Convert the report to a JSON string."""
        indent = 2 if pretty else None
        return json.dumps(self.to_dict(), indent=indent)
    
    def to_csv(self, filepath: Optional[str] = None) -> Optional[str]:
        """
        Convert the report to CSV format.
        
        Args:
            filepath: If provided, save the CSV to this file
            
        Returns:
            str: CSV content if filepath is None, else None
        """
        data = self.to_dict()
        
        # Flatten nested dictionaries
        flat_data = {}
        for key, value in data.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    flat_data[f"{key}_{subkey}"] = subvalue
            else:
                flat_data[key] = value
        
        # Create CSV content
        output = []
        headers = list(flat_data.keys())
        output.append(",".join(headers))
        row = [str(flat_data[header]) for header in headers]
        output.append(",".join(row))
        
        csv_content = "\n".join(output)
        
        if filepath:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                f.write(csv_content)
            return None
        return csv_content


class CostAnalyzer:
    """
    Analyzes filament usage and costs over time.
    
    Features:
    - Track filament usage by project, time period, and filament type
    - Calculate costs and generate reports
    - Export data in various formats (JSON, CSV)
    - Identify cost-saving opportunities
    """
    
    def __init__(self, data_dir: str = 'data'):
        """
        Initialize the CostAnalyzer.
        
        Args:
            data_dir: Directory containing filament usage data
        """
        self.data_dir = data_dir
        self.usage_file = os.path.join(data_dir, 'filament_usage.json')
        self.logger = logging.getLogger(__name__)
        self._ensure_data_file()
    
    def _ensure_data_file(self) -> None:
        """Ensure the data file exists with proper structure."""
        os.makedirs(self.data_dir, exist_ok=True)
        if not os.path.exists(self.usage_file):
            with open(self.usage_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'version': '1.0',
                    'entries': [],
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
    
    def record_usage(self, project_id: str, filament_id: str, filament_type: str,
                    grams_used: float, cost_per_gram: float, 
                    timestamp: Optional[datetime] = None) -> None:
        """
        Record filament usage for a project.
        
        Args:
            project_id: Unique identifier for the project
            filament_id: Unique identifier for the filament spool
            filament_type: Type of filament (e.g., PLA, PETG, ABS)
            grams_used: Amount of filament used in grams
            cost_per_gram: Cost per gram of filament
            timestamp: When the usage occurred (defaults to now)
        """
        try:
            if not timestamp:
                timestamp = datetime.now()
            
            entry = {
                'id': str(len(self._load_entries()) + 1),
                'project_id': project_id,
                'filament_id': filament_id,
                'filament_type': filament_type,
                'grams_used': float(grams_used),
                'cost_per_gram': float(cost_per_gram),
                'total_cost': float(grams_used * cost_per_gram),
                'timestamp': timestamp.isoformat(),
                'recorded_at': datetime.now().isoformat()
            }
            
            data = self._load_data()
            data['entries'].append(entry)
            data['last_updated'] = datetime.now().isoformat()
            
            self._save_data(data)
            self.logger.info(f"Recorded usage: {grams_used}g of {filament_type} for project {project_id}")
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'record_usage',
                'project_id': project_id,
                'filament_id': filament_id,
                'filament_type': filament_type,
                'grams_used': grams_used
            })
            raise
    
    def generate_report(self, period: TimePeriod = TimePeriod.ALL_TIME,
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None) -> CostReport:
        """
        Generate a cost analysis report for the specified time period.
        
        Args:
            period: Time period for the report
            start_date: Optional start date (overrides period)
            end_date: Optional end date (defaults to now)
            
        Returns:
            CostReport: The generated report
        """
        try:
            entries = self._filter_entries(period, start_date, end_date)
            
            if not entries:
                raise ValueError("No data available for the specified period")
            
            # Calculate basic statistics
            total_grams = sum(entry['grams_used'] for entry in entries)
            total_cost = sum(entry['total_cost'] for entry in entries)
            
            # Group by filament type
            usage_by_type = {}
            cost_by_type = {}
            
            for entry in entries:
                f_type = entry['filament_type']
                usage_by_type[f_type] = usage_by_type.get(f_type, 0) + entry['grams_used']
                cost_by_type[f_type] = cost_by_type.get(f_type, 0) + entry['total_cost']
            
            # Find most and least used filament types
            if usage_by_type:
                most_used = max(usage_by_type.items(), key=lambda x: x[1])[0]
                least_used = min(usage_by_type.items(), key=lambda x: x[1])[0]
            else:
                most_used = "N/A"
                least_used = "N/A"
            
            # Count unique projects
            project_count = len(set(entry['project_id'] for entry in entries))
            
            # Calculate cost per gram (weighted average)
            cost_per_gram = total_cost / total_grams if total_grams > 0 else 0
            
            # Calculate cost per project
            cost_per_project = total_cost / project_count if project_count > 0 else 0
            
            # Determine date range
            timestamps = [datetime.fromisoformat(e['timestamp']) for e in entries]
            start = min(timestamps)
            end = max(timestamps)
            
            report = CostReport(
                period=period.value,
                start_date=start.isoformat(),
                end_date=end.isoformat(),
                total_filament_used_g=round(total_grams, 2),
                total_cost=round(total_cost, 2),
                cost_per_gram=round(cost_per_gram, 4),
                filament_usage_by_type={k: round(v, 2) for k, v in usage_by_type.items()},
                cost_by_type={k: round(v, 2) for k, v in cost_by_type.items()},
                projects_completed=project_count,
                cost_per_project=round(cost_per_project, 2),
                most_used_filament=most_used,
                least_used_filament=least_used
            )
            
            return report
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'generate_report',
                'period': period.value if hasattr(period, 'value') else str(period),
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat() if end_date else None
            })
            raise
    
    def export_report(self, report: CostReport, format: str = 'json',
                     output_dir: str = 'reports') -> str:
        """
        Export a cost report to a file.
        
        Args:
            report: The CostReport to export
            format: Output format ('json' or 'csv')
            output_dir: Directory to save the report
            
        Returns:
            str: Path to the generated report file
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            # Create a filename based on the report period and date range
            start_date = report.start_date.split('T')[0]  # Just the date part
            end_date = report.end_date.split('T')[0]
            filename = f"cost_report_{report.period}_{start_date}_to_{end_date}"
            
            if format.lower() == 'csv':
                filepath = os.path.join(output_dir, f"{filename}.csv")
                report.to_csv(filepath)
            else:  # Default to JSON
                filepath = os.path.join(output_dir, f"{filename}.json")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(report.to_json(pretty=True))
            
            self.logger.info(f"Exported {format.upper()} report to {filepath}")
            return filepath
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'export_report',
                'format': format,
                'output_dir': output_dir
            })
            raise
    
    def get_cost_savings_recommendations(self, period: TimePeriod = TimePeriod.ALL_TIME) -> List[Dict]:
        """
        Generate cost-saving recommendations based on usage patterns.
        
        Args:
            period: Time period to analyze
            
        Returns:
            List of recommendations with potential savings
        """
        try:
            entries = self._filter_entries(period)
            if not entries:
                return []
            
            recommendations = []
            
            # Group by filament type and calculate average cost per gram
            type_data = {}
            for entry in entries:
                f_type = entry['filament_type']
                if f_type not in type_data:
                    type_data[f_type] = {
                        'total_grams': 0,
                        'total_cost': 0,
                        'prices': [],
                        'usage_count': 0
                    }
                
                type_data[f_type]['total_grams'] += entry['grams_used']
                type_data[f_type]['total_cost'] += entry['total_cost']
                type_data[f_type]['prices'].append(entry['cost_per_gram'])
                type_data[f_type]['usage_count'] += 1
            
            # Calculate average costs and identify potential savings
            for f_type, data in type_data.items():
                avg_cost = data['total_cost'] / data['total_grams'] if data['total_grams'] > 0 else 0
                min_price = min(data['prices']) if data['prices'] else 0
                
                if avg_cost > min_price * 1.1:  # At least 10% more expensive
                    potential_savings = (avg_cost - min_price) * data['total_grams']
                    
                    recommendations.append({
                        'filament_type': f_type,
                        'current_avg_cost_per_gram': round(avg_cost, 4),
                        'min_observed_cost_per_gram': round(min_price, 4),
                        'potential_savings': round(potential_savings, 2),
                        'recommendation': f"Consider buying {f_type} in bulk or from a cheaper supplier. "
                                       f"You could save up to ${potential_savings:.2f} per {data['total_grams']}g."
                    })
            
            # Sort by potential savings (highest first)
            recommendations.sort(key=lambda x: x['potential_savings'], reverse=True)
            
            return recommendations
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'get_cost_savings_recommendations',
                'period': period.value if hasattr(period, 'value') else str(period)
            })
            raise
    
    def _load_data(self) -> Dict:
        """Load the usage data from file."""
        try:
            with open(self.usage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is corrupted or doesn't exist, return empty structure
            return {
                'version': '1.0',
                'entries': [],
                'last_updated': datetime.now().isoformat()
            }
    
    def _save_data(self, data: Dict) -> None:
        """Save the usage data to file."""
        with open(self.usage_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _load_entries(self) -> List[Dict]:
        """Load just the entries from the data file."""
        data = self._load_data()
        return data.get('entries', [])
    
    def _filter_entries(self, period: TimePeriod = TimePeriod.ALL_TIME,
                       start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None) -> List[Dict]:
        """
        Filter entries based on time period or custom date range.
        
        Args:
            period: Time period to filter by
            start_date: Custom start date (overrides period)
            end_date: Custom end date (defaults to now)
            
        Returns:
            List of filtered entries
        """
        entries = self._load_entries()
        
        if not entries:
            return []
        
        now = datetime.now()
        
        # If custom date range is provided, use that
        if start_date is not None:
            if end_date is None:
                end_date = now
            
            return [
                e for e in entries
                if start_date <= datetime.fromisoformat(e['timestamp']) <= end_date
            ]
        
        # Otherwise, use the specified period
        if period == TimePeriod.ALL_TIME:
            return entries
        
        # Calculate date range based on period
        if period == TimePeriod.DAILY:
            start = now - timedelta(days=1)
        elif period == TimePeriod.WEEKLY:
            start = now - timedelta(weeks=1)
        elif period == TimePeriod.MONTHLY:
            start = now - timedelta(days=30)
        elif period == TimePeriod.YEARLY:
            start = now - timedelta(days=365)
        else:
            return entries
        
        return [
            e for e in entries
            if datetime.fromisoformat(e['timestamp']) >= start
        ]


def analyze_filament_costs(data_dir: str = 'data', 
                          output_format: str = 'json') -> Dict:
    """
    Convenience function to quickly analyze filament costs.
    
    Args:
        data_dir: Directory containing filament data
        output_format: Output format ('json' or 'dict')
        
    Returns:
        Analysis results in the requested format
    """
    analyzer = CostAnalyzer(data_dir)
    
    # Generate reports for different time periods
    reports = {
        'weekly': analyzer.generate_report(TimePeriod.WEEKLY).to_dict(),
        'monthly': analyzer.generate_report(TimePeriod.MONTHLY).to_dict(),
        'yearly': analyzer.generate_report(TimePeriod.YEARLY).to_dict(),
        'all_time': analyzer.generate_report(TimePeriod.ALL_TIME).to_dict(),
        'recommendations': analyzer.get_cost_savings_recommendations()
    }
    
    if output_format.lower() == 'json':
        return json.dumps(reports, indent=2)
    
    return reports
