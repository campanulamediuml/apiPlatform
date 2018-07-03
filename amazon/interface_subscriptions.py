import sys
sys.path.append('../')
import requests
from urllib.parse import quote
import time
from common_methods import common_unit


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Subscriptions/2013-07-01'
api_version = ['Version=2013-07-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y


#订阅
class interface_subscriptions:

    def __init__(self):
        pass

    #指定您想要接收通知的新目的地
    #参数  MarketplaceId , Destination ；其中destination 以list形式进来值为  destination = [DeliveryChannel,AttributeList.key,AttributeList.value]
    #DeliveryChannel的值为: SQS
    def RegisterDestination(execute_command):
        params = ['Action=RegisterDestination'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        if 'destination' in execute_command:
            destination_list = execute_command['destination'].split(',')
        params.append('Destination.DeliveryChannel='+str(destination_list[0]))
        params.append('Destination.AttributeList.member.1.Key=' + str(destination_list[1]))
        params.append('Destination.AttributeList.member.1.Value=' + str(destination_list[2]))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result


    #从注册的目的地列表中删除现有的目的地
    #参数MarketplaceId , Destination ；其中destination 以list形式进来值为  destination = [DeliveryChannel,AttributeList.key,AttributeList.value]
    #DeliveryChannel的值为: SQS
    def DeregisterDestination(execute_command):
        params = ['Action=DeregisterDestination'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        if 'destination' in execute_command:
            destination_list = execute_command['destination'].split(',')
        params.append('Destination.DeliveryChannel=' + str(destination_list[0]))
        params.append('Destination.AttributeList.member.1.Key=' + str(destination_list[1]))
        params.append('Destination.AttributeList.member.1.Value=' + str(destination_list[2]))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result


    #列出您已注册的所有当前目的地
    #只传一个参数 MarketplaceId
    def ListRegisteredDestinations(execute_command):
        params = ['Action=ListRegisteredDestinations'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
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


    #将测试通知发送到现有目的地
    #参数MarketplaceId , Destination ；其中destination 以list形式进来值为  destination = [DeliveryChannel,AttributeList.key,AttributeList.value]
    #DeliveryChannel的值为: SQS
    def SendTestNotificationToDestination(execute_command):
        params = ['Action=SendTestNotificationToDestination'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        if 'destination' in execute_command:
            destination_list = execute_command['destination'].split(',')
        params.append('Destination.DeliveryChannel=' + str(destination_list[0]))
        params.append('Destination.AttributeList.member.1.Key=' + str(destination_list[1]))
        params.append('Destination.AttributeList.member.1.Value=' + str(destination_list[2]))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result


    #为指定的通知类型和目标创建新的订阅
    #参数 MarketplaceId , Subscription ;其中 Subscription 的值包括 NotificationType,Destination,IsEnabled
    #Subscription.Destination.DeliveryChannel:SQS  ;  Subscription.IsEnabled :   true or flase
    def CreateSubscription(execute_command):
        params = ['Action=CreateSubscription'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        if 'subscription' in execute_command:
            subscription_list = execute_command['subscription'].split(',')
        params.append('Subscription.NotificationType=' + str(subscription_list[0]))
        params.append('Subscription.IsEnabled=' + str(subscription_list[1]))
        params.append('Subscription.Destination.DeliveryChannel=' + str(subscription_list[2]))
        params.append('Subscription.Destination.AttributeList.member.1.Key=' + str(subscription_list[3]))
        params.append('Subscription.Destination.AttributeList.member.1.Value=' + str(subscription_list[4]))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result


    #获取指定通知类型和目标的订阅
    #参数 MarketplaceId  ,  NotificationType ,   Destination
    def GetSubscription(execute_command):
        params = ['Action=GetSubscription'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('NotificationType=' +  quote(execute_command['notificaction_type']))
        if 'destination' in execute_command:
            destination_list = execute_command['destination'].split(',')
        params.append('Destination.DeliveryChannel=' + str(destination_list[0]))
        params.append('Destination.AttributeList.member.1.Key=' + str(destination_list[1]))
        params.append('Destination.AttributeList.member.1.Value=' + str(destination_list[2]))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result


    #删除指定的通知类型和目的地的订阅
    #参数 MarketplaceId  ,  NotificationType ,   Destination
    def DeleteSubscription(execute_command):
        params = ['Action=DeleteSubscription'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('NotificationType=' + quote(execute_command['notificaction_type']))
        if 'destination' in execute_command:
            destination_list = execute_command['destination'].split(',')
        params.append('Destination.DeliveryChannel=' + str(destination_list[0]))
        params.append('Destination.AttributeList.member.1.Key=' + str(destination_list[1]))
        params.append('Destination.AttributeList.member.1.Value=' + str(destination_list[2]))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result


    #返回所有当前订阅的列表
    #只传一个参数  MarketplaceId
    def ListSubscriptions(execute_command):
        params = ['Action=ListSubscriptions'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
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


    #更新指定的通知类型和目的地的订阅
    # 参数 MarketplaceId , Subscription ;其中 Subscription 的值包括 NotificationType,Destination,IsEnabled
    # Subscription.Destination.DeliveryChannel:SQS  ;  Subscription.IsEnabled :   true or flase
    def UpdateSubscription(execute_command):
        params = ['Action=UpdateSubscription'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        if 'subscription' in execute_command:
            subscription_list = execute_command['subscription'].split(',')
        params.append('Subscription.NotificationType=' + str(subscription_list[0]))
        params.append('Subscription.IsEnabled=' + str(subscription_list[1]))
        params.append('Subscription.Destination.DeliveryChannel=' + str(subscription_list[2]))
        params.append('Subscription.Destination.AttributeList.member.1.Key=' + str(subscription_list[3]))
        params.append('Subscription.Destination.AttributeList.member.1.Value=' + str(subscription_list[4]))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result


    # 返回 订阅 这块API的操作状态
    def GetServiceStatus(execute_command):
        params = ['Action=GetServiceStatus'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)          # 获取包含认证参数的字典
        params = params + default_params
        params = sorted(params)             # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)           # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params               # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)        # 拼接请求字符串
        r = requests.post(url, headers=headers)     # 发起请求
        result = common_unit.xmltojson(r.text)
        return result
