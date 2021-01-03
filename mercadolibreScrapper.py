
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
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
def get_house_data(selenium_element):
    try:
        img = selenium_element.find_element_by_tag_name("img").get_attribute('src')
    except Exception:
        img = ""
    try:
        price = selenium_element.find_element_by_class_name("price-tag-fraction").text
    except Exception:
        price = ""  
    try:
        size = selenium_element.find_element_by_class_name("ui-search-card-attributes").text.replace("\n", " ")
    except Exception:
        size = ""   
    direction = get_address(selenium_element.find_element_by_class_name("ui-search-item__location").text)
    address = direction["address"] 
    city = direction["city"] 
    region = direction["region"]
    try:
        title = selenium_element.find_element_by_class_name("ui-search-item__title").text
    except Exception:
        title = ""  
    try:
        url = selenium_element.find_element_by_tag_name("a").get_attribute("href")
    except Exception:
        url = ""    
    try:
        code = url.split("-")[1]
    except Exception:
        code = ""   
    return {'code' : code, 'imgurl' : img, 'price' : price, 'size' : size, 'address' : address, 'city' : city, 'region' : region, 'title' : title, 'url' : url}

def selenium_houses_to_obj(all_house):
    my_house_obj = []
    for house in all_house:
        houseObj = get_house_data(house)
        print(houseObj)
        my_house_obj.append(houseObj)
    return my_house_obj

def obtain_page_number(driver):
    #[u'1', u'049']
    data = driver.find_element_by_class_name("ui-search-search-result__quantity-results").text.split(" ")[0]
    #1049
    number = float("".join(data.split(".")))
    page_number = math.ceil(number / 48)
    return page_number

def get_page(pageNumber):
    return "https://listado.mercadolibre.com.uy/inmuebles/casas/_Desde_" + str(48*pageNumber+1) + "_PriceRange_8000UYU-14000UYU"

options = Options()
#options.headless = True
#options.add_argument('--disable-gpu')
#options.add_argument('--no-sandbox')

driver = webdriver.Firefox(executable_path = 'geckodriver', options=options)

endpoint = get_page(0)
driver.get(endpoint)

#Obtiene el numero de paginas
pageNumber = obtain_page_number(driver)

for actualPageNumber in range(0,pageNumber):
    driver.get(get_page(actualPageNumber))
    time.sleep(5)
    #Agarro todas las publicaciones disponibles
    all_house = driver.find_elements_by_class_name("ui-search-layout__item")
    #Las convierte a obj interno
    all_houses_obj = selenium_houses_to_obj(all_house)
    #Inserta en la base de datos
    bdDao.insert_all_house(all_houses_obj)
