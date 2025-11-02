"""
Roster Calculator for JuniorLeague
Manages team rosters, salary caps, and contract tracking
"""
from typing import List, Dict
from datetime import datetime


class RosterCalculator:
    """Calculates roster information and cap compliance"""
    
    LEAGUE_BUDGET = 280  # Junior League auction budget
    
    def calculate_team_info(self, team, players: List, contracts: List) -> Dict:
        """
        Calculate comprehensive team information
        
        Args:
            team: Team object
            players: List of Player objects on the team
            contracts: List of Contract objects for the team
        
        Returns:
            Dictionary with team roster info
        """
        total_salary = sum(c.salary for c in contracts)
        remaining_budget = self.LEAGUE_BUDGET - total_salary
        
        # Count contract types
        keeper_count = sum(1 for c in contracts if c.contract_type == 'auction_keeper')
        in_season_count = sum(1 for c in contracts if c.contract_type == 'in_season')
        rotation_count = sum(1 for c in contracts if c.contract_type == 'rotation')
        
        roster_info = {
            'team_name': team.name,
            'owner': team.owner,
            'total_salary': total_salary,
            'remaining_budget': remaining_budget,
            'budget_percentage_used': (total_salary / self.LEAGUE_BUDGET) * 100,
            'roster_size': len(players),
            'contract_breakdown': {
                'keepers': keeper_count,
                'in_season': in_season_count,
                'rotation': rotation_count
            },
            'players': []
        }
        
        # Add player details
        for player, contract in zip(players, contracts):
            roster_info['players'].append({
                'name': player.name,
                'position': player.position,
                'salary': contract.salary,
                'contract_type': contract.contract_type,
                'years_remaining': contract.years_remaining
            })
        
        return roster_info
    
    def calculate_remaining_auction_budget(self, team, contracts: List) -> Dict:
        """
        Calculate how much budget remains for auction
        
        Args:
            team: Team object
            contracts: List of existing Contract objects
        
        Returns:
            Dictionary with auction budget info
        """
        total_committed = sum(c.salary for c in contracts)
        remaining = self.LEAGUE_BUDGET - total_committed
        
        return {
            'total_budget': self.LEAGUE_BUDGET,
            'committed_salary': total_committed,
            'remaining_budget': remaining,
            'can_bid': remaining > 0
        }
    
    def validate_roster_add(
        self, 
        team, 
        player, 
        proposed_salary: int,
        existing_contracts: List
    ) -> Dict:
        """
        Validate if adding a player to roster is allowed
        
        Args:
            team: Team object
            player: Player object to add
            proposed_salary: Salary being proposed
            existing_contracts: List of existing contracts
        
        Returns:
            Dictionary with validation results
        """
        total_current = sum(c.salary for c in existing_contracts)
        total_with_new = total_current + proposed_salary
        
        validation = {
            'valid': True,
            'reasons': []
        }
        
        # Check budget
        if total_with_new > self.LEAGUE_BUDGET:
            validation['valid'] = False
            validation['reasons'].append(
                f"Would exceed budget: ${total_with_new} > ${self.LEAGUE_BUDGET}"
            )
        
        # Check if player already on roster
        if player.roster_team_id and player.roster_team_id != team.id:
            validation['valid'] = False
            validation['reasons'].append(
                f"Player is on {player.team.name}'s roster"
            )
        
        return validation
    
    def get_contract_timeline(self, contracts: List) -> List[Dict]:
        """
        Get contract timeline showing when contracts expire
        
        Args:
            contracts: List of Contract objects
        
        Returns:
            List of dictionaries with contract timeline info
        """
        timeline = []
        
        for contract in contracts:
            contract_info = {
                'player_name': contract.player.name,
                'salary': contract.salary,
                'years_remaining': contract.years_remaining,
                'expires_year': contract.year + contract.years_remaining,
                'contract_type': contract.contract_type
            }
            timeline.append(contract_info)
        
        # Sort by expiration year
        timeline.sort(key=lambda x: x['expires_year'])
        
        return timeline

