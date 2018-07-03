import sys
sys.path.append('../')
import requests
from urllib.parse import quote
import time
from common_methods import common_unit


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Finances/2015-05-01'
api_version = ['Version=2015-05-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y


class interface_finances:

    def __init__(self):
        pass
    #返回给定日期范围的资金/财务集合
    #参数 page(返回结果页面的最大页码数)  Minimum: 1 , Maximum: 100  , Default: 100  , Type: xs:int   可以为空
    #参数 start_time(查询的开始时间)   Type: xs:dateTime
    #参数 end_time(查询的结束时间) 可以为空 Type: xs:dateTime
    def ListFinancialEventGroups(execute_command):
        params = ['Action=ListFinancialEventGroups'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        if 'page' in execute_command:
            params.append('MaxResultsPerPage=' + quote(execute_command['page']))     #需要几页
        else:
            params.append('MaxResultsPerPage=')

        st = quote(execute_command['start_time'])
        st_timeArray = common_unit.time_to_timeArray(st)
        params.append('FinancialEventGroupStartedAfter=' + st_timeArray)   # 添加请求中包含的start_time

        if 'end_time' in execute_command:
            et = quote(execute_command['end_time'])
            et_timeArray = common_unit.time_to_timeArray(et)
            params.append('FinancialEventGroupStartedBefore=' + et_timeArray)
        else:
            params.append('FinancialEventGroupStartedBefore=')     # 添加请求中包含的end_time
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #返回资金/财务集合的下一页 参数使用nexttoken


    def ListFinancialEventGroupsByNextToken(execute_command):
        params = ['Action=ListFinancialEventGroupsByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
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

    #返回资金事件
    #四个参数  任意给一个 order_id \ event_group_id \ start_time \ end_time
    def ListFinancialEvents(execute_command):
        params = ['Action=ListFinancialEvents'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典

        if 'page' in execute_command:
            params.append('MaxResultsPerPage=' + quote(execute_command['page']))     #返回结果页数
        else:
            params.append('MaxResultsPerPage=')

        if 'order_id' in execute_command:
            params.append('AmazonOrderId=' + quote(execute_command['order_id']))     #订单编号
        else:
            params.append('AmazonOrderId=')

        if 'event_group_id' in execute_command:
            params.append('FinancialEventGroupId=' + quote(execute_command['event_group_id']))  #事件组编号
        else:
            params.append('FinancialEventGroupId=')

        if 'start_time' in execute_command:
            st = quote(execute_command['start_time'])
            st_timeArray = common_unit.time_to_timeArray(st)
            params.append('PostedAfter=' + st_timeArray)  #开始时间
        else:
            params.append('PostedAfter=')

        if 'end_time' in execute_command:
            et = quote(execute_command['end_time'])
            et_timeArray = common_unit.time_to_timeArray(et)
            params.append('PostedBefore=' + et_timeArray)  #结束时间
        else:
            params.append('PostedBefore=')

        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    def ListFinancialEventsByNextToken(execute_command):
        params = ['Action=ListFinancialEventsByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
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


    # 返回 资金 这块API的操作状态
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