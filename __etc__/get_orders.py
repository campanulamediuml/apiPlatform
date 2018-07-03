import sys
import base64
sys.path.append('../')
import requests
from urllib.parse import quote
import time
from common_methods import common_unit
from amazon import interface_orders
from amazon import interface_sellers
import json

# execute_command = {'create_time':'2016-01-01','company_id':'0','store_id':'1'}
# result = interface_sellers.interface_sellers.test_access_code(execute_command)
# print(result)
# result = json.loads(result)
# access_status = result['GetServiceStatusResponse']['GetServiceStatusResult']['Status']
execute_command = {'company_id':'0','create_time':'','method':'ListOrderItems','store_id':'1','order_id':'112-0657446-6421027'}

def main(execute_command):
    # url = 'http://172.18.158.167:8888/amazon_execute/'
    url = 'http://localhost:9527/amazon_execute/order'
    content = execute_command
    time_1 = time.time()
    r=requests.post(url,content)
    time_2 = time.time()
    # print(json.dumps(content))
    return r.text


def order_id_to_order_no(order_id):
    cursor,conn = common_unit.database_connection()
    select_sql = 'SELECT * FROM db_erp.`order` WHERE order_no = "%s"'%order_id
    cursor.execute(select_sql)
    order_index = cursor.fetchall()[0][0] 
    conn.close()
    return order_index

def write_order_item_into_db(item_attribute):
    cursor,conn = common_unit.database_connection()
    key_list = []
    value_list = []
    for key in item_attribute:
        key_list.append(key)
        value_list.append('"'+str(item_attribute[key])+'"')
    key_database = ','.join(key_list)
    value_database = ','.join(value_list)

    sql_search_query = 'SELECT * FROM order_item WHERE order_id = "%s"'%str(item_attribute['order_id'])
    cursor.execute(sql_insert_query)
    if len(cursor.fetchall()) == 0:
        sql_insert_query = 'INSERT INTO order_item(%s) VALUES(%s)'%(key_database,value_database)
        cursor.execute(sql_insert_query)
        conn.commit()
        conn.close()
        return 0
    else:
        conn.close()
        return 1


    # print(sql_insert_query)

def write_order_item_into_database(execute_command,item_json):
    # item_json = main(execute_command)
    # print(item_json)
    item_dict = json.loads(item_json)

    order_attribute = item_dict['ListOrderItemsResponse']['ListOrderItemsResult']

    # print(order_attribute)
    item_attribute = order_attribute['OrderItems']['OrderItem']

    # print(item_attribute)
    item_dict_for_database = {}
    item_dict_for_database['sku'] = item_attribute['SellerSKU']
    item_dict_for_database['product_name'] = item_attribute['Title']

    item_dict_for_database['order_id'] = order_id_to_order_no(execute_command['order_id'])
    item_dict_for_database['quantity'] = item_attribute['ProductInfo']['NumberOfItems']
    item_dict_for_database['total_price'] = str(item_attribute['ItemPrice']['Amount'])

    item_dict_for_database['unit_price'] = str(float(item_dict_for_database['total_price'])/float(item_dict_for_database['quantity']))
    item_dict_for_database['company_id'] = str(execute_command['company_id'])

    # print(item_dict_for_database)
    return_code = write_order_item_into_db(item_dict_for_database)
    if return_code == 0:
        return_content = {'status_code':'0','message':'获取成功，订单的商品写入数据库了'}

    else:
        return_content = {'status_code':'1','message':'获取失败，数据库里已经有这条订单的信息了'}

    return json.dumps(return_content)


# def main_run(execute_command):
    
item_json = main(execute_command)
print(item_json)
    # write_order_item_into_database(item_json)

