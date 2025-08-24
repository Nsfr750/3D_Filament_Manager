"""
Filament price tracking module.

This module provides functionality for tracking historical filament prices,
calculating price trends, and notifying users of price changes.
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Union, Any
from pathlib import Path
import logging
from dataclasses import dataclass, asdict, field
import statistics
from enum import Enum

from src.utils.error_logger import ErrorLogger

class PriceTrend(Enum):
    """Enum for price trend directions."""
    STABLE = "stable"
    INCREASING = "increasing"
    DECREASING = "decreasing"
    FLUCTUATING = "fluctuating"

@dataclass
class PriceEntry:
    """Data class for a single price entry."""
    filament_id: str
    filament_type: str
    price_per_gram: float
    currency: str = "USD"
    source: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PriceEntry':
        """Create from dictionary."""
        return cls(**data)

@dataclass
class PriceHistory:
    """Data class for price history of a specific filament."""
    filament_id: str
    filament_type: str
    entries: List[PriceEntry] = field(default_factory=list)
    
    def add_entry(self, entry: PriceEntry) -> None:
        """Add a price entry to the history."""
        if entry.filament_id != self.filament_id:
            raise ValueError("Entry filament_id does not match history filament_id")
        self.entries.append(entry)
        self.entries.sort(key=lambda x: x.timestamp)
    
    def get_latest_price(self) -> Optional[PriceEntry]:
        """Get the most recent price entry."""
        if not self.entries:
            return None
        return max(self.entries, key=lambda x: x.timestamp)
    
    def get_price_trend(self, days: int = 30) -> Tuple[PriceTrend, float]:
        """
        Calculate the price trend over the specified number of days.
        
        Args:
            days: Number of days to consider for trend analysis
            
        Returns:
            Tuple of (trend, percentage_change)
        """
        if len(self.entries) < 2:
            return PriceTrend.STABLE, 0.0
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_entries = [
            e for e in self.entries 
            if datetime.fromisoformat(e.timestamp) >= cutoff_date
        ]
        
        if len(recent_entries) < 2:
            return PriceTrend.STABLE, 0.0
        
        # Calculate percentage changes between consecutive entries
        changes = []
        for i in range(1, len(recent_entries)):
            prev = recent_entries[i-1].price_per_gram
            curr = recent_entries[i].price_per_gram
            if prev > 0:  # Avoid division by zero
                change = ((curr - prev) / prev) * 100
                changes.append(change)
        
        if not changes:
            return PriceTrend.STABLE, 0.0
        
        avg_change = statistics.mean(changes)
        
        # Determine trend based on average change
        if abs(avg_change) < 0.5:  # Less than 0.5% change
            return PriceTrend.STABLE, avg_change
        elif avg_change > 0:
            return PriceTrend.INCREASING, avg_change
        else:
            return PriceTrend.DECREASING, avg_change
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'filament_id': self.filament_id,
            'filament_type': self.filament_type,
            'entries': [e.to_dict() for e in self.entries]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PriceHistory':
        """Create from dictionary."""
        history = cls(
            filament_id=data['filament_id'],
            filament_type=data['filament_type']
        )
        for entry_data in data.get('entries', []):
            history.add_entry(PriceEntry.from_dict(entry_data))
        return history

class PriceTracker:
    """
    Tracks historical filament prices and analyzes price trends.
    
    Features:
    - Record price changes over time
    - Calculate price trends and statistics
    - Get price alerts for significant changes
    - Export price history data
    """
    
    def __init__(self, data_dir: str = 'data'):
        """
        Initialize the PriceTracker.
        
        Args:
            data_dir: Directory to store price history data
        """
        self.data_dir = data_dir
        self.history_file = os.path.join(data_dir, 'price_history.json')
        self.logger = logging.getLogger(__name__)
        self._ensure_data_file()
    
    def _ensure_data_file(self) -> None:
        """Ensure the data file exists with proper structure."""
        os.makedirs(self.data_dir, exist_ok=True)
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'version': '1.0',
                    'last_updated': datetime.now().isoformat(),
                    'histories': {}
                }, f, indent=2)
    
    def record_price(self, filament_id: str, filament_type: str, 
                    price_per_gram: float, source: Optional[str] = None,
                    metadata: Optional[Dict] = None) -> PriceEntry:
        """
        Record a new price for a filament.
        
        Args:
            filament_id: Unique identifier for the filament
            filament_type: Type of filament (e.g., PLA, PETG)
            price_per_gram: Price per gram in the filament's currency
            source: Optional source of the price (e.g., 'manual', 'api:amazon')
            metadata: Additional metadata about the price entry
            
        Returns:
            The created PriceEntry
        """
        try:
            entry = PriceEntry(
                filament_id=filament_id,
                filament_type=filament_type,
                price_per_gram=price_per_gram,
                source=source,
                metadata=metadata or {}
            )
            
            data = self._load_data()
            histories = data.get('histories', {})
            
            if filament_id not in histories:
                histories[filament_id] = PriceHistory(
                    filament_id=filament_id,
                    filament_type=filament_type
                ).to_dict()
            
            # Add the new entry
            entry_dict = entry.to_dict()
            histories[filament_id]['entries'].append(entry_dict)
            
            # Update the last_updated timestamp
            data['last_updated'] = datetime.now().isoformat()
            data['histories'] = histories
            
            self._save_data(data)
            self.logger.info(f"Recorded price for {filament_id}: {price_per_gram}/g")
            
            return entry
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'record_price',
                'filament_id': filament_id,
                'filament_type': filament_type,
                'price_per_gram': price_per_gram
            })
            raise
    
    def get_price_history(self, filament_id: str) -> Optional[PriceHistory]:
        """
        Get the price history for a specific filament.
        
        Args:
            filament_id: ID of the filament to get history for
            
        Returns:
            PriceHistory object if found, None otherwise
        """
        try:
            data = self._load_data()
            history_data = data.get('histories', {}).get(filament_id)
            
            if not history_data:
                return None
                
            return PriceHistory.from_dict(history_data)
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'get_price_history',
                'filament_id': filament_id
            })
            raise
    
    def get_all_histories(self) -> Dict[str, PriceHistory]:
        """
        Get price histories for all tracked filaments.
        
        Returns:
            Dictionary mapping filament IDs to PriceHistory objects
        """
        try:
            data = self._load_data()
            return {
                fid: PriceHistory.from_dict(h_data)
                for fid, h_data in data.get('histories', {}).items()
            }
        except Exception as e:
            ErrorLogger.log_error(e, {'action': 'get_all_histories'})
            raise
    
    def get_price_alerts(self, threshold_pct: float = 5.0, 
                        days: int = 7) -> List[Dict]:
        """
        Get alerts for significant price changes.
        
        Args:
            threshold_pct: Minimum percentage change to trigger an alert
            days: Number of days to look back for changes
            
        Returns:
            List of alert dictionaries with details about price changes
        """
        try:
            alerts = []
            histories = self.get_all_histories()
            
            for history in histories.values():
                if len(history.entries) < 2:
                    continue
                
                # Get entries within the specified time frame
                cutoff_date = datetime.now() - timedelta(days=days)
                recent_entries = [
                    e for e in history.entries
                    if datetime.fromisoformat(e.timestamp) >= cutoff_date
                ]
                
                if len(recent_entries) < 2:
                    continue
                
                # Calculate price change
                first_price = recent_entries[0].price_per_gram
                latest_price = recent_entries[-1].price_per_gram
                change_pct = ((latest_price - first_price) / first_price) * 100
                
                if abs(change_pct) >= threshold_pct:
                    alerts.append({
                        'filament_id': history.filament_id,
                        'filament_type': history.filament_type,
                        'old_price': first_price,
                        'new_price': latest_price,
                        'change_pct': change_pct,
                        'change_direction': 'increase' if change_pct > 0 else 'decrease',
                        'first_seen': recent_entries[0].timestamp,
                        'last_updated': recent_entries[-1].timestamp,
                        'num_changes': len(recent_entries) - 1
                    })
            
            # Sort by absolute percentage change (largest first)
            alerts.sort(key=lambda x: abs(x['change_pct']), reverse=True)
            return alerts
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'get_price_alerts',
                'threshold_pct': threshold_pct,
                'days': days
            })
            raise
    
    def get_best_deals(self, filament_type: Optional[str] = None,
                      limit: int = 5) -> List[Dict]:
        """
        Find the best current deals on filaments.
        
        Args:
            filament_type: Optional filter for specific filament type
            limit: Maximum number of deals to return
            
        Returns:
            List of deal dictionaries, sorted by price (lowest first)
        """
        try:
            deals = []
            histories = self.get_all_histories()
            
            for history in histories.values():
                if filament_type and history.filament_type.lower() != filament_type.lower():
                    continue
                
                latest_entry = history.get_latest_price()
                if not latest_entry:
                    continue
                
                # Calculate price trend
                trend, pct_change = history.get_price_trend(days=30)
                
                deals.append({
                    'filament_id': history.filament_id,
                    'filament_type': history.filament_type,
                    'price_per_gram': latest_entry.price_per_gram,
                    'currency': latest_entry.currency,
                    'source': latest_entry.source,
                    'last_updated': latest_entry.timestamp,
                    'price_trend': trend.value,
                    'price_change_pct': pct_change,
                    'metadata': latest_entry.metadata
                })
            
            # Sort by price (lowest first) and apply limit
            deals.sort(key=lambda x: x['price_per_gram'])
            return deals[:limit]
            
        except Exception as e:
            ErrorLogger.log_error(e, {
                'action': 'get_best_deals',
                'filament_type': filament_type,
                'limit': limit
            })
            raise
    
    def _load_data(self) -> Dict:
        """Load the price history data from file."""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If file is corrupted or doesn't exist, return empty structure
            return {
                'version': '1.0',
                'last_updated': datetime.now().isoformat(),
                'histories': {}
            }
    
    def _save_data(self, data: Dict) -> None:
        """Save the price history data to file."""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)


def track_filament_price(filament_id: str, filament_type: str, 
                        price_per_gram: float, source: Optional[str] = None,
                        data_dir: str = 'data') -> Dict:
    """
    Convenience function to track a filament price.
    
    Args:
        filament_id: Unique identifier for the filament
        filament_type: Type of filament (e.g., PLA, PETG)
        price_per_gram: Price per gram in the filament's currency
        source: Optional source of the price (e.g., 'manual', 'api:amazon')
        data_dir: Directory to store price history data
        
    Returns:
        Dictionary with the recorded price entry and any relevant alerts
    """
    tracker = PriceTracker(data_dir)
    entry = tracker.record_price(filament_id, filament_type, price_per_gram, source)
    
    # Check for price alerts
    alerts = tracker.get_price_alerts(threshold_pct=5.0, days=7)
    relevant_alerts = [a for a in alerts if a['filament_id'] == filament_id]
    
    return {
        'entry': entry.to_dict(),
        'alerts': relevant_alerts
    }
