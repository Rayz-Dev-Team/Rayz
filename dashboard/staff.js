var url = window.location.href;
var urlParts = url.split('/');
var serverId = urlParts[urlParts.length - 1];


$.ajax({
    url: "https://api.rayzbot.xyz/server/"+ serverId +"/info",
    type: "GET",
    dataType: "json",
    success: function(data) {
        const select = document.getElementById("notification");
        if (data.code === 200) {
            const container = document.getElementById('container');
            Object.keys(data.server_staff).forEach((key) => {
                const item = data.server_staff[key];
                const gridItem = document.createElement('div');
                gridItem.classList.add('grid-item');
                const button = document.createElement('button');
                button.classList.add('staff-button');
                button.addEventListener('click', () => {
                    window.location.href = "https://rayzbot.xyz/auth/"+item.id; // Replace this with the actual URL of the staff member's profile
                });
                const image = document.createElement('img');
                image.src = item.avatar;
                image.alt = item.name;
                button.appendChild(image);
                const name = document.createElement('h3');
                name.textContent = item.name;
                button.appendChild(name);
                gridItem.appendChild(button);
                container.appendChild(gridItem);
            });
        } 
        if (data.code === 404) {
            const displayContent = document.createElement('option');
            displayContent.classList.add('StatusError');
            const optionText = document.createTextNode(data.message);
            const paragraphElement = document.createElement('p');
            paragraphElement.classList.add("Search")
            paragraphElement.appendChild(optionText);
            displayContent.appendChild(paragraphElement);
            select.appendChild(displayContent);
            setTimeout(function() {
                select.removeChild(displayContent);
            }, 4000);
        } else {
        }
    }
});