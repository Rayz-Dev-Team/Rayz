fetch('https://api.rayzbot.xyz/gilgang')
.then(response => response.json())
.then(data => {

    const container = document.getElementById('container');
    Object.keys(data.GG).forEach((key) => {
        const item = data.GG[key];
        const gridItem = document.createElement('div');
        gridItem.classList.add('grid-item');
        gridItem.innerHTML = `<img src="${item.avatar}" alt="${item.name}"><h3>${item.name}</h3>`;
        container.appendChild(gridItem);
    });
})