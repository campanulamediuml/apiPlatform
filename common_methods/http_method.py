#coding=utf-8
import sys
sys.path.append('../')
import json
from wish import wish_methods
from joom import joom_methods
from urllib.parse import unquote
from amazon import interface_products
from amazon import interface_sellers
from amazon import interface_orders
from amazon import interface_recommendations
from amazon import interface_reports
from amazon import interface_finances
from amazon import interface_fulfillmentInventory
from amazon import interface_fulfillmentOutboundShipment
from amazon import interface_feeds

import requests
from wish import interface_wish_order
from wish import interface_wish_faq
from wish import interface_wish_product
from wish import interface_wish_ticket
from wish import interface_wish_notifications

from joom import interface_joom_order

def amazon_execute_method_product(request):
    print('/amazon_execute/product is recieved a post request')
    data = request.request.body
    # print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_products.interface_products.'+execute_command['method'])
    # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)
    #处理请求参数，
    result = return_data
    return result

def amazon_execute_method_order(request):
    print('/amazon_execute/order is recieved a post request')
    data = request.request.body
    # print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_orders.interface_orders.'+execute_command['method'])
    # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)
    #处理请求参数，
    result = return_data
    return result
    
def amazon_execute_method_seller(request):
    print('/amazon_execute/seller is recieved a post request')
    data = request.request.body
    # print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_sellers.interface_sellers.'+execute_command['method'])
    # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)
    #处理请求参数
    result = return_data
    return result


def amazon_execute_method_fulfillment_inbound_shipment(request):
    print('/amazon_execute/fulfillment_inbound_shipment is recieved a post request')
    data = request.request.body
    # print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_fulfillment_inbound_shipment.interface_fulfillment_inbound_shipment.'+execute_command['method'])
    # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)
    #处理请求参数
    result = return_data
    return result

#实现库存   完成清单
def amazon_execute_method_fulfillment_inventory(request):
    print('/amazon_execute/fulfillmentInventory is recieved a post request')
    data = request.request.body
    # print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_fulfillmentInventory.interface_fulfillmentInventory.' + execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)  # 处理请求参数
    result = return_data
    return result

#配送出库
def amazon_execute_method_fulfillment_outbound_shipment(request):
    print('/amazon_execute/fulfillmentOutboundShipment is recieved a post request')
    data = request.request.body
    # print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_fulfillmentOutboundShipment.interface_fulfillmentOutboundShipment.' + execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)  # 处理请求参数
    result = return_data
    return result

#资金
def amazon_execute_method_finances(request):
    print('/amazon_execute/finances is recieved a post request')
    data = request.request.body
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_finances.interface_finances.'+execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)   #处理请求参数
    result = return_data
    return result

def amazon_execute_method_recommendation(request):
    print('/amazon_execute/recommendation is recieved a post request')
    data = request.request.body
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_recommendations.interface_recommendations.'+execute_command['method'])
    # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)
    #处理请求参数，
    result = return_data
    return result

#报告
def amazon_execute_method_reports(request):
    print('/amazon_execute/reports is recieved a post request')
    data = request.request.body
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_reports.interface_reports.'+execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)   #处理请求参数
    result = return_data
    return result

def amazon_execute_method_merchant_fulfillment(request):
    print('/amazon_execute/merchant_fulfillment is recieved a post request')
    data = request.request.body
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_merchant_fulfillment.interface_merchant_fulfillment.'+execute_command['method'])
    # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)
    #处理请求参数，
    result = return_data
    return result


#订阅
def amazon_execute_method_subscriptions(request):
    print('/amazon_execute/subscriptions is recieved a post request')
    data = request.request.body      # 传入的参数集
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_subscriptions.interface_subscriptions.'+execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)   #处理请求参数
    result = return_data
    return result

def amazon_execute_method_feed(request):
    print('/amazon_execute/feed is recieved a post request')
    data = request.request.body      # 传入的参数集
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_feeds.interface_feeds.'+execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)   #处理请求参数
    result = return_data
    return result

#================================================================
#WISH

def wish_execute_order(request):
    print('/wish/orders is recieved a get request')
    data = request.request.body  # 传入的参数集
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_wish_order.Order.' + execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)  # 处理请求参数
    result = return_data
    return result

def wish_execute_faq(request):
    data = request.request.body  # 传入的参数集
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_wish_faq.Faq.' + execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)  # 处理请求参数
    result = return_data
    return result

def wish_execute_product(request):
    data = request.request.body  # 传入的参数集
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_wish_product.Product.' + execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)  # 处理请求参数
    result = return_data
    return result

def wish_execute_ticket(request):
    data = request.request.body  # 传入的参数集
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_wish_ticket.Ticket.' + execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)  # 处理请求参数
    result = return_data
    return result

def wish_execute_notifications(request):
    data = request.request.body  # 传入的参数集
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_wish_notifications.Notifications.' + execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)  # 处理请求参数
    result = return_data
    return result

#joom
def joom_execute_order(request):
    print('/wish/orders is recieved a get request')
    data = request.request.body  # 传入的参数集
    print(data)
    data = data.decode('utf-8').split('&')
    execute_command = {}
    for item in data:
        execute_command[unquote(item.split('=')[0])] = unquote(item.split('=')[1])
    method = eval('interface_joom_order.Order.' + execute_command['method'])  # 传入的json字符串中有method这个键，通过eval直接寻找对应键值的方法名
    print(execute_command)
    return_data = method(execute_command)  # 处理请求参数
    result = return_data
    return result
