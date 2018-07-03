import sys
sys.path.append('../')
import requests
from urllib.parse import quote
import time
from common_methods import common_unit
from urllib.parse import unquote
import json
from multiprocessing.dummy import Pool

headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Orders/2013-09-01'
api_version = ['Version=2013-09-01']
#本类中的公用方法
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y


def get_attributes(response,cursor,conn):
    # print(response)
    try:
        purchase_time = response['PurchaseDate'].replace('T',' ').replace('Z','')
    except:
        purchase_time = '0'

    try:
        order_type = response['OrderType']
    except:
        order_type = '0'

    try:
        buyer_email = response['BuyerEmail']
    except:
        buyer_email = '0'

    try:
        last_update_time = response['LastUpdateDate'].replace('T',' ').replace('Z','')
    except:
        last_update_time = '0'

    try:
        buyer_name = response['BuyerName']
    except:
        buyer_name = '0'

    try:
        order_price = response['OrderTotal']['Amount']
    except:
        order_price = '0'

    try:
        currency_code = response['OrderTotal']['CurrencyCode']
    except:
        currency_code = '0'

    try:
        address = response['ShippingAddress']
    except:
        address = '0'


    try:
        address_city = address['City']
    except:
        address_city = '0'

    try:
        address_postcode = address['PostalCode']
    except:
        address_postcode = '0'
    
    try:
        province = address['StateOrRegion']
    except:
        province = '0'
    
    try:
        country = address['CountryCode']
    except:
        country = '0'
    
    try:
        address_line = address['AddressLine1']
    except:
        address_line = '0'
    
    try:
        order_id = response['SellerOrderId']
    except:
        order_id = '0'
    

    try:
        payment = response['PaymentMethodDetails']['PaymentMethodDetail']
    except:
        payment = '0'
    
    try:
        order_status = response['OrderStatus']
    except:
        order_status = '0'
    
    try:
        service_level = response['ShipServiceLevel']
    except:
        service_level = '0'

    try:
        shipment = response['FulfillmentChannel']
    except:
        shipment = '0'

    try:
        sales_channel = response['SalesChannel']
    except:
        sales_channel = '0'

    try:
        PostalCode = address['PostalCode']
    except:
        PostalCode = '0'


    try:
        payment = response['PaymentMethod']
    except:
        payment = '0'

    try:
        PaymentMethodDetail = response['PaymentMethodDetails']['PaymentMethodDetail']
    except:
        PaymentMethodDetail = '0'

    try:
        market_place_id = response['MarketplaceId']
    except:
        market_place_id = '0'

    try:
        buyer_email = response['BuyerEmail']
    except:
        buyer_email = '0'

    try:
        latest_ship_date = response['LatestShipDate']
    except:
        latest_ship_date = '0'


    try:
        is_prime = response['IsPrime']
    except:
        is_prime = '0'

    try:
        is_premium_order = response['IsPremiumOrder']
    except:
        is_premium_order = '0'






    line_insert_time_stamp = common_unit.get_sql_time_stamp()

    line = {}
    line['order_id'] = order_id
    line['buyer_country'] = country
    line['state_or_province'] = province
    line['city'] = address_city
    line['address_line1'] = address_line
    line['order_type'] = order_type
    line['purch_date'] = purchase_time
    line['last_update_date'] = last_update_time
    line['amount'] = order_price
    line['buyer_name'] = buyer_name
    line['ful_channel'] = shipment
    line['time'] = line_insert_time_stamp
    line['order_status'] = order_status
    line['sales_channel'] = sales_channel
    line['postal_code'] = PostalCode
    line['country_code'] = country
    line['currency_code'] = currency_code
    line['pay_method'] =  payment
    line['method_detail'] = PaymentMethodDetail
    line['market_place_id'] = market_place_id
    line['buyer_email'] = buyer_email
    line['latest_ship_date'] = latest_ship_date
    line['is_prime'] = is_prime
    line['is_premium_order'] = is_premium_order
    # line = [order_id,purchase_time,buyer_email,last_update_time,buyer_name,order_price,currency_code,address_city,address_postcode,province,country,address_line,payment,order_status]
    # print(line)
    print(line)
    # line = refresh_country_province_and_city_index_table_in_database(line,cursor,conn)
    # 把省市国家转化为编码
    # line = get_order_status_and_order_type(line,cursor,conn)
    # 把订单类型状态转化为编码
    return line


