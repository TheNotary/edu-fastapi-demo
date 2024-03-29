let endpoint = '/wizard_lm'

document.getElementById('jsonForm').addEventListener('submit', function(e) {
  e.preventDefault();

  var input_data = document.getElementById('input_data').value;

  fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      input_data: input_data
    })
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(data) {
    debugger;
    document.getElementById('result').innerText = data;
  })
  .catch(function(error) {
    console.error('Error:', error);
  });
});
