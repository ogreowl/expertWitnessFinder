<script>
// Function to send the query
function sendQuery() {
    const query = document.getElementById("queryInput").value.trim();
    const loadingElement = document.getElementById("loading");
    const responseElement = document.getElementById("api-response");

    if (!query) {
        responseElement.innerHTML = "Please enter a query.";
        return;
    }

    // Show loading spinner
    loadingElement.style.display = "block";
    responseElement.innerHTML = "";

    const serviceUrl = '...';
    const payload = { query: query };

    fetch(serviceUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
        // Hide the loading spinner when the response is received
        loadingElement.style.display = "none";
        displayFormattedResponse(data, responseElement);
    })
    .catch((error) => {
        // Hide the loading spinner in case of error
        loadingElement.style.display = "none";
        console.error('Error:', error);
        responseElement.innerHTML = "Error occurred: " + error;
    });
}

// Event listener for the "Send Query" button
document.getElementById("sendQueryButton").addEventListener("click", function() {
    sendQuery();
});

// Event listener for pressing the "Enter" key inside the query input field
document.getElementById("queryInput").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendQuery();
    }
});

function displayFormattedResponse(data, element) {
    let formattedResponse = `<strong>Query:</strong> ${data.query} <span style="font-style: italic;"><br><br>Hint: Need better matches? Try rephrasing your search to get new results.</span><br><br>`;

    // Limit to the top 4 matches
    const topMatches = data.matches.slice(0, 8);

    topMatches.forEach((match, index) => {
        formattedResponse += `<div style="margin-bottom: 20px;">`;
        formattedResponse += `<strong>${index + 1}. ${match.first_name} ${match.last_name}</strong> (Similarity: ${(match.similarity_score * 100).toFixed(2)}%)<br>`;
        formattedResponse += `${match.summary}<br>`;
        
        // Add the link to full_filename
        formattedResponse += `<a href="${match.full_filename}" target="_blank">View Profile</a><br>`;
        
        formattedResponse += `<hr style="border: 1px solid #ccc; margin-top: 10px;">`;
        formattedResponse += `</div>`;
    });
    
    // Add the paragraph below the results
    
    element.innerHTML = formattedResponse;
}
// Add subtle hover and click animations for the send button
document.getElementById("sendQueryButton").style.transition = "all 0.3s ease";
document.getElementById("sendQueryButton").style.borderWidth = "1px";

document.getElementById("sendQueryButton").addEventListener("mouseover", function() {
    this.style.transform = "scale(1.05)";
    this.style.borderColor = "#007bff"; // Change border to blue when hovered
});

document.getElementById("sendQueryButton").addEventListener("mouseout", function() {
    this.style.transform = "scale(1)";
    this.style.borderColor = ""; // Revert to original border color
});

document.getElementById("sendQueryButton").addEventListener("mousedown", function() {
    this.style.transform = "scale(0.95)";
    this.style.borderColor = "#0056b3"; // Change border to slightly darker blue when clicked
});

document.getElementById("sendQueryButton").addEventListener("mouseup", function() {
    this.style.transform = "scale(1.05)";
    this.style.borderColor = "#007bff"; // Change back to blue when mouse button is released
});
</script>