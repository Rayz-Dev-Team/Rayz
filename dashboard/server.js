function checkIDAPI() {
    var dataText = document.getElementById("Search").value;
    $.ajax({
        url: "https://api.rayzbot.xyz/server/"+dataText+"/info",
        type: "GET",
        dataType: "json",
        success: function(data) {
            const select = document.getElementById("notification");
            if (data.code === 200) {
                window.location.href = "https://rayzbot.xyz/dashboard/"+dataText
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
}