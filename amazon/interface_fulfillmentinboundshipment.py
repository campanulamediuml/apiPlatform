import sys
sys.path.append('../')
import requests
from urllib.parse import quote
import time
from common_methods import common_unit


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/FulfillmentInboundShipment/2010-10-01'
api_version = ['Version=2010-10-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y

class interface_fulfillment_inbound_shipment:
    def __init__(self):
        pass   

    def GetInboundGuidanceForSKU(execute_command):
        params = ['Action=GetInboundGuidanceForSKU']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)

        if 'seller_sku' in execute_command:
            seller_sku_list = execute_command['seller_sku'].split(',')
        seller_sku_param_list = []
        #计算sku列表
        try:
            for i in seller_sku_list:
                seller_sku_param_list.append('SellerSKUList.Id.'+str(seller_sku_list.index(i)+1)+'='+i)
        except:
            seller_sku_param_list = ['SellerSKUList.Id.1=']

        params = params + default_params + seller_sku_param_list

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

    def GetInboundGuidanceForASIN(execute_command):
        params = ['Action=GetInboundGuidanceForASIN']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)

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

    def CreateInboundShipmentPlan(execute_command):
        params = ['Action=CreateInboundShipmentPlan']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
        #params += ['ShipFromAddress='+execute_command['from_address']]
        params += ['ShipFromAddress.Name='+execute_command['address_name']]
        params += ['ShipFromAddress.AddressLine1='+execute_command['address_line']]
        params += ['ShipFromAddress.City='+execute_command['address_city']]
        params += ['ShipFromAddress.CountryCode='+execute_command['address_country']]
        #添加寄出地址

        params += ['ShipToCountryCode='+common_unit.country_code[execute_command['to_address_country']]]
        #此处应传入一个用逗号分隔的地区代码
        # CA – Canada
        # MX – Mexico
        # US – United States
        params += ['LabelPrepPreference=SELLER_LABEL']
        params += ['InboundShipmentPlanRequestItems.member.1.SellerSKU='+execute_command['seller_sku']]
        params += ['InboundShipmentPlanRequestItems.member.1.Quantity='+execute_command['quantity']]
        
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

    def CreateInboundShipment(execute_command):
        return
        # 暂时放着没法制作，这个接口标准太傻比了
    def UpdateInboundShipment(execute_command):
        return
    def GetPreorderInfo(execute_command):
        params = ['Action=GetPreorderInfo']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
        params += ['ShipmentId='+execute_command['shipment_id']]
        # 添加货运单编号

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

    def ConfirmPreorder(execute_command):
        params = ['Action=ConfirmPreorder']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
        params += ['ShipmentId='+execute_command['shipment_id']]
        # 添加运单编号

        params += ['NeedByDate='+common_unit.timestamp_to_datetime(execute_command['need_by_time'])]
        # 添加时间戳，此处李豪传入的时间戳应该统一为timestamp格式，然后我拿到再来转换，以方便后端
        params = sorted(params)
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

    def GetPrepInstructionsForSKU(execute_command):
        params = ['Action=GetPrepInstructionsForSKU']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)

        if 'seller_sku' in execute_command:
            seller_sku_list = execute_command['seller_sku'].split(',')
        seller_sku_param_list = []
        #计算sku列表
        try:
            for i in seller_sku_list:
                seller_sku_param_list.append('SellerSKUList.Id.'+str(seller_sku_list.index(i)+1)+'='+i)
        except:
            seller_sku_param_list = ['SellerSKUList.Id.1=']

        params = params + default_params + seller_sku_param_list
        # 链接sku

        params += ['ShipToCountryCode='+common_unit.country_code[execute_command['to_address_country']]]

        params = sorted(params)
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

    def GetPrepInstructionsForASIN(execute_command):
        params = ['Action=GetPrepInstructionsForASIN']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)

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
        # 链接sku

        params += ['ShipToCountryCode='+common_unit.country_code[execute_command['to_address_country']]]

        params = sorted(params)
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

    def PutTransportContent(execute_command):
        pass

    def EstimateTransportRequest(execute_command):
        params = ['Action=EstimateTransportRequest']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
       
        params = params + default_params

        params += ['ShipmentId='+execute_command['shipment_id']]

        params = sorted(params)
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

    def GetTransportContent(execute_command):
        params = ['Action=GetTransportContent']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
       
        params = params + default_params

        params += ['ShipmentId='+execute_command['shipment_id']]

        params = sorted(params)
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

    def ConfirmTransportRequest(execute_command):
        params = ['Action=ConfirmTransportRequest']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
        params = params + default_params

        params += ['ShipmentId='+execute_command['shipment_id']]

        params = sorted(params)
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

    def VoidTransportRequest(execute_command):
        params = ['Action=VoidTransportRequest']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
        params = params + default_params

        params += ['ShipmentId='+execute_command['shipment_id']]

        params = sorted(params)
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

    def GetPackageLabels(execute_command):
        params = ['Action=GetPackageLabels']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
        params = params + default_params

        params += ['ShipmentId='+execute_command['shipment_id']]
        params += ['PageType=PackageLabel_Plain_Paper']

        params = sorted(params)
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
        
    # def GetUniquePackageLabels(execute_command):
    #     params = ['Action=GetUniquePackageLabels']+api_version+['Timestamp='+common_unit.get_time_stamp()]
    #     user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
    #     params += default_params
    #     # 获取认证参数
    #     # 把认证参数添加进请求头
    #     params += common_unit.make_access_param(user_access_dict,execute_command)
    #     params = params + default_params

    #     params += ['ShipmentId='+execute_command['shipment_id']]
    #     params += ['PageType=PackageLabel_Plain_Paper']

    #     params = sorted(params)
    #     params = '&'.join(params)
    #     # print(params)
    #     # 对请求身进行分割
    #     sig_string = 'POST\n'+host_name+'\n'+port_point+'\n'+params
    #     # 连接签名字符串
    #     signature = quote(str(common_unit.cal_signature(sig_string,user_access_dict['secret_key'])))
    #     # 计算字符串的加密签名
    #     url = connect_url(params,signature)
    #     # 拼接请求字符串
    #     r = requests.post(url,headers=headers)
    #     # 发起请求
    #     # print(common_unit.xmltojson(r.text))
    #     return common_unit.xmltojson(r.text) 

    def GetPalletLabels(execute_command):
        params = ['Action=GetPalletLabels']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
        params = params + default_params

        params += ['ShipmentId='+execute_command['shipment_id']]
        params += ['PageType=PackageLabel_Plain_Paper']
        params += ['NumberOfPallets=4']
        #这边添加这个接口的特征信息

        params = sorted(params)
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

    def GetBillOfLading(execute_command):
        params = ['Action=GetBillOfLading']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
       
        params = params + default_params

        params += ['ShipmentId='+execute_command['shipment_id']]

        params = sorted(params)
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

    def ListInboundShipments(execute_command):
        pass

    def ListInboundShipmentItems(execute_command):
        params = ['Action=ListInboundShipmentItems']+api_version+['Timestamp='+common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += default_params
        # 获取认证参数
        # 把认证参数添加进请求头
        params += common_unit.make_access_param(user_access_dict,execute_command)
       
        params = params + default_params
        if 'shipment_id' in execute_command:
            params += ['ShipmentId='+execute_command['shipment_id']]

        if 'last_updated_before' in execute_command and 'last_created_after' in execute_command:
            params += ['LastUpdatedAfter='+execute_command['last_updated_after']]
            params += ['LastUpdatedBefore='+execute_command['last_updated_before']]
        # 添加时间区间或者运单id，二者只能存在一样

        params = sorted(params)
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

    def GetServiceStatus(execute_command):
        params = ['Action=GetServiceStatus'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  
        # 获取包含认证参数的字典
        params = params + default_params
        params = sorted(params)  
        # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  
        # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  
        # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  
        # 计算字符串的加密签名
        url = connect_url(params, signature)  
        # 拼接请求字符串
        r = requests.post(url, headers=headers)  
        # 发起请求
        result = common_unit.xmltojson(r.text)
        return result
