def get_order(execute_command,result):
    # print(result)
    result = json.loads(result)
    response = result['GetOrderResponse']['GetOrderResult']['Orders']['Order']
    if response == {}:
        return -1
    attribute_line = get_attributes(response,cursor,conn)
    #添加公司和店铺的id
    attribute_line['store_id'] = execute_command['store_id']
    attribute_line['company_id'] = execute_command['company_id']
    cursor,conn = common_unit.database_connection()
    status = write_into_database(attribute_line,cursor,conn)
    conn.close()
    return status
    # 获取订单，并将其写入数据库

def list_orders(execute_command,result):
    # print(result)
    result = json.loads(result)
    try:
        response = result['ListOrdersResponse']['ListOrdersResult']['Orders']['Order']
        status = 0
        # print(response)
    except:
        response = []
    if len(response) == 0:
        return -1
    order_no_list = []
    cursor,conn = common_unit.database_connection()
    for i in response:
        # print(i)
        result = get_attributes(i,cursor,conn)
        print(i)
        #添加公司和店铺的id
        result['store_id'] = execute_command['store_id']

        
        result['seller_id'] = get_company_id_by_store_id(result['store_id'],cursor,conn)


        status += write_into_database(result,cursor,conn)
        # order_no_list.append(result['order_id'])

    conn.close()
    return status,order_no_list
    # 获取订单列表，并将其写入数据库

def get_company_id_by_store_id(store_id,cursor,conn):
    search_query = "SELECT seller_id FROM store WHERE id = '%s'"%store_id
    cursor.execute(search_query)
    return cursor.fetchall()[0][0]

def write_into_database(content,cursor,conn):
    order_id = content['order_id']
    print(content)
    sql_sententce = 'SELECT * FROM syn_order WHERE order_id = "%s"'%order_id
    # print(sql_sententce)
    cursor.execute(sql_sententce)
    order_lines = cursor.fetchall()
    # 链接订单表
    # print(len(content_keys))
    # 把key和value拼接成一个tuple
    # print(sql_query)
    # print(sql_query)


    if len(order_lines) == 0:
        # print(len(order_lines))
        content_keys = []
    # 订单表key做成列表
        content_values = []
    # 对应value做成列表
        for key in content:
            content_keys.append(key)
            content_values.append(content[key])
        sql_query = tuple([','.join(content_keys)]+content_values)
        try:
            sql_insert = 'INSERT INTO syn_order(%s) VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'%sql_query
            cursor.execute(sql_insert)
            conn.commit()
            return 0
        except Exception as e:
            print(str(e))

            return 1

    else:
        content_keys = []
    # 订单表key做成列表
        content_values = []
    # 对应value做成列表
        content.pop('order_id')
        # for key in content:
        #     content_keys.append(key)
        #     content_values.append(content[key])
        # sql_query = tuple([','.join(content_keys)]+content_values)
        try:
            update_query_head = 'UPDATE syn_order SET '
            for key in content:
                update_query_head = update_query_head + key + '='+'"'+content[key]+'",'
            update_query = update_query_head[:-1] + 'WHERE order_id = "'+order_id+'"'
            cursor.execute(update_query)
            conn.commit()
            print('update successful')
            return 0
        except Exception as e:
            print(str(e))

            return 1







