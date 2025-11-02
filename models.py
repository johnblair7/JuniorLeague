"""
Database models for JuniorLeague fantasy baseball app
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Team(db.Model):
    """Represents one of the 10 teams in the league"""
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    owner = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    players = db.relationship('Player', backref='roster_team', lazy=True)
    auction_bids = db.relationship('AuctionBid', backref='bid_team', lazy=True)
    
    def __repr__(self):
        return f'<Team {self.name}>'


class Player(db.Model):
    """Represents a baseball player"""
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    fangraphs_id = db.Column(db.Integer, unique=True, nullable=True)  # Fangraphs player ID
    position = db.Column(db.String(50))  # e.g., "OF", "SP", "C"
    mlb_team = db.Column(db.String(10))  # MLB team abbreviation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Roster information
    roster_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    
    # Relationships
    contracts = db.relationship('Contract', backref='player', lazy=True, cascade='all, delete-orphan')
    historical_data = db.relationship('HistoricalAuction', backref='player', lazy=True)
    
    def __repr__(self):
        return f'<Player {self.name}>'


class Contract(db.Model):
    """Represents a contract for a player"""
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    
    # Contract details
    salary = db.Column(db.Integer, nullable=False)  # Dollar amount
    contract_type = db.Column(db.String(50), nullable=False)  # 'auction_keeper', 'in_season', 'rotation'
    year = db.Column(db.Integer, nullable=False)  # Season year
    years_remaining = db.Column(db.Integer, default=0)  # Years left on contract
    
    # Additional metadata
    rotation_round = db.Column(db.Integer, nullable=True)  # For rotation round contracts
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Contract {self.salary}$ {self.contract_type}>'


class HistoricalAuction(db.Model):
    """Historical auction data for statistical analysis"""
    __tablename__ = 'historical_auctions'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    
    # Auction details
    year = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    contract_type = db.Column(db.String(50), nullable=False)
    
    # Player stats for that season
    batting_avg = db.Column(db.Float)
    home_runs = db.Column(db.Integer)
    rbis = db.Column(db.Integer)
    stolen_bases = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    era = db.Column(db.Float)
    strikeouts = db.Column(db.Integer)
    saves = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<HistoricalAuction {self.year}: ${self.salary}>'


class ProjectedStats(db.Model):
    """Projected statistics for players"""
    __tablename__ = 'projected_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    # Projected stats
    projected_batting_avg = db.Column(db.Float)
    projected_home_runs = db.Column(db.Integer)
    projected_rbis = db.Column(db.Integer)
    projected_stolen_bases = db.Column(db.Integer)
    projected_wins = db.Column(db.Integer)
    projected_era = db.Column(db.Float)
    projected_strikeouts = db.Column(db.Integer)
    projected_saves = db.Column(db.Integer)
    
    # Dollar value calculation
    projected_value = db.Column(db.Float)
    source = db.Column(db.String(100))  # 'fangraphs', 'steamer', etc.
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProjectedStats {self.player_id} {self.year}>'


class AuctionBid(db.Model):
    """Live auction tracking"""
    __tablename__ = 'auction_bids'
    
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    
    bid_amount = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Bid status
    is_winning = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<AuctionBid ${self.bid_amount}>'

