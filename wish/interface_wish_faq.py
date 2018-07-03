#coding=utf-8
import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from wish import wish_common

#常见问题的解决
class Faq:

    def __init__(self):
        pass

#更新产品价格
    def update_price(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        sku = quote(execute_command['sku'])
        new_price = quote(execute_command['new_price'])
        url = "https://merchant.wish.com/api/v2/variant/update?access_token=%s&sku=%s&price=%s"%(access_token,sku,new_price)
        r = requests.post(url)
        result = r.text
        return result

#更新产品库存
    def update_inventory(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        sku = quote(execute_command['sku'])
        inventory = quote(execute_command['inventory'])
        url = "https://merchant.wish.com/api/v2/variant/update-inventory?access_token=%s&sku=%s&inventory=%s"%(access_token,sku,inventory)
        r = requests.post(url)
        result = r.text
        return result

#启用/禁用产品
    def enable_product(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        product_id = quote(execute_command['product_id'])
        url = "https://merchant.wish.com/api/v2/product/enable?access_token=%s&id=%s"%(access_token, product_id)
        r = requests.post(url)
        result = r.text
        return result

    
