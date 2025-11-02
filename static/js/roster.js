// Roster Manager JavaScript

function addTeam() {
    const teamName = document.getElementById('team-name').value;
    const ownerName = document.getElementById('owner-name').value;
    
    if (!teamName || !ownerName) {
        alert('Please fill in both fields');
        return;
    }
    
    // Fetch API call will go here
    console.log('Adding team:', { teamName, ownerName });
    
    alert('Team added successfully!');
    
    // Clear form
    document.getElementById('team-name').value = '';
    document.getElementById('owner-name').value = '';
}