def refresh_country_province_and_city_index_table_in_database(content,cursor,conn):
    country_name_for_database_key = common_unit.anti_sql_inject_attack(content['country_id'])
    province_name_for_database_key = common_unit.anti_sql_inject_attack(content['province_id'])
    city_name_for_database_key = common_unit.anti_sql_inject_attack(content['city_id'])
    sql_sententce_for_search_country = 'SELECT * FROM country WHERE name = "%s"'%country_name_for_database_key
    cursor.execute(sql_sententce_for_search_country)
    country_line = cursor.fetchall()
    # 搜索数据库中国家对应的国家代码

    if len(country_line) == 0:
        cursor.execute('INSERT INTO country(name) VALUES(%s)',(country_name_for_database_key,))
        conn.commit()
        cursor.execute(sql_sententce_for_search_country)
        country_line = cursor.fetchall()
    # 如果不存在这个国家，就插入一条新的

    country_index_code = str(country_line[0][0])
    # 提取国家代码
    
    sql_sententce_for_search_province = 'SELECT * FROM province WHERE name = "%s" AND country_id = "%s"'%(province_name_for_database_key,country_index_code)
    cursor.execute(sql_sententce_for_search_province)
    province_line = cursor.fetchall()
    #用国家代码查询这个国家内的省份的代码

    if len(province_line) == 0:
        cursor.execute('INSERT INTO province(name,country_id) VALUES(%s,%s)',(province_name_for_database_key,country_index_code))
        conn.commit()
        cursor.execute(sql_sententce_for_search_province)
        province_line = cursor.fetchall()
    # 如果不存在就插入新的，然后重新获取

    province_index_code = str(province_line[0][0])
    #提取省份代码

    sql_sententce_for_search_city = 'SELECT * FROM city WHERE name = "%s" AND province_id = "%s"'%(city_name_for_database_key,province_index_code)
    cursor.execute(sql_sententce_for_search_city)
    city_line = cursor.fetchall()
    if len(city_line) == 0:
        cursor.execute('INSERT INTO city(name,province_id) VALUES(%s,%s)',(city_name_for_database_key,province_index_code))
        conn.commit()
        cursor.execute(sql_sententce_for_search_city)
        city_line = cursor.fetchall()

    city_index_code = str(city_line[0][0])
    # 提取城市代码
    content['country_id'] = country_index_code
    content['province_id'] = province_index_code
    content['city_id'] = city_index_code

    return content

def get_order_status_and_order_type(content,cursor,conn):
    order_type = content['order_type']
    order_status = content['status']

    sql_get_order_type = 'SELECT * FROM dictionary WHERE dict_value = "%s" AND remark = "%s" '%(order_type,'Amazon_order_type')
    cursor.execute(sql_get_order_type)
    order_type_line = cursor.fetchall()
    if len(order_type_line) == 0:
        cursor.execute('INSERT INTO dictionary(dict_value,remark) VALUES(%s,%s)',(order_type,'Amazon_order_type'))
        conn.commit()
        cursor.execute(sql_get_order_type)
        order_type_line = cursor.fetchall()
    # 更新字典中订单类别

    order_type_id = str(order_type_line[0][0])

    sql_get_order_status = 'SELECT * FROM dictionary WHERE dict_value = "%s" AND remark = "%s" '%(order_status,'Amazon_order_status')
    cursor.execute(sql_get_order_status)
    order_status_line = cursor.fetchall()
    if len(order_status_line) == 0:
        cursor.execute('INSERT INTO dictionary(dict_value,remark) VALUES(%s,%s)',(order_status,'Amazon_order_status'))
        conn.commit()
        cursor.execute(sql_get_order_status)
        order_status_line = cursor.fetchall()
    # 更新字典中的订单的状态

    order_status_id = str(order_status_line[0][0])

    content['order_type'] = order_type_id 
    content['status'] = order_status_id
    # 在订单字典中添加类别和状态
    return content

def list_order_by_store_id(execute_command):
    params = ['Action=ListOrders']+api_version+['Timestamp='+common_unit.get_time_stamp()]
    user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
    # 获取认证参数
    # 把认证参数添加进请求头
    params += common_unit.make_access_param(user_access_dict,execute_command)

    params[-1] = 'MarketplaceId.Id.1='+params[-1].split('=')[1]

    if execute_command['create_time'] != '':
        params += ['CreatedAfter='+quote(execute_command['create_time']+'T00:00:00')]
    else:
        params += ['CreatedAfter='+quote('1970-01-01T00:00:00')]
    params = params + default_params
    # print(params)
    params = sorted(params) 
    # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
    params = '&'.join(params) 
    # 对请求身进行分割
    # print(params)
    sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params # 连接签名字符串
    signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key']))) # 计算字符串的加密签名

    url = connect_url(params, signature)

    # 拼接请求字符串
    # print(url)
    r = requests.post(url, headers=headers)    # 发起请求
    content = common_unit.xmltojson(r.text)

    # print(content)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

    status,order_no_list = list_orders(execute_command,content)

    if status == 0:
        result = {'status_code':0,'message':'同步成功了所有订单，好哥哥你真棒！'}
    elif status == -1:
        result = {'status_code':-1,'message':'没有订单啊，你会不会查询啊？'}
    else:
        result = {'status_code':1,'message':'好像有'+str(status)+'条订单数据库里已经有了，要不要试试直接查查数据库？'}

    return result,order_no_list

    # return json.dumps(result)
    # print(common_unit.xmltojson(r.text))

