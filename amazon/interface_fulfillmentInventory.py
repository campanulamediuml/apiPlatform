import sys
sys.path.append('../')
import requests
from urllib.parse import quote
import time
from common_methods import common_unit
import json

headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/FulfillmentInventory/2010-10-01'
api_version = ['Version=2010-10-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y





#了解库存的可用性
class interface_fulfillmentInventory:


    def __init__(self):
        pass


    #返回关于卖方库存可用性的信息
    # def ListInventorySupply(execute_command):
    #     params = ['Action=ListInventorySupply'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
    #     user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
    #     params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
    #
    #     if 'start_time' in execute_command:
    #         # st = quote(execute_command['start_time'])
    #         st_timeArray = common_unit.timestamp_to_datetime(execute_command['start_time'])
    #         params.append('QueryStartDateTime=' + execute_command['start_time'].replace(':','%3A'))
    #     else:
    #         params.append('QueryStartDateTime=')     # 添加请求中包含的start_time
    #
    #     # if 'seller_sku' in execute_command:
    #     #     sku_list = execute_command['seller_sku'].split(',')
    #     # sellerskuList = []
    #     # try:
    #     #     for i in sku_list:
    #     #         sellerskuList.append('SellerSkus.member.' + str(sku_list.index(i) + 1) + '=' + i)  # 计算sellerskuList列表
    #     # except:
    #     #     sellerskuList = ['SellerSkus.member.1=']  # 如果不存在sellerskuList列表，则直接返回一个空列表扔掉
    #
    #     params = params + default_params # + sellerskuList
    #     params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
    #     params = '&'.join(params)  # 对请求身进行分割
    #     # print(params)
    #     sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
    #     signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))
    #     signature = signature.replace('/','%2F')
    #     # signature = signature.replace('=','%3D') # 计算字符串的加密签名
    #     url = connect_url(params, signature)  # 拼接请求字符串
    #     # print(url)
    #     r = requests.post(url, headers=headers)  # 发起请求
    #     result = common_unit.xmltojson(r.text)
    #     return result

    #返回关于卖方库存的可用性信息下一页  使用nexttoken参数
    def ListInventorySupplyByNextToken(execute_command):
        params = ['Action=ListInventorySupplyByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('NextToken=' + quote(execute_command['next_token']))  # 取上一个接口 NextToken的返回值
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #返回  实现库存API  的操作状态
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
        result = common_unit.xmltojson(r.text)
        return result

    # 返回关于卖方库存可用性的信息   非第一次做更新操作
    def ListInventorySupply(execute_command):
        params = ['Action=ListInventorySupply'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        # skuList = []
        # sku_list = common_unit.get_skuList(execute_command['store_id'])
        # for i in sku_list:
        #     skuList.append('SellerSkus.member.' + str(sku_list.index(i) + 1) + '=' + i)  # 计算skuList列表
        params.append('SellerSkus.member.1=' + quote(execute_command['sku']))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        params = params.replace('+',"%2B")
        # print(params)
        params = params.replace(' ',"%20")
        # print(params)
        #把你拉到和我同一水平，再用丰富的经验击败你
        #空格不能自动quote，需要手动转换
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))
        signature = signature.replace('/', '%2F')
        # print(signature)
        # signature = signature.replace('=','%3D') # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    # 同步库存产品列表的库存信息  第一次同步做插入操作
    def syn_inventory(execute_command):
        params = ['Action=ListInventorySupply'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        start_time = '1970-12-31T16:00:00'  # 设置一个久远的时间开始同步库存(第一次同步店铺商品列表的库存)
        start_time = start_time.replace(':', '%3A')
        params.append('QueryStartDateTime=' + start_time)

        params = params + default_params  #
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))
        signature = signature.replace('/', '%2F')
        # signature = signature.replace('=','%3D') # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        # result = r
        return result







