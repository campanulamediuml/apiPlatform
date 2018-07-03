import sys
sys.path.append('../')
import requests
from urllib.parse import quote
import time
from common_methods import common_unit


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/FulfillmentOutboundShipment/2010-10-01'
api_version = ['Version=2010-10-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y


#配送出库
class interface_fulfillmentOutboundShipment:

    def __init__(self):
        pass
    #根据您指定的送货条件返回配送订单预览列表
    #参数  Address   Items
    def GetFulfillmentPreview(execute_command):
        params = ['Action=GetFulfillmentPreview'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典

        if 'address' in execute_command:
            address_list = execute_command['address'].split(',')
        params.append('Address.Name=' + str(address_list[0]))
        params.append('Address.Line1=' + str(address_list[1]))
        params.append('Address.Line2=' + str(address_list[2]))
        params.append('Address.Line3=' + str(address_list[3]))
        params.append('Address.StateOrProvinceCode=' + str(address_list[4]))
        params.append('Address.PostalCode=' + str(address_list[5]))
        params.append('Address.CountryCode=' + str(address_list[6]))

        if 'items' in execute_command:
            item_list = execute_command['items'].split(',')
        params.append('Items.member.1.Quantity=' + str(item_list[0]))
        params.append('Items.member.1.SellerFulfillmentOrderItemId=' + str(item_list[1]))
        params.append('Items.member.1.SellerSKU=' + str(item_list[2]))


        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #要求亚马逊将来自亚马逊实现网络中卖方库存的项目运送到目的地地址
    #DisplayableOrderDateTime   yyyy-mm-dd
    def CreateFulfillmentOrder(execute_command):
        params = ['Action=CreateFulfillmentOrder'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command) 

        params.append('SellerFulfillmentOrderId=' + quote(execute_command['seller_order_id']))
        params.append('DisplayableOrderId=' + quote(execute_command['display_order_id']))
        params.append('DisplayableOrderDateTime=' + quote(execute_command['display_order_datetime']))
        params.append('DisplayableOrderComment=' + quote(execute_command['display_order_comment']))
        params.append('ShippingSpeedCategory=' + quote(execute_command['ship_speed_category']))
        params.append('DestinationAddress.Name=' + quote(execute_command['address_name']))
        params.append('DestinationAddress.Line1=' + quote(execute_command['address_line1']))
        params.append('DestinationAddress.Line2=' + quote(execute_command['address_line2']))
        params.append('DestinationAddress.CountryCode=' + quote(execute_command['country_code']))
        params.append('DestinationAddress.StateOrProvinceCode=' + quote(execute_command['state_province_code']))
        params.append('DestinationAddress.PostalCode=' + quote(execute_command['postal_code']))
        params.append('Items.member.1.DisplayableComment=' + quote(execute_command['dispaly_comment']))
        params.append('Items.member.1.GiftMessage=' + quote(execute_command['gift_message']))
        params.append('Items.member.1.PerUnitDeclaredValue.CurrencyCode=' + quote(execute_command['puv_currency_code']))
        params.append('Items.member.1.PerUnitDeclaredValue.Value=' + quote(execute_command['puv_value']))
        params.append('Items.member.1.PerUnitPrice.CurrencyCode=' + quote(execute_command['pup_currency_code']))
        params.append('Items.member.1.PerUnitPrice.Value=' + quote(execute_command['pup_value']))
        params.append('Items.member.1.PerUnitTax.CurrencyCode=' + quote(execute_command['put_currency_code']))
        params.append('Items.member.1.PerUnitTax.Value=' + quote(execute_command['put_value']))
        params.append('Items.member.1.Quantity=' + quote(execute_command['quantity']))
        params.append('Items.member.1.SellerFulfillmentOrderItemId=' + quote(execute_command['sell_orderitem_id']))
        params.append('Items.member.1.SellerSKU=' + quote(execute_command['sell_sku']))
        if 'start_time' in execute_command:
            st = quote(execute_command['start_time'])
            st_timeArray = common_unit.time_to_timeArray(st)
            params.append('DeliveryWindow.StartDateTime=' + st_timeArray) 
        else:
            params.append('DeliveryWindow.StartDateTime=')

        if 'end_time' in execute_command:
            et = quote(execute_command['end_time'])
            et_timeArray = common_unit.time_to_timeArray(et)
            params.append('DeliveryWindow.EndDateTime=' + et_timeArray) 
        else:
            params.append('DeliveryWindow.EndDateTime=')

        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result



    #更新和/或请求订单完成订单的发货
    #请求参数   SellerFulfillmentOrderId  必须
    def UpdateFulfillmentOrder(execute_command):
        params = ['Action=UpdateFulfillmentOrder'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('SellerFulfillmentOrderId=' + quote(execute_command['order_id']))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result


    #根据指定的SellerFulfillmentOrderId返回执行订单
    #参数  order_id
    def GetFulfillmentOrder(execute_command):
        params = ['Action=GetFulfillmentOrder'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('SellerFulfillmentOrderId=' + quote(execute_command['order_id']))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #返回在指定日期（或以后）完成的履行订单清单
    #参数  QueryStartDateTime
    def ListAllFulfillmentOrders(execute_command):
        params = ['Action=ListAllFulfillmentOrders'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        if 'start_time' in execute_command:
            st = execute_command['start_time'] + 'T00:00:00'
            # st_timeArray = common_unit.time_to_timeArray(st)
            params.append('QueryStartDateTime=' + quote(st))  # 添加请求中包含的start_time
        else:
            params.append('QueryStartDateTime=')
        params = params + default_params
        print(params)
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #使用NextToken参数返回履行订单的下一页
    #给进来参数[next_token]
    def ListAllFulfillmentOrdersByNextToken(execute_command):
        ntoken = quote(execute_command['next_token'])
        params = 'Action=ListAllFulfillmentOrdersByNextToken&NextToken='+ntoken
        url = 'https://'+ host_name + port_point + '?' + params
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result



    #返回多渠道配送订单的出货中包裹的配送跟踪信息
    #参数  PackageNumber  件号
    def GetPackageTrackingDetails(execute_command):
        params = ['Action=GetPackageTrackingDetails'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('PackageNumber=' + quote(execute_command['package_number']))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result


    #要求亚马逊停止尝试完成现有的配送订单
    def CancelFulfillmentOrder(execute_command):
        params = ['Action=CancelFulfillmentOrder'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典

        params.append('SellerFulfillmentOrderId=' + quote(execute_command['order_id']))

        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    # 返回给定 seller SKU的退货原因代码 描述 列表
    # 参数  order_id 可以为空   seller_sku 必须   Language 也是可以为空  格式如：fr_FR
    def ListReturnReasonCodes(execute_command):
        params = ['Action=ListReturnReasonCodes'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        if 'order_id' in execute_command:
            order_id = quote(execute_command['order_id'])  # 获取参数order_id
            params.append('SellerFulfillmentOrderId=' + order_id)
        else:
            params.append('SellerFulfillmentOrderId=')

        params.append('SellerSKU=' + quote(execute_command['seller_sku']))  # 获取参数seller_sku

        if 'language' in execute_command:
            language = quote(execute_command['language'])  # 获取参数language
            params.append('Language=' + language)
        else:
            params.append('Language=')

        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #创建一个 配送列表的返回
    def CreateFulfillmentReturn(execute_command):
        params = ['Action=CreateFulfillmentReturn'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典

        params.append('SellerFulfillmentOrderId=' + quote(execute_command['seller_order_id']))
        params.append('Items.member.1.SellerReturnItemId=' + quote(execute_command['item_id']))
        params.append('Items.member.1.SellerFulfillmentOrderItemId=' + quote(execute_command['order_item_id']))
        params.append('Items.member.1.AmazonShipmentId=' + quote(execute_command['ship_id']))
        params.append('Items.member.1.ReturnReasonCode=' + quote(execute_command['reason_code']))
        params.append('Items.member.1.ReturnComment=' + quote(execute_command['comment']))

        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result


    # 返回  配送出库 这块API的操作状态
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