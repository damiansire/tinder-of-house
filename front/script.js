let code1 = "1"
let code2 = "2"
let allHousesManager;


class housesManager {
    constructor(houseArray) {
        this.houseArray = houseArray
    }

    takeTwoHouses() {
        return this.houseArray.splice(0, 2)
    }

    addTwoHouse(housesArr) {
        this.houseArray = this.houseArray.concat(housesArr)
    }
}

const endpointBase = "http://127.0.0.1:5550/api/v1/houses"


function getInitialHouse() {
    fetch(endpointBase + "/initial")
        .then(response => response.json())
        .then(json => {
            allHousesManager = new housesManager(json);
            renderNewSelection()
        })
}

getInitialHouse()

function renderNewSelection() {
    let twoHouse = allHousesManager.takeTwoHouses()
    code1 = twoHouse[0]["code"];
    code2 = twoHouse[1]["code"];
    return renderHouse(twoHouse)
}

function renderHouse(twoHouses) {
    let housesDiv = document.getElementsByClassName("house");
    renderHouseData(twoHouses[0], housesDiv[0])
    renderHouseData(twoHouses[1], housesDiv[1])
}

function renderHouseData(houseData, houseDiv) {
    console.log(houseData)
    console.log(houseData["title"])
    houseDiv.querySelector(".title").textContent = houseData["title"]
    houseDiv.querySelector(".price").textContent = houseData["price"]
    houseDiv.querySelector(".size").textContent = houseData["size"]
    houseDiv.querySelector(".address").textContent = houseData["address"] + houseData["city"] + houseData["region"]
    rederPhotos(houseData, houseDiv)
}

function rederPhotos(houseData, houseDiv) {
    //let allPhotos = houseData["allImg"]
    let allPhotos = [houseData["imgurl"], houseData["imgurl"]]
    const photoDiv = houseDiv.querySelector(".photos");
    photoDiv.innerHTML = ""
    for (let url of allPhotos) {
        let html = `        
        <div class="col-sm-6 item">
                            <a href="${url}" data-lightbox="photos"><img class="img-fluid" src="${url}"></a>
                        </div>
        `
        photoDiv.insertAdjacentHTML('beforeend', html)
    }
}

const buttonGroupDiv = document.getElementsByClassName("button-bar-container")[0];

buttonGroupDiv.addEventListener("click", (event) => {

    let selection = event.target.getAttribute("data-action")

    let objSelection = [
        { "code": code1, "like": selection == "left" || selection == "both" },
        { "code": code2, "like": selection == "right" || selection == "both" }
    ]

    sendSelection(objSelection)
})

function sendSelection(objSelection) {
    fetch(endpointBase + "/selection", {
            method: 'POST',
            body: JSON.stringify(objSelection),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(
            house => {
                allHousesManager.addTwoHouse(house);
                renderNewSelection();
            }
        )

}