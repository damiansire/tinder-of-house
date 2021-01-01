import pymysql
import baseconect

def get_bd_connection():
    connection_bd = pymysql.connect(
        user = "housedata", 
        password=baseconect.password, 
        host = "den1.mysql5.gear.host", 
        database="housedata" )
    return connection_bd

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

def insert_all_house(all_houses_obj):
    connection_bd = get_bd_connection()
    cursor = connection_bd.cursor()
    for houseObj in all_houses_obj:
        sql_insert = get_insert_house_query(houseObj)
        print(sql_insert)
        cursor.execute(sql_insert)
    connection_bd.commit()
    cursor.close()
    connection_bd.close()

def dbHouse_to_house(row):
    return {'imgurl' : row[0], 'price' : row[1], 'size' : row[2], 'address' : row[3], 'title' : row[4] , 'url' : row[5], 'city' : row[6]}

def get_all_house():
    connection_bd = get_bd_connection()
    cursor = connection_bd.cursor()
    select_all_house_query = "SELECT * FROM housedata.housedata;"
    cursor.execute(select_all_house_query)
    rows = cursor.fetchall()
    allHouseObj = []
    for row in rows:
        allHouseObj.append(dbHouse_to_house(row))
    return allHouseObj

