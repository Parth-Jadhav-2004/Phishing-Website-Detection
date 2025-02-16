document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("checkPhishing").addEventListener("click", function () {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            let url = tabs[0].url;
            
            fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url: url })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("result").innerText = "Prediction: " + data.prediction;
            })
            .catch(error => {
                console.error("Error fetching prediction:", error);
                document.getElementById("result").innerText = "Error fetching prediction. Check server.";
            });
        });
    });
});
