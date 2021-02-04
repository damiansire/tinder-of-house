import pymysql
import baseconect

def get_bd_connection():
    connection_bd = pymysql.connect(
        user = "housedata", 
        password=baseconect.password, 
        host = "den1.mysql5.gear.host", 
        database="housedata" )
    return connection_bd

def execute_query(query):
    connection_bd = get_bd_connection()
    cursor = connection_bd.cursor()
    sql_table_created = query
    cursor.execute(sql_table_created)
    connection_bd.commit()
    cursor.close()
    connection_bd.close()

def create_housedata_table():
    sql_table_created = """ CREATE TABLE HouseData ( code VARCHAR(60), address VARCHAR(200), city VARCHAR(200), region VARCHAR(200), price VARCHAR(200), size VARCHAR(200), title VARCHAR(200), url VARCHAR(300), imgurl VARCHAR(200)); """
    execute_query(sql_table_created)

### CUIDADO, NO HACER ESTO ASI EN PROYECTOS REALES, PORQUE TIENE PELIGRO DE INYECCION SQL
### AGUJERO DE SEGURIDAD, USAR PARAMETROS.
def get_insert_house_query(houseObj):
    sql_insert = "INSERT INTO HouseData ( code, address, city, region, price, size, title, url, imgurl) VALUES " 
    sql_insert += " ( '{}', '{}' , '{}' , '{}' , '{}' , '{}' , '{}', '{}', '{}' )".format(
        houseObj['code'] ,
        houseObj['address'] , 
        houseObj['city'],
        houseObj['region'] , 
        houseObj['price'] , 
        houseObj['size'] , 
        houseObj['title'] , 
        houseObj['url'],
        houseObj['imgurl'])
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

def db_house_to_house(row):
    return {'code' : row[0], 'address' : row[1], 'city' : row[2], 'region' : row[3], 'price' : row[4], 'size' : row[5], 'title' : row[6], 'url' : row[7], 'imgurl' : row[8]}

def get_all_house():
    connection_bd = get_bd_connection()
    cursor = connection_bd.cursor()
    select_all_house_query = "SELECT * FROM housedata.housedata;"
    cursor.execute(select_all_house_query)
    rows = cursor.fetchall()
    allHouseObj = []
    for row in rows:
        allHouseObj.append(db_house_to_house(row))
    return allHouseObj

def get_new_house():
    connection_bd = get_bd_connection()
    cursor = connection_bd.cursor()
    select_all_house_query = "SELECT * FROM housedata.housedata hd WHERE NOT EXISTS (SELECT NULL FROM housedata.dislikedata dld WHERE hd.code = dld.code) AND NOT EXISTS (SELECT NULL FROM housedata.likedata ld WHERE hd.code = ld.code) limit 2;"
    cursor.execute(select_all_house_query)
    rows = cursor.fetchall()
    all_house_obj = []
    for row in rows:
        all_house_obj.append(db_house_to_house(row))
    return all_house_obj

def get_action_query(obj_action):
    user_id = 0
    if(obj_action["like"]):
        print("entre a like")
        table_name = "likedata"
    else:
        table_name = "dislikedata"
        print("entre a dislike")
    query = "INSERT INTO {} ( code, userId) VALUES ({}, {})".format(table_name, obj_action["code"], user_id)
    return query
    
def save_action_to_house(action_arr):
    for obj_action in action_arr:
        query = get_action_query(obj_action)
        execute_query(query)

def get_initial_house():
    connection_bd = get_bd_connection()
    cursor = connection_bd.cursor()
    select_all_house_query = "SELECT * FROM housedata.housedata hd WHERE NOT EXISTS (SELECT NULL FROM housedata.dislikedata dld WHERE hd.code = dld.code) AND NOT EXISTS (SELECT NULL FROM housedata.likedata ld WHERE hd.code = ld.code) limit 20;"
    cursor.execute(select_all_house_query)
    rows = cursor.fetchall()
    all_house_obj = []
    for row in rows:
        all_house_obj.append(db_house_to_house(row))
    return all_house_obj