def order_id_to_order_no(order_id):
    cursor,conn = common_unit.database_connection()
    select_sql = 'SELECT * FROM syn_order WHERE order_no = "%s"'%order_id
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

    # print(key_database)
    # print(value_database)

    sql_search_query = 'SELECT * FROM syn_order_item WHERE order_item_id = "%s"'%str(item_attribute['order_item_id'])
    cursor.execute(sql_search_query)
    if len(cursor.fetchall()) == 0:
        sql_insert_query = 'INSERT INTO syn_order_item(%s) VALUES(%s)'%(key_database,value_database)
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
    if 'Error' in item_json:
        return_code = 1
    else:
        item_dict = json.loads(item_json)
        try:
            # print(item_dict)


            order_attribute = item_dict['ListOrderItemsResponse']['ListOrderItemsResult']
            # print(order_attribute)
            item_attribute = order_attribute['OrderItems']['OrderItem']
            # print(item_attribute)

            item_dict_for_database = {}
            item_dict_for_database['order_id'] = execute_command['order_id']
            item_dict_for_database['asin'] = item_attribute['ASIN']
            item_dict_for_database['order_item_id'] = item_attribute['OrderItemId']
            item_dict_for_database['seller_sku'] = item_attribute['SellerSKU']
            item_dict_for_database['title'] = item_attribute['Title']
            item_dict_for_database['quant_order'] = item_attribute['QuantityOrdered']
            item_dict_for_database['quant_ship'] = item_attribute['QuantityShipped']
            item_dict_for_database['item_num'] = item_attribute['ProductInfo']['NumberOfItems']
            item_dict_for_database['currency_code'] = item_attribute['ItemPrice']['CurrencyCode']
            item_dict_for_database['im_price_amount'] = str(item_attribute['ItemPrice']['Amount'])
            item_dict_for_database['is_gift'] = item_attribute["IsGift"]






            # item_dict_for_database['sku'] = item_attribute['SellerSKU']
            # item_dict_for_database['product_name'] = item_attribute['Title']
            # item_dict_for_database['quantity'] = item_attribute['ProductInfo']['NumberOfItems']
            # item_dict_for_database['total_price'] = str(item_attribute['ItemPrice']['Amount'])
            # item_dict_for_database['unit_price'] = str(float(item_dict_for_database['total_price'])/float(item_dict_for_database['quantity']))
            # # item_dict_for_database['company_id'] = str(execute_command['company_id'])
            # # print(item_dict_for_database['company_id'])
            # item_dict_for_database['order_item_id'] = item_attribute['OrderItemId']
            # print(item_attribute['OrderItemId'])

        # print(item_dict_for_database)
            print('writing')
            print(item_dict_for_database)
            try:
                return_code = write_order_item_into_db(item_dict_for_database)
            except (Exception) as e:
                print(e)
            # print('write_finish')
        except (Exception) as e:
            print(e)
            # print(e)
            return_code = 1
    if return_code == 0:
        return_content = {'status_code':'0','message':'获取成功，订单的商品写入数据库了'}

    else:
        return_content = {'status_code':'1','message':'获取失败，数据库里已经有这条订单的信息了'}

    return json.dumps(return_content)

def list_order_items(executable):
    execute_command = executable[0]
    result_list = []
    for i in executable[1]:
        execute_command['order_id'] = i
        # print(execute_command)
        result = interface_orders.ListOrderItems(execute_command)
        result_list.append(result)
    
    result_list = list(set(result_list))[0]
    return result


class interface_orders:
    def __init__(self):
        pass     
