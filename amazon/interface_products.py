import sys
sys.path.append('../')
import requests
import time
import json
from urllib.parse import quote
from common_methods import common_unit



headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Products/2011-10-01'
api_version = ['Version=2011-10-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y


def get_sfs_id_by_asin(conn,cursor,asin):
    select_command = 'SELECT id from syn_fba_stocks where asin="%s"'%asin
    cursor.execute(select_command)
    return cursor.fetchall()[0][0]

def get_sfs_id_by_sku(conn,cursor,sku):
    select_command = 'SELECT id from syn_fba_stocks where sku="%s"'%sku
    cursor.execute(select_command)
    return cursor.fetchall()[0][0]

def get_sku_by_asin(conn,cursor,asin):
    select_command = 'SELECT sku from syn_fba_stocks where asin="%s"'%asin
    cursor.execute(select_command)
    return cursor.fetchall()[0][0]

def write_product_info_into_db(conn,cursor,content):
    content_keys = []
    content_values = []
    for key in content:
        content_keys.append(key)
        content_values.append(content[key])
    sql_query = tuple([','.join(content_keys)]+content_values)

    select_command = 'SELECT * from syn_listings where sfs_id="%s"'%content['sfs_id']
    cursor.execute(select_command)
    tmp = cursor.fetchall()
    if len(tmp) == 0:
        try:
            sql_insert = 'INSERT INTO syn_listings(%s) VALUES("%s","%s","%s","%s","%s","%s")'%sql_query
            cursor.execute(sql_insert)
            conn.commit()
            return 0
        except Exception as e:
            print(str(e))
            conn.commit()
            return 1
    else:
        return 1

def write_product_rank_into_db(conn,cursor,content):
    content_keys = []
    content_values = []
    for key in content:
        content_keys.append(key)
        content_values.append(content[key])
    sql_query = tuple([','.join(content_keys)]+content_values)

    string_write = ''
    for i in content_keys:
        string_write+='"%s",'

    string_write = string_write[:-1]

    search_string = 'SELECT * FROM listing_ranks WHERE listing_id = "%s"'%content['listing_id']
    cursor.execute(search_string)
    if len(cursor.fetchall()) == 0:
        try:
            sql_insert = 'INSERT INTO listing_ranks(%s) VALUES('+string_write+')'
            sql_insert = sql_insert%sql_query
            print(sql_insert)
            cursor.execute(sql_insert)
            conn.commit()
            return 0
        except Exception as e:
            print(str(e))
            conn.commit()
            return 1
    else:
        return 1




def save_result_into_db(json_content,execute_command):
    product_info = json.loads(json_content)
    cursor,conn = common_unit.database_connection()

    product_attribute = {}
    if 'asin' in execute_command:
        product_attribute['sfs_id'] = get_sfs_id_by_asin(conn,cursor,execute_command['asin'])
        product_attribute['sku'] = get_sku_by_asin(conn,cursor,execute_command['asin'])
    elif 'sku' in execute_command:
        product_attribute['sfs_id'] = get_sfs_id_by_sku(conn,cursor,execute_command['sku'])
        product_attribute['sku'] = execute_command['sku']

    attribute = json.dumps(product_info["GetMatchingProductResponse"]["GetMatchingProductResult"]["Product"])
    attribute = attribute.replace('"','\\"')
    product_attribute['attribute'] = attribute


    product_attribute['platform'] = product_info["GetMatchingProductResponse"]["GetMatchingProductResult"]["Product"]['Identifiers']['MarketplaceASIN']['MarketplaceId']
    product_attribute['marketpalce'] = product_info["GetMatchingProductResponse"]["GetMatchingProductResult"]["Product"]['Identifiers']['MarketplaceASIN']['MarketplaceId']

    product_attribute['store_id'] = execute_command['store_id']


    result = write_product_info_into_db(conn,cursor,product_attribute)

    ranking_attribute = {}
    ranking_attribute['listing_id'] = product_info["GetMatchingProductResponse"]["GetMatchingProductResult"]["Product"]['Identifiers']['MarketplaceASIN']['ASIN']
    ranking_attribute['sku'] = product_attribute['sku']
    ranking_attribute['marketplace_id'] = product_info["GetMatchingProductResponse"]["GetMatchingProductResult"]["Product"]['Identifiers']['MarketplaceASIN']['MarketplaceId']

    try:
        ranking_attribute_list = product_info["GetMatchingProductResponse"]["GetMatchingProductResult"]["Product"]['SalesRankings']
        ranking_attribute['cid_one'] = ranking_attribute_list['SalesRank']["ProductCategoryId"]
        ranking_attribute['rank_one'] = ranking_attribute_list['SalesRank']["Rank"]
    except:
        pass

    ranking_attribute['time'] = common_unit.get_time_stamp_now()

    result = write_product_rank_into_db(conn,cursor,ranking_attribute)

    conn.close()
    return result 






class interface_products:
    def __init__(self):
        pass     
#直接在亚马逊的class中添加接口方法
#通过连接请求参数，创建亚马逊请求网址
    def GetMatchingProduct(execute_command):
        params = ['Action=GetMatchingProduct']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict,execute_command)
        # 获取包含认证参数的字典
        if 'asin' in execute_command:
            asin_code = execute_command['asin']
        #计算asin列表
            asin_param_list = ['ASINList.ASIN.1='+asin_code]
            params = params + default_params + asin_param_list

        elif 'sku' in execute_command:
            sku_code = execute_command['sku']
        #计算asin列表
            sku_param_list = ['SKUList.SKU.1='+sku_code]
            params = params + default_params + sku_param_list
        # 如果不存在asin列表，则直接返回一个空列表扔掉
        # 上面计算的asin列表是该接口的特征参数
        # 添加请求中包含的asin
    
        params = sorted(params)
        # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序
        # 拼接请求身，需要按首字母排序
        # 关于api的分类和版本
        params = '&'.join(params)
        # print(params)
        # 对请求身进行分割
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string,user_access_dict['secret_key'])))
        # 计算字符串的加密签名
        url = connect_url(params,signature)

        # 拼接请求字符串
        r = requests.post(url,headers=headers)
        # 发起请求
        # print(common_unit.xmltojson(r.text))
        result = common_unit.xmltojson(r.text)
        print(result)

        result = save_result_into_db(result,execute_command)
        return str(result)


    def ListMatchingProducts(execute_command):
        params = ['Action=ListMatchingProducts']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict,execute_command)
        if 'keyword' in execute_command:
            params.append('Query='+ quote(execute_command['keyword']))
        else:
            params.append('Query=')
        # 如果不存在搜索关键词，则直接返回一个空的query
        # 获取特征参数query即搜索关键词
        params = params + default_params
        params = sorted(params)
        # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序
        # 拼接请求身，需要按首字母排序
        params = '&'.join(params)
        # print(params)
        # 对请求身进行分割
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string,user_access_dict['secret_key'])))
        # 计算字符串的加密签名
        url = connect_url(params,signature)
        # 拼接请求字符串
        r = requests.post(url,headers=headers)
        # 发起请求
        # print(common_unit.xmltojson(r.text))
        return common_unit.xmltojson(r.text)


    #根据卖的sku取得商品价格
    #sku是多个值  sku：'S123,S124,S125'
    def GetMyPriceForSKU(execute_command):
        params = ['Action=GetMyPriceForSKU'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
            # if 'sku' in execute_command:
            #     sku_list = execute_command['sku'].split(',')
            # print (sku_list)
            # sku_param_list = []
            # try:
            #     for i in sku_list:
            #         sku_param_list.append('SellerSKUList.SellerSKU.' + str(sku_list.index(i) + 1) + '=' + i)  # 计算sku列表
            # except:
            #     sku_param_list = ['SellerSKUList.SellerSKU.1=']  # 如果不存在sku列表，则直接返回一个空列表扔掉

        # skuList = []
        # sku_list = common_unit.get_skuList(execute_command['store_id'])
        # for i in sku_list:
        #     skuList.append('SellerSKUList.SellerSKU.' + str(sku_list.index(i) + 1) + '=' + i)  # 计算skuList列表

        if 'sku' in execute_command:
            params.append('SellerSKUList.SellerSKU.1=' + quote(execute_command['sku']))
        else:
            params.append('SellerSKUList.SellerSKU.1=') # 添加请求中包含的SellerSKU
        params = params + default_params   # 上面计算的sku列表是该接口的特征参数  添加请求中包含的sku
        params = sorted(params)       # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序 ,拼接请求身，需要按首字母排序,关于api的分类和版本
        params = '&'.join(params)  # 对请求身进行分割
        # print(params)
        params = params.replace('%2B',"%20")
        params = params.replace(' ',"%20")
        # print(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        # print(sig_string)
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        # print(signature)
        signature = signature.replace('/', '%2F')
        # print(signature)
        url = connect_url(params, signature)  # 拼接请求字符串
        # print(url)
        r = requests.post(url, headers=headers)  # 发起请求
        return common_unit.xmltojson(r.text)

    # 根据asin取得商品价格
    #  asin的值是多个  asin：'B071JJ3BJ3,B071JJ3BJ7,B071JJ3BJ8'
    def GetMyPriceForASIN(execute_command):
        params = ['Action=GetMyPriceForASIN'] + api_version + ['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)   # 获取包含认证参数的字典
        # if 'asin' in execute_command:
        #     asin_list = execute_command['asin'].split(',')
        # asin_param_list = []
        # try:
        #     for i in asin_list:
        #         asin_param_list.append('ASINList.ASIN.' + str(asin_list.index(i) + 1) + '=' + i)  # 计算asin列表
        # except:
        #     asin_param_list = ['ASINList.ASIN.1=']  # 如果不存在asin列表，则直接返回一个空列表扔掉
        #

        if 'asin' in execute_command:
            params.append('ASINList.ASIN.1=' + quote(execute_command['asin']))
        else:
            params.append('ASINList.ASIN.1=')

        params = params + default_params    # 上面计算的asin列表是该接口的特征参数  添加请求中包含的asin
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序 ,拼接请求身，需要按首字母排序,关于api的分类和版本
        params = '&'.join(params) # 对请求身进行分割
        params = params.replace('%2B', "%20")
        params = params.replace(' ', "%20")
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        signature = signature.replace('/', '%2F')
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)   # 发起请求
        return common_unit.xmltojson(r.text)


    #根据sku取得商品类别
    #sku值是单个
    def GetProductCategoriesForSKU(execute_command):
        params = ['Action=GetProductCategoriesForSKU'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        if 'sku' in execute_command:
            params.append('SellerSKU=' + quote(execute_command['sku']))
        else:
            params.append('SellerSKU=') # 添加请求中包含的SellerSKU
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        # print (params)
        params = '&'.join(params)  # 对请求身进行分割
        params = params.replace('%2B',"%20")
        # params = params.replace('+', "%2B")
        params = params.replace(' ', "%20")
        # print(params)
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        signature = signature.replace('/', '%2F')
        # print (signature)
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        return common_unit.xmltojson(r.text)

    #根据asin取得商品的类别
    #asin的值是单个
    def GetProductCategoriesForASIN(execute_command):
        params = ['Action=GetProductCategoriesForASIN'] + api_version+ ['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command) # 获取包含认证参数的字典
        if 'asin' in execute_command:
            params.append('ASIN=' + quote(execute_command['asin']))
        else:
            params.append('ASIN=')   # 添加请求中包含的ASIN
        params = params + default_params
        params = sorted(params) # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params) # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key']))) # 计算字符串的加密签名
        signature = signature.replace('/', '%2F')
        url = connect_url(params, signature)       # 拼接请求字符串
        r = requests.post(url, headers=headers)    # 发起请求
    
        return common_unit.xmltojson(r.text)

    #返回产品API部分的操作状态
    def GetServiceStatus(execute_command):
        params = ['Action=GetServiceStatus'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        return common_unit.xmltojson(r.text)


    def GetCompetitivePricingForSKU(execute_command):
        params = ['Action=GetCompetitivePricingForSKU']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict,execute_command)
        # 获取包含认证参数的字典
        if 'sku' in execute_command:
            sku_list = execute_command['sku'].split(',')
        sku_param_list = []
        #计算asin列表
        try:
            for i in sku_list:
                sku_param_list.append('SellerSKUList.SellerSKU.'+str(sku_list.index(i)+1)+'='+i)
        except:
            sku_param_list = ['SellerSKUList.SellerSKU.1=']
        # 如果不存在asin列表，则直接返回一个空列表扔掉
        # 上面计算的asin列表是该接口的特征参数
        # 添加请求中包含的asin
        params = params + default_params + sku_param_list
        params = sorted(params)       # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序    # 拼接请求身，需要按首字母排序   # 关于api的分类和版本
        params = '&'.join(params)     # 对请求身进行分割
        params = params.replace('%2B', "%20")
        # print(params)
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params   # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string,user_access_dict['secret_key'])))   # 计算字符串的加密签名
        signature = signature.replace('/', '%2F')
        url = connect_url(params,signature)
        r = requests.post(url,headers=headers)
        # print(common_unit.xmltojson(r.text))
        return common_unit.xmltojson(r.text)




    def GetCompetitivePricingForASIN(execute_command):
        params = ['Action=GetMatchingProduct']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict,execute_command)
        # 获取包含认证参数的字典
        if 'asin' in execute_command:
            asin_list = execute_command['asin'].split(',')
        asin_param_list = []
        #计算asin列表
        try:
            for i in asin_list:
                asin_param_list.append('ASINList.ASIN.'+str(asin_list.index(i)+1)+'='+i)
        except:
            asin_param_list = ['ASINList.ASIN.1=']
        # 如果不存在asin列表，则直接返回一个空列表扔掉
        # 上面计算的asin列表是该接口的特征参数
        # 添加请求中包含的asin
        params = params + default_params + asin_param_list
        params = sorted(params)
        # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序
        # 拼接请求身，需要按首字母排序
        # 关于api的分类和版本
        params = '&'.join(params)
        # print(params)
        # 对请求身进行分割
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string,user_access_dict['secret_key'])))
        # 计算字符串的加密签名
        url = connect_url(params,signature)
        # 拼接请求字符串
        r = requests.post(url,headers=headers)
        # 发起请求
        # print(common_unit.xmltojson(r.text))
        return common_unit.xmltojson(r.text)

    def GetLowestOfferListingsForSKU(execute_command):
        params = ['Action=GetLowestOfferListingsForSKU']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict,execute_command)
        params += ['ExcludeMe=false']
        # 获取包含认证参数的字典
        if 'sku' in execute_command:
            sku_list = execute_command['sku'].split(',')
        sku_param_list = []
        #计算asin列表
        try:
            for i in sku_list:
                sku_param_list.append('SellerSKUList.SellerSKU.'+str(sku_list.index(i)+1)+'='+i)
        except:
            sku_param_list = ['SellerSKUList.SellerSKU.1=']
        # 如果不存在asin列表，则直接返回一个空列表扔掉
        # 上面计算的asin列表是该接口的特征参数
        # 添加请求中包含的asin
        params = params + default_params + sku_param_list
        params = sorted(params)
        # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序
        # 拼接请求身，需要按首字母排序
        # 关于api的分类和版本
        params = '&'.join(params)
        # print(params)
        # 对请求身进行分割
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string,user_access_dict['secret_key'])))
        # 计算字符串的加密签名
        url = connect_url(params,signature)
        # 拼接请求字符串
        r = requests.post(url,headers=headers)
        # 发起请求
        # print(common_unit.xmltojson(r.text))
        return common_unit.xmltojson(r.text)

    def GetLowestOfferListingsForASIN(execute_command):
        params = ['Action=GetLowestOfferListingsForASIN']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict,execute_command)
        params += ['ExcludeMe=false']
        # 获取包含认证参数的字典
        if 'asin' in execute_command:
            asin_list = execute_command['asin'].split(',')
        asin_param_list = []
        #计算asin列表
        try:
            for i in asin_list:
                asin_param_list.append('ASINList.ASIN.'+str(asin_list.index(i)+1)+'='+i)
        except:
            asin_param_list = ['ASINList.ASIN.1=']
        # 如果不存在asin列表，则直接返回一个空列表扔掉
        # 上面计算的asin列表是该接口的特征参数
        # 添加请求中包含的asin
        params = params + default_params + asin_param_list
        params = sorted(params)
        # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序
        # 拼接请求身，需要按首字母排序
        # 关于api的分类和版本
        params = '&'.join(params)
        # print(params)
        # 对请求身进行分割
        sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
        # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string,user_access_dict['secret_key'])))
        # 计算字符串的加密签名
        url = connect_url(params,signature)
        # 拼接请求字符串
        r = requests.post(url,headers=headers)
        # 发起请求
        # print(common_unit.xmltojson(r.text))
        return common_unit.xmltojson(r.text)



