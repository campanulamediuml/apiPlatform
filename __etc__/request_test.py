import requests
import json
import time
from urllib.parse import quote
from datetime import datetime
import sys
sys.path.append('../')
from amazon import interface_fulfillmentOutboundShipment
from common_methods import common_unit
from multiprocessing.dummy import Pool as ThreadPool
# import common_methods.common_unit as cu

def main_1(a):
    # url = 'http://172.18.158.167:8888/amazon_execute/'
    url = 'http://localhost:9527/amazon_execute/reports'

    content_2 = {'method':'RequestReport','store_id':'8','report_type':'_GET_PADS_PRODUCT_PERFORMANCE_OVER_TIME_DAILY_DATA_XML_'}

    content = content_2
    time_1 = time.time()
    r = requests.post(url,content)
    time_2 = time.time()
    # print(json.dumps(content))
    return r.text

# POST
# mws.amazonservices.com
# /FulfillmentInventory/2010-10-01
# AWSAccessKeyId=AKIAI4IDB6MWJPVSDKQQ&Action=ListInventorySupply&MWSAuthToken=amzn.mws.fcafccdc-8aca-0e02-69cb-ca594407d1cf&MarketplaceId=ATVPDKIKX0DER&QueryStartDateTime=1970-12-31T16%3A00%3A00Z&SellerId=A23LGBE17JOXAI&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=2018-04-13T02%3A43%3A59Z&Version=2010-10-01
ThreadPool(4).map(main_1,range(1,5))
# AWSAccessKeyId=AKIAI4IDB6MWJPVSDKQQ&Action=ListInventorySupply&MWSAuthToken=amzn.mws.fcafccdc-8aca-0e02-69cb-ca594407d1cf&MarketplaceId=ATVPDKIKX0DER&QueryStartDateTime=1970-12-31T16:00:00&SellerId=A23LGBE17JOXAI&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=2018-04-13T02%3A49%3A00.00Z&Version=2010-10-01
# print(main_1())
# def main_2():
#     # url = 'http://172.18.158.167:8888/amazon_execute/'
#     url = 'http://localhost:9527/amazon_execute/feed'

#     content_2 = {'company_id':'0','sku':'9500-blue-S','method':'GetFeedSubmissionList','store_id':'1'}

#     content = content_2
#     time_1 = time.time()
#     r = requests.post(url,content)
#     time_2 = time.time()
#     # print(json.dumps(content))
#     return r.text

# def main_3():
#     # url = 'http://172.18.158.167:8888/amazon_execute/'
#     url = 'http://localhost:9527/amazon_execute/feed'

#     content_2 = {'company_id':'0','sku':'9500-blue-S','method':'GetFeedSubmissionResult','store_id':'1','submission_id':'50215017563'}

#     content = content_2
#     time_1 = time.time()
#     r = requests.post(url,content)
#     time_2 = time.time()
#     # print(json.dumps(content))
#     return r.text


# # def main(a):
#     # url = 'http://172.18.158.167:8888/amazon_execute/'
# def test_order(a):
#     url = 'http://localhost:9527/amazon_execute/order'
#     content_0 = {'method': 'ListOrders', 'company_id': '11'}
#     content = content_0       
#     # time_1 = time.time()
#     r = requests.post(url,content)
#     # time_2 = time.time()
#     # print(json.dumps(content))
#     print(r.text)

# test_order(1)

# # def main(a):

# #     url = 'http://localhost:9527/amazon_execute/product'

# #     content_2 = {'company_id':'0','create_time':'','method':'GetProductCategoriesForSKU','sku':'L9-FMHH-FXTO','store_id':'1'}

# #     content = content_2
# #     time_1 = time.time()
# #     r=requests.post(url,content)
# #     time_2 = time.time()
# #     # print(json.dumps(content))
# #     print('successful')
# #     return r.text

# # result = main()
# # print(result)
# # time_stamp = common_unit.get_time_stamp_now()

# # test_order(1)

# # open('log.log','a').write(str(time_stamp)+'\n')
# # open('log.log','a').write(str(result)+'\n\n\n')
# # a_list = [1,9,9,9,1,9,1,9,1,9,1,1,1,1,9,1,1,9,9,9,1,1,1,1,9,1,9,1,9,9,1,1]
# # ThreadPool().map(test_order,a_list)
# # execute_command = {'company_id':'0','create_time':'','method':'ListAllFulfillmentOrders','start_time':'2017-01-01','store_id':'1','order_id':'111-9614293-5919424'}
# # result = interface_fulfillmentOutboundShipment.interface_fulfillmentOutboundShipment.ListAllFulfillmentOrders(execute_command)
# # print(result)


# # def feed():
# #     # url = 'http://172.18.158.167:8888/amazon_execute/'
# #     url = 'http://localhost:9527/amazon_execute/feed'

# #     content_2 = {'company_id':'0','sku':'9655','method':'SubmitFeed','store_id':'1'}

# #     content = content_2
# #     time_1 = time.time()
# #     r = requests.post(url,content)
# #     time_2 = time.time()
# #     # print(json.dumps(content))
# #     print(r.text)
# #     return r.text

# # feed()


