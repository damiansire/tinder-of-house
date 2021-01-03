var req = new XMLHttpRequest();
req.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        let housesData = JSON.parse(req.responseText);
        housesData.forEach(houseData => addHouse(houseData))

    }
};

let allHouseEndpoint = "http://127.0.0.1:5550/api/v1/getAllHouse/"
req.open("GET", allHouseEndpoint, true);
req.send();

function addHouse(houseData) {
    let houseDataElement = renderData(houseData);
}

function renderData(houseData) {
    let dataHouseTr = document.createElement("tr");
    addNormalTd(dataHouseTr, houseData['code']);
    addNormalTd(dataHouseTr, houseData['address']);
    addNormalTd(dataHouseTr, houseData['city']);
    addNormalTd(dataHouseTr, houseData['region']);
    addTdImg(dataHouseTr, houseData['imgurl']);
    addNormalTd(dataHouseTr, houseData['price']);
    addNormalTd(dataHouseTr, houseData['size']);
    addNormalTd(dataHouseTr, houseData['title']);
    addNormalTd(dataHouseTr, houseData['url']);
    document.getElementsByClassName("houseTableBody")[0].appendChild(dataHouseTr);
}

function addTdImg(dataHouseTr, imgUrl, optionalClass) {
    let imgTdContainer = document.createElement("td")
    imgTdContainer.className += "tdImgContainer";
    let tdImgElement = document.createElement("IMG");
    tdImgElement.className += "imgTd";
    tdImgElement.className += optionalClass != undefined ? optionalClass : "";
    tdImgElement.src = imgUrl;
    imgTdContainer.append(tdImgElement);
    dataHouseTr.appendChild(imgTdContainer)
    return dataHouseTr;
}


function addNormalTd(dataHouseTr, dato) {
    let tdElement = document.createElement("td");
    let text = document.createTextNode(dato); // Create a text node
    tdElement.appendChild(text);
    dataHouseTr.appendChild(tdElement)
}