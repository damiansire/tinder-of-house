var req = new XMLHttpRequest();
req.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let housesData = JSON.parse(req.responseText);
        housesData.forEach(houseData => addHouse(houseData))

    }
};

var aux;

let allHouseEndpoint = "http://127.0.0.1:5400/api/v1/getAllHouse/"
req.open("GET", allHouseEndpoint, true);
req.send();

function addHouse(houseData) {
    let houseDataElement = renderData(houseData);
}

function renderData(houseData) {

    let dataHouseTr = document.createElement("tr");

    let houseDataKey = ['id', 'address', 'city', 'imgurl', 'price', 'size', 'title', 'url'];

    houseDataKey.forEach(key => {
        let tdElement = document.createElement("td");
        let text = document.createTextNode(houseData[key]); // Create a text node
        tdElement.appendChild(text);
        dataHouseTr.appendChild(tdElement)
    });

    document.getElementsByClassName("houseTableBody")[0].appendChild(dataHouseTr)
}

/*


*/