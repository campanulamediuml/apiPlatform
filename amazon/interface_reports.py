import sys
sys.path.append('../')
import requests
from urllib.parse import quote
import time
from common_methods import common_unit


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = ''
api_version = [''] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+'/'+port_point+'?'+x+'&Signature='+y


#报告

class interface_reports:

    def __init__(self):
        pass
    

    #创建一个报告请求和提交请求亚马逊MWS
    def RequestReport(execute_command):
        params = ['Action=RequestReport'] + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        access_params = common_unit.make_access_param(user_access_dict, execute_command)
        market_place_id = access_params[-1].split('=')[1]

        access_params += ['MarketplaceIdList.Id.1='+market_place_id]
        params = params + access_params # 获取包含认证参数的字典
        params.append('ReportType=' + quote(execute_command['report_type']))

        if 'start_time' in execute_command:
            st = quote(execute_command['start_time'])
            st_timeArray = common_unit.time_to_timeArray(st)
            params.append('StartDate=' + st_timeArray)
        else:
            pass    # 添加请求中包含的start_time

        if 'end_time' in execute_command:
            st = quote(execute_command['end_time'])
            st_timeArray = common_unit.time_to_timeArray(st)
            params.append('EndDate=' + st_timeArray)
        else:
            pass       # 添加请求中包含的end_time

        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key']))) # 计算字符串的加密签名
        
        signature = signature.replace('/', '%2F')

        url = connect_url(params, signature)  # 拼接请求字符串
        print(url)
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #返回一个请求报告的列表  用参数ReportRequestId 请求
    def GetReportRequestList(execute_command):
        params = ['Action=GetReportRequestList'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('ReportProcessingStatusList.Status.1='+ quote(execute_command['process_status']))
        params.append('ReportRequestIdList.Id.1=' + quote(execute_command['request_id']))
        if 'start_time' in execute_command:
            st = quote(execute_command['start_time'])
            st_timeArray = common_unit.time_to_timeArray(st)
            params.append('RequestedFromDate=' + st_timeArray)  #开始时间
        else:
            params.append('RequestedFromDate=')

        if 'end_time' in execute_command:
            et = quote(execute_command['end_time'])
            et_timeArray = common_unit.time_to_timeArray(et)
            params.append('RequestedToDate=' + et_timeArray)  #结束时间
        else:
            params.append('RequestedToDate=')

        if 'report_type' in execute_command:
            report_list = execute_command['report_type'].split(',')
        report_type_list = []

        for i in report_list:
            report_type_list.append('ReportTypeList.Type.' + str(report_list.index(i) + 1) + '=' + i)
        params = params + default_params + report_type_list
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result


    #下一页
    def GetReportRequestListByNextToken(execute_command):
        params = ['Action=GetReportRequestListByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
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

    #返回已提交给亚马逊MWS进行处理的报告请求计数
    def GetReportRequestCount(execute_command):
        params = ['Action=GetReportRequestCount'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('ReportProcessingStatusList.Status.1=' + quote(execute_command['process_status']))
        if 'start_time' in execute_command:
            st = quote(execute_command['start_time'])
            st_timeArray = common_unit.time_to_timeArray(st)
            params.append('RequestedFromDate=' + st_timeArray)  # 开始时间
        else:
            params.append('RequestedFromDate=')

        if 'end_time' in execute_command:
            et = quote(execute_command['end_time'])
            et_timeArray = common_unit.time_to_timeArray(et)
            params.append('RequestedToDate=' + et_timeArray)  # 结束时间
        else:
            params.append('RequestedToDate=')

        if 'report_type' in execute_command:
            report_list = execute_command['report_type'].split(',')
        report_type_list = []

        for i in report_list:
            report_type_list.append('ReportTypeList.Type.' + str(report_list.index(i) + 1) + '=' + i)

        params = params + default_params + report_type_list
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #取消一个或多个报告请求
    def CancelReportRequests(execute_command):
        params = ['Action=CancelReportRequests'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('ReportRequestIdList.Id.1=' + quote(execute_command['request_id']))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #返回在前90天中创建的报告列表
    #request_id  传list进来
    def GetReportList(execute_command):
        params = ['Action=GetReportList'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        if 'request_id' in execute_command:
            request_id_list = execute_command['request_id'].split(',')
        request_list = []

        for i in request_id_list:
            request_list.append('ReportRequestIdList.Id.' + str(request_id_list.index(i) + 1) + '=' + i)

        params = params + default_params + request_list
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #上一个接口的下一页
    def GetReportListByNextToken(execute_command):
        params = ['Action=GetReportListByNextToken'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
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

    #返回报告的数量,在过去的90天了，_DONE_ 状态,可供下载
    def GetReportCount(execute_command):
        params = ['Action=GetReportCount'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('ReportTypeList.Type.1=' + quote(execute_command['report_type']))  # 取得参数report_type的值
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #返回报告的内容以及返回的报告主体的Content-MD5头
    def GetReport(execute_command):
        params = ['Action=GetReport'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('ReportId=' + quote(execute_command['report_id']))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #创建，更新或删除指定报告类型的报告请求计划
    def ManageReportSchedule(execute_command):
        params = ['Action=ManageReportSchedule'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('ReportType=' + quote(execute_command['report_type']))
        params.append('Schedule=' + quote(execute_command['schedule']))
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #返回计划提交给亚马逊MWS进行处理的订单报告请求列表
    def GetReportScheduleList(execute_command):
        params = ['Action=GetReportScheduleList'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典

        if 'report_type' in execute_command:
            report_list = execute_command['report_type'].split(',')
        report_type_list = []

        for i in report_list:
            report_type_list.append('ReportTypeList.Type.' + str(report_list.index(i) + 1) + '=' + i)


        params = params + default_params + report_type_list
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #返回计划提交给亚马逊MWS的订单报告请求计数
    def GetReportScheduleCount(execute_command):
        params = ['Action=GetReportScheduleCount'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('ReportTypeList.Type.1=' + quote(execute_command['report_type']))  # 取得参数report_type的值
        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    #更新一个或多个报告的确认状态
    #参数 acknowledged 只有两种状态  true or false
    def UpdateReportAcknowledgements(execute_command):
        params = ['Action=UpdateReportAcknowledgements'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典
        params.append('Acknowledged=' + quote(execute_command['acknowledged']))  # true or false

        if 'request_id' in execute_command:
            request_id_list = execute_command['request_id'].split(',')
        request_list = []

        for i in request_id_list:
            request_list.append('ReportRequestIdList.Id.' + str(request_id_list.index(i) + 1) + '=' + i)

        params = params + default_params + request_list
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result




