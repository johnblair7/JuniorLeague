"""
JuniorLeague - Fantasy Baseball Auction & Roster Calculator
Main Flask application
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Team, Player, Contract, HistoricalAuction, ProjectedStats, AuctionBid
from calculators.auction_calculator import AuctionCalculator
from calculators.roster_calculator import RosterCalculator
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///juniorleague.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Initialize database
db.init_app(app)

# Initialize calculators
auction_calc = AuctionCalculator()
roster_calc = RosterCalculator()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/init_db')
def init_db():
    """Initialize database and create sample data"""
    with app.app_context():
        db.create_all()
        return "Database initialized!"


@app.route('/auction')
def auction():
    """Auction calculator interface"""
    # Get all players
    players = Player.query.all()
    
    # Get projected stats
    projected = ProjectedStats.query.all()
    projected_dict = {p.player_id: p for p in projected}
    
    return render_template('auction.html', players=players, projected=projected_dict)


@app.route('/roster')
def roster():
    """Roster management interface"""
    teams = Team.query.all()
    players = Player.query.filter(Player.roster_team_id.isnot(None)).all()
    
    return render_template('roster.html', teams=teams, players=players)


@app.route('/api/calculate_bid', methods=['POST'])
def calculate_bid():
    """Calculate recommended bid for a player"""
    data = request.json
    player_id = data.get('player_id')
    player_name = data.get('player_name')
    
    # Get historical data
    historical = HistoricalAuction.query.filter_by(player_name=player_name).all()
    
    # Get projected stats
    projected = ProjectedStats.query.filter_by(player_id=player_id).first()
    
    # Calculate recommendation
    recommendation = auction_calc.calculate_bid(player_name, historical, projected)
    
    return jsonify(recommendation)


@app.route('/api/teams', methods=['GET', 'POST'])
def teams():
    """Get or create teams"""
    if request.method == 'GET':
        teams = Team.query.all()
        return jsonify([{'id': t.id, 'name': t.name, 'owner': t.owner} for t in teams])
    
    elif request.method == 'POST':
        data = request.json
        team = Team(name=data['name'], owner=data['owner'])
        db.session.add(team)
        db.session.commit()
        return jsonify({'id': team.id, 'name': team.name})


@app.route('/api/players', methods=['GET', 'POST'])
def players():
    """Get or create players"""
    if request.method == 'GET':
        players = Player.query.all()
        return jsonify([{'id': p.id, 'name': p.name, 'position': p.position} for p in players])
    
    elif request.method == 'POST':
        data = request.json
        player = Player(name=data['name'], position=data.get('position'), team=data.get('team'))
        db.session.add(player)
        db.session.commit()
        return jsonify({'id': player.id, 'name': player.name})


@app.route('/api/contracts', methods=['POST'])
def create_contract():
    """Create a new contract"""
    data = request.json
    contract = Contract(
        player_id=data['player_id'],
        team_id=data['team_id'],
        salary=data['salary'],
        contract_type=data['contract_type'],
        year=data['year'],
        years_remaining=data.get('years_remaining', 0),
        rotation_round=data.get('rotation_round')
    )
    db.session.add(contract)
    db.session.commit()
    return jsonify({'id': contract.id})


@app.route('/api/live_bid', methods=['POST'])
def live_bid():
    """Record a live auction bid"""
    data = request.json
    
    # Mark all other bids for this player as not winning
    AuctionBid.query.filter_by(player_id=data['player_id']).update({'is_winning': False})
    
    bid = AuctionBid(
        player_id=data['player_id'],
        team_id=data['team_id'],
        bid_amount=data['bid_amount'],
        is_winning=True
    )
    db.session.add(bid)
    db.session.commit()
    return jsonify({'id': bid.id})


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

