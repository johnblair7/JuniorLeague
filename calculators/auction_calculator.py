"""
Auction Calculator for JuniorLeague
Provides bidding recommendations based on historical data and projections
"""
import statistics
from typing import List, Dict, Optional


class AuctionCalculator:
    """Calculates recommended auction bids based on multiple factors"""
    
    def calculate_bid(
        self, 
        player_name: str, 
        historical_data: List, 
        projected_stats: Optional[object]
    ) -> Dict:
        """
        Calculate recommended bid range for a player
        
        Args:
            player_name: Name of the player
            historical_data: List of HistoricalAuction objects
            projected_stats: ProjectedStats object (optional)
        
        Returns:
            Dictionary with recommended bid info
        """
        recommendation = {
            'player_name': player_name,
            'recommended_bid': 0,
            'bid_range': {'min': 0, 'max': 0, 'avg': 0},
            'confidence': 'low',
            'reasoning': []
        }
        
        # Calculate from historical auction data
        if historical_data:
            historical_bids = [h.salary for h in historical_data]
            recommendation['bid_range'] = {
                'min': min(historical_bids),
                'max': max(historical_bids),
                'avg': statistics.mean(historical_bids),
                'median': statistics.median(historical_bids)
            }
            
            # Use median as baseline (less affected by outliers)
            recommendation['recommended_bid'] = int(recommendation['bid_range']['median'])
            
            # Confidence based on sample size
            if len(historical_bids) >= 3:
                recommendation['confidence'] = 'high'
            elif len(historical_bids) >= 1:
                recommendation['confidence'] = 'medium'
            
            recommendation['reasoning'].append(
                f"Based on {len(historical_bids)} historical auction(s): "
                f"${recommendation['bid_range']['min']}-${recommendation['bid_range']['max']} "
                f"(avg: ${recommendation['bid_range']['avg']:.0f})"
            )
        else:
            recommendation['reasoning'].append("No historical auction data available")
        
        # Adjust based on projected stats if available
        if projected_stats and projected_stats.projected_value:
            projected_value = projected_stats.projected_value
            
            # Weight the recommendation
            if historical_data:
                # Blend historical and projected: 60% historical, 40% projected
                blended = 0.6 * recommendation['recommended_bid'] + 0.4 * projected_value
                recommendation['recommended_bid'] = int(blended)
            else:
                recommendation['recommended_bid'] = int(projected_value)
                recommendation['confidence'] = 'medium'
            
            recommendation['reasoning'].append(
                f"Projected value: ${projected_value:.0f}"
            )
        
        # Suggested bid range
        recommendation['suggested_range'] = {
            'low': int(recommendation['recommended_bid'] * 0.85),
            'high': int(recommendation['recommended_bid'] * 1.15)
        }
        
        return recommendation
    
    def calculate_stat_value(
        self, 
        projected_homeruns: int, 
        projected_rbis: int,
        projected_sb: int,
        projected_avg: float
    ) -> float:
        """
        Calculate dollar value based on projected stats for hitters
        This is a simplified version - you can enhance with more sophisticated formulas
        """
        # Simplified $ calculation (you'll want to tune these coefficients)
        avg_points = projected_avg * 300
        hr_points = projected_homeruns * 6
        rbi_points = projected_rbis * 2
        sb_points = projected_sb * 4
        
        total_points = avg_points + hr_points + rbi_points + sb_points
        
        # Convert to $ (rough approximation: $1 per 10 points)
        return total_points / 10
    
    def calculate_pitcher_value(
        self,
        projected_wins: int,
        projected_era: float,
        projected_k: int,
        projected_saves: int
    ) -> float:
        """
        Calculate dollar value based on projected stats for pitchers
        """
        # Simplified $ calculation for pitchers
        win_points = projected_wins * 4
        era_points = (3.50 - projected_era) * 20  # Lower ERA better
        k_points = projected_k * 0.5
        save_points = projected_saves * 6
        
        total_points = win_points + era_points + k_points + save_points
        
        return total_points / 10

