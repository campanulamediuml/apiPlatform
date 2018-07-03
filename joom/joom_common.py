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

def get_joom_access(store_id):
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
    get_refresh_token_list_query = 'SELECT seller_id,secret_key,aws_access_key_id,refresh_token FROM store WHERE website = "36"'
    cursor.execute(get_refresh_token_list_query)
    joom_refresh_token_list = cursor.fetchall()
    print(joom_refresh_token_list)
    conn.close()
    count = 0
    for token_line in joom_refresh_token_list:
        result = refresh_execute(token_line)
        count += result[0]
        if result[1] != 0:
            common_unit.write_log(result[1])
    return 0


def refresh_execute(token_line):
    try:
        url = 'https://api-merchant.joom.com/api/v2/oauth/refresh_token?client_id=%s&client_secret=%s&code=%s&grant_type=refresh_token&refresh_token=%s'%token_line
        # print(url)
        r = requests.post(url)
        result_data = json.loads(r.text)['data']
        # print(r.text)
        common_unit.write_log(r.text)
        cursor,conn = common_unit.database_connection()
        update_token_query = 'UPDATE store SET mws_token = "%s",refresh_token="%s" WHERE seller_id = "%s"'%(result_data["access_token"],result_data["refresh_token"],token_line[0])
        cursor.execute(update_token_query)
        conn.commit()
        cursor.close()
        return (0,0)
    except (Exception) as e:
        return (1,str(e))

def main_token_refresh_circle_joom():
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
        print("joom_token_refreshing")
        time.sleep(3600*24)

def test_token_joom(store_id):
    access_token = get_joom_access(store_id)
    url = 'https://api-merchant.joom.com/api/v2/auth_test?access_token=%s'%access_token
    # print(url)
    r = requests.get(url)
    return r.text

# test_token_joom("13")

# result = refresh_access_token()
# print(result)

