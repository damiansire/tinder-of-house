#Usar a gusto del consumidr
endpoint = "https://listado.mercadolibre.com.uy/inmuebles/casas/canelones/atlantida/_PriceRange_8000UYU-14000UYU"

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Firefox(executable_path = 'geckodriver', options=options)

driver.get(endpoint)

#Agarro todas las publicaciones disponibles
all_house = driver.find_elements_by_class_name("ui-search-layout__item")


def get_house_data(seleniumElement, city):
    img = seleniumElement.find_element_by_tag_name("img").get_attribute('src')
    price = seleniumElement.find_element_by_class_name("price-tag-fraction").text
    size = seleniumElement.find_element_by_class_name("ui-search-card-attributes").text.replace("\n", " ")
    address = seleniumElement.find_element_by_class_name("ui-search-item__location").text
    title = seleniumElement.find_element_by_class_name("ui-search-item__title").text
    url = seleniumElement.find_element_by_tag_name("a").get_attribute("href")
    return {'imgurl' : img, 'price' : price, 'size' : size, 'address' : address, 'title' : title, 'url' : url, 'city' : city}

def selenium_house_to_obj(all_house, city):
    my_house_obj = []
    for house in all_house:
        houseObj = get_house_data(house, city)
        print(houseObj)
        my_house_obj.append(houseObj)
    return my_house_obj

all_houses_obj = selenium_house_to_obj(all_house, "Atlantida")

def save_in_last_row_csv(text, csv_name):
    with open(csv_name,'a') as fd:
        fd.write(text + "\n")

def save_house_in_csv(houseObj):
    string = "{} , {} , {} , {} , {} , {}, {}".format(
        houseObj['imgurl'] ,
        houseObj['price'] , 
        houseObj['size'] , 
        houseObj['address'] , 
        houseObj['title'] , 
        houseObj['url'],
        houseObj['city'])
    save_in_last_row_csv(string,"houseData.csv")


import bdDao;

bdDao.insert_all_house(all_houses_obj)