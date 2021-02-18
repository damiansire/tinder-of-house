from selenium import webdriver
import bdDao;
import math;
import time;

def get_address(data):
    part = data.split(",")
    partAmount = len(part)
    if(partAmount == 3):
        return {'address' : part[0],'city' : part[1], 'region' : part[2]}
    elif(partAmount > 3):
        return {'address' : " ".join(part[:len(part)-3]), 'city' : part[partAmount-2], 'region' : part[partAmount-1]}
    elif(partAmount < 3):
        for i in range(0,100):
            print("error:")
            print(data)
        return {'address' : 'FAIL','city' : 'FAIL', 'region' : data}

##Buscar alternativas a los try except, algo que contrele la excepion como el "?"" javascript
## Es esto: https://www.php2python.com/wiki/function.isset/
def get_house_data(html_element):
    img = html_element.find("img")['data-src']
    if(img == ""):
        img = html_element.find("img")['src']
    price = html_element.find(class_="price-tag-fraction").text
    size = html_element.find(class_="ui-search-card-attributes").text.replace("\n", " ")
    direction = get_address(html_element.find(class_="ui-search-item__location").text)
    address = direction["address"] 
    city = direction["city"] 
    region = direction["region"]
    title = html_element.find(class_="ui-search-item__title").text
    url = html_element.a['href']
    code = url.split("-")[1]
    return {'code' : code, 'imgurl' : img, 'price' : price, 'size' : size, 'address' : address, 'city' : city, 'region' : region, 'title' : title, 'url' : url}

def obtain_page_number(driver):
    #[u'1', u'049']
    data = driver.find_element_by_class_name("ui-search-search-result__quantity-results").text.split(" ")[0]
    #1049
    number = float("".join(data.split(".")))
    page_number = math.ceil(number / 48)
    return page_number

def get_page(page_number):
    return "https://listado.mercadolibre.com.uy/inmuebles/casas/_Desde_" + str(48*page_number+1) + "_PriceRange_8000UYU-14000UYU"

def div_houses_to_obj(all_house):
    my_house_obj = []
    for house in all_house:
        houseObj = get_house_data(house)
        print(houseObj)
        my_house_obj.append(houseObj)
    return my_house_obj

options = Options()

driver = webdriver.Firefox(executable_path = 'geckodriver', options=options)

endpoint = get_page(0)
driver.get(endpoint)

#Obtiene el numero de paginas
page_number = obtain_page_number(driver)

from bs4 import BeautifulSoup

for actual_page_number in range(0,page_number):
    driver.get(get_page(actual_page_number))
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    #Agarro todas las publicaciones disponibles
    all_houses = soup.find_all("li", class_="ui-search-layout__item")
    #Las convierte a obj interno
    all_houses_obj = div_houses_to_obj(all_houses)

for house_data in all_houses_obj:
    #Inserta en la base de datos
    bdDao.insert_all_house(all_houses_obj)