#直接在亚马逊的class中添加接口方法
#通过连接请求参数，创建亚马逊请求网址

    def ListOrders(execute_command):
        cursor,conn = common_unit.database_connection()
        if execute_command['create_time'] == '':
            execute_command['create_time'] == '1970-01-01'
        if execute_command['store_id'] != '':
            result = list_order_by_store_id(execute_command)
            return json.dumps(result)


        elif 'company_id' in execute_command:
            company_id_in_execute_command = common_unit.anti_sql_inject_attack(str(execute_command['company_id']))
            # 清洗一下数据，把公司的id拿出来
            search_query = 'SELECT id FROM store WHERE company_id = "%s"'%company_id_in_execute_command
            # 拼接数据条
            cursor.execute(search_query)
            # 执行查询
            store_list = cursor.fetchall()
            result = []
            # 获取该公司的全部店铺的id
            order_no_list_all = []
            print (len(store_list))
            for i in store_list:
                execute_command['store_id']=i[0]
                return_json,order_no_list = list_order_by_store_id(execute_command)
                order_no_list = list(set(order_no_list))
                # executable = (execute_command,order_no_list)
                # result = list_order_items(executable)
                # result.append(return_json)
            # 拿店铺id去查询，最后把数据插入到一个列表中
            # print(order_no_list_all)
            conn.close()
        # 关闭数据库连接，防止连接数过高导致溢出，然后把列表转化为json数组
        else:
            result = {'status_code':'-9527','message':'傻逼啊……你会不会请求啊……params都弄错了'}

        result = return_json
        return result
 

    def ListOrderItems(execute_command):
        params = ['Action=ListOrderItems']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
        params += [str('AmazonOrderId='+execute_command['order_id'])]
        # 添加订单编号
        # params = params + default_params
        params = sorted(params) 
        # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params) 
        # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params 
        # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key']))) # 计算字符串的加密签名
        url = connect_url(params, signature)      
        # 拼接请求字符串
        r = requests.post(url, headers=headers)    
        # 发起请求

        attribute_content = common_unit.xmltojson(r.text)
        print(attribute_content)
        result = write_order_item_into_database(execute_command,attribute_content)
        return result



    # def GetServiceStatus(execute_command):
    #     params = ['Action=GetServiceStatus']+api_version+['Timestamp='+common_unit.get_time_stamp()]
    #     user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
    #     params += common_unit.make_access_param(user_access_dict,execute_command)
    #     params = params + default_params
    #     params = sorted(params)
    #     # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序
    #     # 拼接请求身，需要按首字母排序
    #     # 关于api的分类和版本
    #     params = '&'.join(params)
    #     # print(params)
    #     # 对请求身进行分割
    #     sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
    #     # 连接签名字符串
    #     signature = quote(str(common_unit.cal_signature(sig_string,user_access_dict['secret_key'])))
    #     # 计算字符串的加密签名
    #     url = connect_url(params,signature)
    #     print(params)
    #     # 拼接请求字符串
    #     r = requests.post(url,headers=headers)
    #     # 发起请求
    #     # print(common_unit.xmltojson(r.text))
    #     result_json_string = common_unit.xmltojson(r.text)
    #     print(result_json_string)
    #     result = json.loads(result_json_string)
    #     access_status = result['GetServiceStatusResponse']['GetServiceStatusResult']['Status']
    #     if access_status == 'GREEN':
    #         result = {'status_code':'0','message':'你真厉害，好哥哥！验证成功啦！'} 
    #     else:
    #         result = {'status_code':'-1','message':'你眼瞎啊？抄access_id都抄错'} 
    #     return json.dumps(result)

    # def test_access_account(execute_command):
    #     params = ['Action=GetOrder']+api_version+['Timestamp='+common_unit.get_time_stamp()]
    #     user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
    #     params += common_unit.make_access_param(user_access_dict,execute_command)
    #     params = params + default_params
    #     params = sorted(params)
    #     # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序
    #     # 拼接请求身，需要按首字母排序
    #     # 关于api的分类和版本
    #     params = '&'.join(params)
    #     # print(params)
    #     # 对请求身进行分割
    #     sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
    #     # 连接签名字符串
    #     signature = quote(str(common_unit.cal_signature(sig_string,user_access_dict['secret_key'])))
    #     # 计算字符串的加密签名
    #     url = connect_url(params,signature)
    #     print(params)
    #     # 拼接请求字符串
    #     r = requests.post(url,headers=headers)
    #     # 发起请求
    #     # print(common_unit.xmltojson(r.text))
    #     result_json_string = common_unit.xmltojson(r.text)
    #     print(result_json_string)
    #     result = json.loads(result_json_string)
    #     if "ErrorResponse" not in result:
    #         result = {'status_code':'0','message':'你真厉害，好哥哥！验证成功啦！'} 
    #     else:
    #         result = {'status_code':'-1','message':'你眼瞎啊？抄access_id都抄错'} 
    #     return json.dumps(result)















