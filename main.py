#coding=utf-8
import tornado.ioloop
import tornado.web
import time
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from wish import wish_common
from joom import joom_common
from common_methods import http_method
from multiprocessing import Pool

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello world')
        self.finish()

class test_thread(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    def get(self):
        time.sleep(10)
        self.write('done!')
        self.finish()
#以上两个纯属没鸡儿用的测试模块……用来实现异步的测试

class amazon_execute_product(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    def post(self):
        result = http_method.amazon_execute_method_product(self)
        self.write(result)
        self.finish()
        print('finish')

class amazon_execute_order(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor

    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.amazon_execute_method_order(self)
        self.write(result)
        self.finish()
        print('finish')

class amazon_execute_seller(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.amazon_execute_method_seller(self)
        self.write(result)
        self.finish()
        print('finish')
# #资金
class amazon_execute_finances(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.amazon_execute_method_finances(self)
        self.write(result)
        self.finish()
        print('finish')

class amazon_execute_recommendation(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.amazon_execute_method_recommendation(self)
        self.write(result)
        self.finish()
        print('finish')

class amazon_execute_fulfillment_inbound_shipment(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.amazon_execute_method_fulfillment_inbound_shipment(self)
        self.write(result)
        self.finish()
        print('finish')
# #库存
class amazon_execute_fulfillment_inventory(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.amazon_execute_method_fulfillment_inventory(self)
        self.write(result)
        self.finish()
        print('finish')
# #配送出库
class amazon_execute_fulfillment_outbound_shipment(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.amazon_execute_method_fulfillment_outbound_shipment(self)
        self.write(result)
        self.finish()
        print('finish')
# #报告
class amazon_execute_reports(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.amazon_execute_method_reports(self)
        self.write(result)
        self.finish()
        print('finish')

class amazon_execute_merchant_fulfillment(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.amazon_execute_method_merchant_fulfillment(self)
        self.write(result)
        self.finish()
        print('finish')
# #订阅
class amazon_execute_subscriptions(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.amazon_execute_method_subscriptions(self)
        self.write(result)
        self.finish()
        print('finish')

class amazon_execute_feed(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.amazon_execute_method_feed(self)
        self.write(result)
        self.finish()
        print('finish')
# #对应亚马逊的product接口

#====================================================================================
#WISH

class wish_execute_order(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.wish_execute_order(self)
        self.write(result)
        self.finish()
        print('finish')


class wish_execute_faq(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.wish_execute_faq(self)
        self.write(result)
        self.finish()
        print('finish')


class wish_execute_product(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.wish_execute_product(self)
        self.write(result)
        self.finish()
        print('finish')


class wish_execute_ticket(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.wish_execute_ticket(self)
        self.write(result)
        self.finish()
        print('finish')


class wish_execute_notifications(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.wish_execute_notifications(self)
        self.write(result)
        self.finish()
        print('finish')


class joom_execute_order(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(40)
    @run_on_executor
    #@tornado.web.asynchronous
    #@gen.coroutine
    def post(self):
        result = http_method.joom_execute_order(self)
        self.write(result)
        self.finish()
        print('finish')



def main():
    method_list = [
            ('/',MainHandler),
            ('/cothread_test',test_thread),
            ("/amazon_execute/product",amazon_execute_product),
            ('/amazon_execute/order',amazon_execute_order),
            ('/amazon_execute/seller',amazon_execute_seller),
            ('/amazon_execute/finances',amazon_execute_finances),
            ('/amazon_execute/feed',amazon_execute_feed),
            ('/amazon_execute/recommendation',amazon_execute_recommendation),
            ('/amazon_execute/fulfillment_inbound_shipment',amazon_execute_fulfillment_inbound_shipment),
            ('/amazon_execute/fulfillment_inventory',amazon_execute_fulfillment_inventory),
            ('/amazon_execute/fulfillment_outbound_shipment',amazon_execute_fulfillment_outbound_shipment),
            ('/amazon_execute/reports',amazon_execute_reports),
            ('/amazon_execute/merchant_fulfillment',amazon_execute_merchant_fulfillment),
            ('/amazon_execute/subscriptions',amazon_execute_subscriptions),
#==================================================================================================
# WISH
            ('/wish/orders',wish_execute_order),
            ('/wish/faq',wish_execute_faq),
            ('wish/product',wish_execute_product),
            ('wish/ticket', wish_execute_ticket),
            ('wish/notifications',wish_execute_notifications),
            # ('/wish/refresh_token',wish_token_refresh)

# 
# joom
            ('joom/order',joom_execute_order)

            ]
    #初始化方法列表
    application = tornado.web.Application(method_list,autoreload=True)
    print('running')
    # wish_common.main_token_refresh_circle()
    application.listen(9527)
    tornado.ioloop.IOLoop.instance().start()


while 1:
    try:
        main()
    except:
        print('reload....')
        continue




    
    