document.getElementById('jsonForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var input_data = document.getElementById('input_data').value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/ml', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var json = JSON.parse(xhr.responseText);
            var resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<h2>Result</h2><p>Input: ' + json.input_data + '</p><p>Sentiment: ' + json.label + ', Score: ' + json.score + '</p>';
            resultDiv.style.display = 'block';
        } else {
            console.error(xhr);
        }
    }
    xhr.send(JSON.stringify({
        input_data: input_data
    }));
});