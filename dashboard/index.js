fetch('https://api.rayzbot.xyz/stats')
.then(response => response.json())
.then(data => {
    const outputDiv = document.getElementById('StatDisplay');
    const text = `${data.servers} servers, ${data.users} users`;
    outputDiv.innerText = text;
});