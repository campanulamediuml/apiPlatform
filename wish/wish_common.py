import sys
sys.path.append('../')
import time
from urllib.parse import quote
import hmac
import base64
import hashlib
import xmltodict
import json
import pymysql as mydatabase
from common_methods import db
from common_methods import common_unit
import requests

def get_wish_access(store_id):
    cursor,conn = common_unit.database_connection()
    search_access_id_query = 'SELECT mws_token FROM store WHERE id = "%s"'%store_id
    cursor.execute(search_access_id_query)
    token_list = cursor.fetchall()
    if len(token_list) == 0:
        access_token = "0"
    else:
        access_token = token_list[0][0]

    conn.close()
    return access_token

def refresh_access_token():
    cursor,conn = common_unit.database_connection()
    get_refresh_token_list_query = 'SELECT seller_id,secret_key,refresh_token FROM store WHERE website = "35"'
    cursor.execute(get_refresh_token_list_query)
    wish_refresh_token_list = cursor.fetchall()
    conn.close()
    count = 0
    for token_line in wish_refresh_token_list:
        result = refresh_execute(token_line)
        count += result[0]
        if result[1] != 0:
            common_unit.write_log(result[1])
    return 0


def refresh_execute(token_line):
    try:
        url = 'https://merchant.wish.com/api/v2/oauth/refresh_token?client_id=%s&client_secret=%s&refresh_token=%s&grant_type=refresh_token'%token_line
        r = requests.post(url)
        result_data = json.loads(r.text)['data']
        common_unit.write_log(r.text)
        cursor,conn = common_unit.database_connection()
        update_token_query = 'UPDATE store SET mws_token = "%s",refresh_token="%s" WHERE seller_id = "%s"'%(result_data["access_token"],result_data["refresh_token"],result_data["client_id"])
        cursor.execute(update_token_query)
        conn.commit()
        cursor.close()
        return (0,0)
    except (Exception) as e:
        return (1,str(e))

def main_token_refresh_circle_wish():
    while 1:
        time_struct = []
        time_stamp = time.localtime()
        for i in time_stamp[:6]:
            time_struct.append(str(i))
        # print(time_struct)
        for i in time_struct[1:]:
            if len(i) == 1:
                time_struct[time_struct.index(i)] = '0'+i
        if time_struct[2] == "01" or time_struct[2] == "16":
            refresh_access_token()
        print("wish_token_refreshing")
        time.sleep(3600*24)



