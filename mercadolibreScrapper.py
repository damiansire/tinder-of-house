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


import pymysql

connection_bd = pymysql.connect(
    user = "housedata", 
    password="Qd3qY03!E_7o", 
    host = "den1.mysql5.gear.host", 
    database="housedata" )


cursor = connection_bd.cursor()

#sql_table_created = """ CREATE TABLE HouseData ( imgurl VARCHAR(200), price VARCHAR(200), size VARCHAR(200), address VARCHAR(200), title VARCHAR(200), url VARCHAR(200), city VARCHAR(200) ); """
#cursor.execute(sql_table_created)

def get_insert_house_query(houseObj):
    sql_insert = "INSERT INTO HouseData (imgurl , price , size , address , title , url , city) VALUES " 
    sql_insert += " ( '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}' )".format(
        houseObj['imgurl'] ,
        houseObj['price'] , 
        houseObj['size'] , 
        houseObj['address'] , 
        houseObj['title'] , 
        houseObj['url'],
        houseObj['city'])
    return sql_insert

for houseObj in all_houses_obj:
    sql_insert = get_insert_house_query(houseObj)
    print(sql_insert)
    cursor.execute(sql_insert)

connection_bd.commit()


cursor.close()
connection_bd.close()


