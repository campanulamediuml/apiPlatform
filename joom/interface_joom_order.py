#coding=utf-8
import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from joom import joom_common



class Order:
    def __init__(self):
        pass

    def retrieve_order(execute_command):
        order_id = quote(execute_command['order_id'])
        access_token = joom_common.get_joom_access(execute_command['store_id'])
        url = "https://api-merchant.joom.com/api/v2/oauth/order?access_token=%s&id=%s"%(access_token,order_id)
        # print (url)
        r = requests.post(url)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result

#检索最近更改订单
    def recently_changed_orders(execute_command):
        start = quote(execute_command['start'])
        limit = quote(execute_command['limit'])
        since = quote(execute_command['since'])
        access_token =joom_common.get_joom_access(execute_command['store_id'])
        url = "https://api-merchant.joom.com/api/v2/oauth/order/multi-get?start=%s&limit=%s&since=%s&access_token=%s"%(start,limit,since,access_token)
        r = requests.get(url)
        result = r.text
        # print(r.text)
        # result = common_unit.xmltojson(r.text)
        return result


#检索未履行订单
    def retrieve_unfulfilled_orders(execute_command):
        start = quote(execute_command['start'])
        limit = quote(execute_command['limit'])
        access_token =joom_common.get_joom_access(execute_command['store_id'])
        url = "https://api-merchant.joom.com/api/v2/oauth/order/get-fulfill?start=%s&limit=%s&access_token=%s"%(start,limit,access_token)
        # print (url)
        r = requests.get(url)
        # print(r.text)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result


#履行订单
    def fulfill_orders(execute_command):
        order_id = quote(execute_command['order_id'])
        tracking_provider = quote(execute_command['tracking_provider'])
        tracking_number = quote(execute_command['tracking_number'])
        access_token =joom_common.get_joom_access(execute_command['store_id'])
        url = "https://api-merchant.joom.com/api/v2/oauth/order/fulfill-one?access_token=%s&tracking_provider=%s&tracking_number=%s&id=%s"%(access_token,tracking_provider,tracking_number,order_id)
        r = requests.post(url)
        print(r.text)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result


#退款/取消订单
    def refund_order(execute_command):
        order_id = quote(execute_command['order_id'])
        reason_code = quote(execute_command['reason_code'])
        access_token =joom_common.get_joom_access(execute_command['store_id'])
        url = "https://api-merchant.joom.com/api/v2/oauth/order/refund?access_token=%s&reason_code=%s&id=%s" % (access_token,reason_code,order_id)
        r = requests.post(url)
        print(r.text)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result


#修改发运订单的跟踪
    def modify_track_ship_order(execute_command):
        order_id = quote(execute_command['order_id'])
        tracking_number = quote(execute_command['tracking_number'])
        tracking_provider = quote(execute_command['tracking_provider'])
        access_token =joom_common.get_joom_access(execute_command['store_id'])
        url = "https://api-merchant.joom.com/api/v2/oauth/order/modify-tracking?access_token=%s&tracking_provider=%s&tracking_number=%s&id=%s"%(access_token, tracking_provider, tracking_number, order_id)
        r = requests.post(url)
        print(r.text)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result


#在装运前修改订单的发货地址
    def modify_address_order(execute_command):
        country = quote(execute_command['country'])
        state = quote(execute_command['state'])
        city = quote(execute_command['city'])
        street_address1 = quote(execute_command['street_address1'])
        access_token =joom_common.get_joom_access(execute_command['store_id'])
        order_id = quote(execute_command['order_id'])
        url = "https://api-merchant.joom.com/api/v2/oauth/order/change-shipping?access_token=%s&street_address1=%s&city=%s&state=%s&country=%s&id=%s"%(access_token,street_address1,city,state,country,order_id)
        r = requests.post(url)
        print(r.text)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result


#启动批量订单下载
    def batch_order_download(execute_command):
        start = quote(execute_command['start'])
        end = quote(execute_command['end'])
        access_token =joom_common.get_joom_access(execute_command['store_id'])
        url = "https://api-merchant.joom.com/api/v2/oauth/order/create-download-job?access_token=%s&start=%s&end=%s"%(access_token,start,end)
        r = requests.post(url)
        print(r.text)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result


#获取批量订单下载的状态
    def batch_order_download_status(execute_command):
        job_id = quote(execute_command['job_id'])
        access_token =joom_common.get_joom_access(execute_command['store_id'])
        url = "https://api-merchant.joom.com/api/v2/oauth/order/get-download-job-status?access_token=%s&job_id=%s"%(access_token, job_id)
        r = requests.post(url)
        print(r.text)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result


#取消批量订购下载
    def batch_order_download_cancel(execute_command):
        job_id = quote(execute_command['job_id'])
        url = "https://api-merchant.joom.com/api/v2/oauth/order/cancel-download-job?job_id=%s"%(job_id)
        r = requests.post(url)
        print(r.text)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result


#获取需要确认交付的国家
    def get_countries_confirmed_delivery(execute_command):
        access_token =joom_common.get_joom_access(execute_command['store_id'])
        url = "https://api-merchant.joom.com/api/v2/oauth/order/get-confirmed-delivery-countries?access_token=%s"%(access_token)
        r = requests.post(url)
        print(r.text)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result


#获得国家确认的送货船
    def get_shipping_for_country(execute_command):
        access_token = joom_common.get_joom_access(execute_command['store_id'])
        country_code = execute_command['country_code']
        url = "https://api-merchant.joom.com/api/v2/oauth/order/get-confirmed-delivery-shipping-carriers-for-country?access_token=%s&country_code=%s"%(access_token,country_code)
        r = requests.post(url)
        print(r.text)
        result = r.text
        # result = common_unit.xmltojson(r.text)
        return result







