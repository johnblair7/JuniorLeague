// Auction Calculator JavaScript

function searchPlayer() {
    const playerName = document.getElementById('player-search').value;
    
    if (!playerName) {
        alert('Please enter a player name');
        return;
    }
    
    // For now, just show a placeholder
    // You'll connect this to your API endpoint
    const recommendationDiv = document.getElementById('recommendation');
    const contentDiv = document.getElementById('recommendation-content');
    
    contentDiv.innerHTML = `
        <div class="bid-recommendation">
            Recommended Bid: $25
            <span class="confidence medium">Medium</span>
        </div>
        <div class="reasoning">
            <h3>Why this bid?</h3>
            <ul>
                <li>Based on 3 historical auctions</li>
                <li>Projected value: $28</li>
                <li>Suggested range: $22-$32</li>
            </ul>
        </div>
    `;
    
    recommendationDiv.style.display = 'block';
}

function submitLiveBid() {
    const playerId = document.getElementById('live-player-select').value;
    const bidAmount = document.getElementById('live-bid-amount').value;
    
    if (!bidAmount) {
        alert('Please enter a bid amount');
        return;
    }
    
    // Fetch API call will go here
    console.log('Submitting bid:', { playerId, bidAmount });
    
    // For now, just show confirmation
    alert(`Bid of $${bidAmount} recorded!`);
}

