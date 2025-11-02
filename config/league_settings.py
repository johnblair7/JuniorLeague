"""
League Configuration Settings

This file will be auto-generated from your constitution
or can be manually configured if you prefer.
"""

# League Basics
LEAGUE_NAME = "Junior League"
NUM_TEAMS = 10
BUDGET = 280  # Auction budget per team

# Roster Configuration
ROSTER_SIZE = 25  # Active roster size after auction
POSITIONS = {
    'OF': 5,      # Outfielders
    'C': 2,       # Catchers
    '2B': 1,      # Second baseman
    'SS': 1,      # Shortstop
    'MIF': 1,     # Middle infielder (2B or SS)
    '1B': 1,      # First baseman
    '3B': 1,      # Third baseman
    'CO': 1,      # Corner man (1B or 3B)
    'DH': 2,      # Other hitters (DH slots)
    'P': 10,      # Pitchers
}

# Auction Rules
AUCTION_RULES = {
    'minimum_bid': 1,
    'minimum_increment': 1,
    'max_spend_required': False,  # Teams don't need to spend the full $280
    'eligibility': 'AL players on 26-man roster or AL IL as of Draft Day',
}

# Rotation Draft Rules
ROTATION_DRAFT = {
    'total_rounds': 15,
    'reserve_roster_size': 15,  # Max additional players after auction
    'exception_60day_il': True,  # Can carry 16th player on 60-day IL
    'order': '5th, 6th, 7th, 8th, 9th, 10th, 4th, 3rd, 2nd, 1st',
    'eligibility': 'Any player except NL players or already rostered',
    'no_position_requirement': True,  # Can select all pitchers, all position players, or mix
}

# Contract Types
CONTRACT_TYPES = {
    'A': {
        'description': 'One-year contract (acquired Sept 1 or later)',
        'years': 1,
        'expires_at_end_of_season': True,
    },
    'B': {
        'description': 'Second year of C contract',
        'years': 1,
        'expires_at_end_of_season': True,
    },
    'C': {
        'description': 'Standard contract (option year), 2-3 years',
        'years': 2,  # Can be extended to option year
        'option_year_allowed': True,
        'expires_at_end_of_season': False,
    },
    'F': {
        'description': 'Free agent/prospect contract (rookie)',
        'years': 'until rookie status lost',
        'loses_year_if_rookie_status_lost': False,
        'migrates_to_C': True,  # When rookie status lost
    },
    'LONG_TERM': {
        'description': 'Guaranteed long-term contract',
        'years': 1,  # Variable, adds $5 per additional year
        'salary_formula': 'current_salary + ($5 x additional_years)',
        'transferable': True,
    }
}

# Rotation Draft Salaries by Round
ROTATION_SALARIES = {
    1: 15,
    2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10, 10: 10,
    11: 5, 12: 5, 13: 5, 14: 5,
    15: 2,
}

# Keeper Rules (Freeze Day)
KEEPER_RULES = {
    'max_active_keepers': 10,  # Max players frozen on active roster
    'max_reserve_keepers': 10,  # Max players frozen on reserve roster
    'max_total_keepers': 18,  # Combined active + reserve frozen players
    'min_keepers': 0,
    'frozen_salaries_count_against_budget': True,  # Frozen salaries count vs $280 auction budget
    'active_eligibility': 'Players on AL active roster, AL IL, or AL suspended list',
    'reserve_eligibility': 'NOT on major league 26-man active roster/IL/suspended list',
    'long_term_contracts_require_notice': True,  # Must declare at freeze time
}

# Scoring Categories (Junior League Standings)
HITTING_CATEGORIES = ['OBP', 'R', 'HR', 'RBI', 'SB']
PITCHING_CATEGORIES = ['ERA', 'W', 'WHIP', 'K', 'SHOLDS']

# SHOLDS = Saves + Holds (1.0 for save, 0.5 for hold)
STANDINGS_ORDER = [
    'OBP',  # Composite On-base Percentage
    'R',    # Total Runs
    'HR',   # Total Home Runs
    'RBI',  # Total RBIs
    'SB',   # Total Stolen Bases
    'ERA',  # Composite ERA
    'W',    # Total Wins
    'WHIP', # Composite Ratio (Walks + Hits)/Innings Pitched
    'K',    # Total Strikeouts
    'SHOLDS',  # Saves + Holds (0.5 for hold, 1.0 for save)
]

