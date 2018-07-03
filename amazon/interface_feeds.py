import sys
sys.path.append('../')
import requests
from urllib.parse import quote
import time
from common_methods import common_unit
from amazon import make_submit_feed


headers = common_unit.headers
default_params = common_unit.default_params
host_name = headers['Host']
port_point = '/Feeds/2009-01-01'
api_version = ['Version=2009-01-01'] # 关于api的分类和版本
connect_url = lambda x,y:'https://'+host_name+port_point+'?'+x+'&Signature='+y


def upload_product(execute_command):

    params = ['Action=SubmitFeed'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
    user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
    params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典

    # if execute_command['feed_method'] == 
    params += ['FeedType=_POST_PRODUCT_DATA_']
    # request_content = make_feed.feed_string
    request_content = make_submit_feed.make_feed_string(execute_command)
    request_content = bytes(request_content, 'utf-8')
    # print(request_content)
    # print(type(request_content)) 
    # print(common_unit.get_md5(request_content))
    params += ['ContentMD5Value='+quote(common_unit.get_md5(request_content)).replace('/','%2F')]
    params = params + default_params
    params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
    params = '&'.join(params)  # 对请求身进行分割
    sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
    signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
    url = connect_url(params, signature)  # 拼接请求字符串
    r = requests.post(url, request_content, headers=headers)  # 发起请求
    result = common_unit.xmltojson(r.text)
    return result


class interface_feeds:
    def __init__(self):
        pass
    def SubmitFeed(execute_command):
        if execute_command['feed_method'] == 'upload':
            result = upload_product(execute_command)
        return result        

    def GetFeedSubmissionList(execute_command):
        params = ['Action=GetFeedSubmissionList'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)
        params = params + default_params + ['MaxCount=99']

        params = sorted(params)
        # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params) 
        # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名

        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)

        return result


    def GetFeedSubmissionCount(execute_command):
        params = ['Action=GetFeedSubmissionCount'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典

        params += ['FeedProcessingStatusList.Status.1=_DONE_']
        params += ['FeedProcessingStatusList.Status.2=_CANCELLED_']
        params += ['FeedTypeList.Type.1=_POST_PRODUCT_DATA_']

        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    def CancelFeedSubmissions(execute_command):
        params = ['Action=CancelFeedSubmissions'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典

        params += ['FeedTypeList.Type.1=_POST_PRODUCT_DATA_']
        params += ['FeedTypeList.Type.2=_POST_PRODUCT_PRICING_DATA_']

        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    def GetFeedSubmissionResult(execute_command):
        params = ['Action=GetFeedSubmissionResult'] + api_version + ['Timestamp=' + common_unit.get_time_stamp()]
        user_access_dict = common_unit.get_amazon_keys(execute_command['store_id'])
        params += common_unit.make_access_param(user_access_dict, execute_command)  # 获取包含认证参数的字典

        # params += ['FeedTypeList.Type.1=_POST_PRODUCT_DATA_']
        # params += ['FeedTypeList.Type.2=_POST_PRODUCT_PRICING_DATA_']
        feed_submission_id = execute_command['submission_id']
        params += ['FeedSubmissionId='+feed_submission_id]

        params = params + default_params
        params = sorted(params)  # 拼接公有请求参数，认证请求参数，和特征请求参数，并进行排序,拼接请求身，需要按首字母排序
        params = '&'.join(params)  # 对请求身进行分割
        sig_string = 'POST\n' + host_name + '\n' + port_point + '\n' + params  # 连接签名字符串
        signature = quote(str(common_unit.cal_signature(sig_string, user_access_dict['secret_key'])))  # 计算字符串的加密签名
        url = connect_url(params, signature)  # 拼接请求字符串
        r = requests.post(url, headers=headers)  # 发起请求
        result = common_unit.xmltojson(r.text)
        return result

    



    

