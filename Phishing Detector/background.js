chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete") {
        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "url": tab.url })
        })
        .then(response => response.json())
        .then(data => {
            console.log(`Prediction for ${tab.url}: ${data.prediction}`);
        });
    }
});
