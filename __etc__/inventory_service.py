#coding=utf-8
import requests
import json
import time
import sys
sys.path.append('../')
from common_methods import common_unit
# from amazon.interface_fulfillmentInventory import interface_fulfillmentInventory as inventory



class Inventory_service:
    def __int__(self):
        pass

    # 第一次同步, 准备同步库存的所需要的参数   每个店铺的那些个key   以及开始时间
    def first_syn_stock(self):
        status = 0
        store_id_list = common_unit.get_store(status)
        for sid in store_id_list:
            # user_access_dict = common_unit.get_amazon_keys(sid)      #获取基本 店铺参数
            # result = inventory.syn_inventory(user_access_dict)       #请求触发接口
            url = 'http://localhost:9527/amazon_execute/fulfillment_inventory'
            params = {'store_id':sid,'method':'syn_inventory'}
            result = requests.post(url,params)
            self.deal_result(result,sid)     #处理请求结果,并写入数据库
            self.update_store_status(sid)    #更新店铺的表的状态    第一次同步完成之后更新状态为1

    #处理请求结果,并写入数据库
    def deal_result(self,result,store_id):
        l_result = json.loads(result)
        members = l_result['ListInventorySupplyResponse']['ListInventorySupplyResult']['InventorySupplyList']['member']
        for m in members:
            length_key = len(m.keys())
            if length_key == 7:
                fnsku = m['FNSKU']
                sku = m['SellerSKU']
                condition = m['Condition']
                total = m['TotalSupplyQuantity']
                asin = m['ASIN']
                instock = m['InStockSupplyQuantity']
                supplyDetail = m['SupplyDetail']
                tpt = ''
                # print ([fnsku,sku,condition,total,asin,instock,supplyDetail])
                stock_list = [fnsku, sku, condition, total, asin, instock, supplyDetail, tpt, store_id]
                self.write_into_fba_stock(stock_list)    #写入数据库
            elif (length_key == 8):
                fnsku = m['FNSKU']
                sku = m['SellerSKU']
                condition = m['Condition']
                total = m['TotalSupplyQuantity']
                asin = m['ASIN']
                instock = m['InStockSupplyQuantity']
                supplyDetail = m['SupplyDetail']
                ea = m['EarliestAvailability']
                tpt = ea['TimepointType']
                # print ([fnsku,sku,condition,total,asin,instock,supplyDetail,tpt])
                stock_list = [fnsku, sku, condition, total, asin, instock, supplyDetail, tpt, store_id]
                self.write_into_fba_stock(stock_list)   #写入数据库

    # 更新操作   第一次同步完成之后,后面每次同步都是更新操作
    def second_syn_stock(self):
        status = 1
        store_id_list = common_unit.get_store(status)
        for sid in store_id_list:
            user_access_dict = common_unit.get_amazon_keys(sid)
            sku_list = self.get_skuList(sid)
            # inventory.ListInventorySupply(user_access_dict, sku_list)


    # 将具体每个sku对应的库存写进数据库
    def write_into_fba_stock(sele,stock_list):
        cursor, conn = common_unit.database_connection()
        sku = stock_list[1]
        rs = cursor.execute("select * from syn_fba_stocks where sku='%s'" % (sku))
        if rs >= 1:
            print('已经同步过了,需要做的是更新操作')
        else:
            cursor.execute(
                'INSERT INTO syn_fba_stocks(fnsku,sku,term,total,asin,instock_quant,supply_detail,tpoint_type,store_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                stock_list)
            conn.commit()

    # 更新店铺的状态  (即第一次同步完成之后状态为置为1)
    def update_store_status(self,store_id):
        cursor, conn = common_unit.database_connection()
        cursor.execute("update stores set status=1 where id='%s'" % (store_id))
        conn.commit()

    # 获取每家店铺的sku列表
    def get_skuList(self,store_id):
        cursor, conn = common_unit.database_connection()
        cursor.execute("select sku from syn_fba_stocks where store_id='%s'" % (store_id))
        sellerSku_list = []
        for sku in cursor.fetchall():
            sellerSku_list.append(sku[0])
        return sellerSku_list

    # first_syn_stock()
    second_syn_stock()