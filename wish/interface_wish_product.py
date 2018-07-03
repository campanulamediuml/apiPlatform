#coding=utf-8
import sys
sys.path.append('../')
import requests
from urllib.parse import quote
from wish import wish_common

class Product:

    def __init__(self):
        pass


    #创建产品
    def create_product(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        main_image = quote(execute_command['main_image'])
        name = quote(execute_command['name'])
        description = quote(execute_command['description'])
        tags = quote(execute_command['tags'])
        sku = quote(execute_command['sku'])
        inventory = quote(execute_command['inventory'])
        price = quote(execute_command['price'])
        shipping = quote(execute_command['shipping'])
        extra_images = quote(execute_command['extra_images'])
        parent_sku = quote(execute_command['parent_sku'])
        url = "https://merchant.wish.com/api/v2/product/add?access_token=%s&main_image=%s&name=%s&description=%s&tags=%s&sku=%s&inventory=%s&price=%s&shipping=%s&extra_images=%s&parent_sku=%s"%(access_token, main_image, name, description, tags, sku, inventory, price, shipping, extra_images, parent_sku)
        r = requests.post(url)
        result = r.text
        return result

    #创建变种产品
    def create_variation_product(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        sku = quote(execute_command['sku'])
        inventory = quote(execute_command['inventory'])
        price = quote(execute_command['price'])
        shipping = quote(execute_command['shipping'])
        size = quote(execute_command['size'])
        parent_sku = quote(execute_command['parent_sku'])
        url = "https://merchant.wish.com/api/v2/variant/add?access_token=%s&sku=%s&inventory=%s&price=%s&shipping=%s&size=%s&parent_sku=%s" %(access_token,sku,inventory,price,shipping,size,parent_sku)
        r = requests.post(url)
        result = r.text
        return result



    #检索产品
    #produt_id 或者  parent_sku   两者取其一
    def retrieve_product(execute_command):
        access_token  = wish_common.get_wish_access(execute_command['store_id'])
        product_id = quote(execute_command['product_id'])
        url = "https://merchant.wish.com/api/v2/product?access_token=%s&id=%s"%(access_token,product_id)
        r = requests.post(url)
        result = r.text
        return result


    #检索变种产品
    def retrieve_variation_product(execute_command):
        access_token  = wish_common.get_wish_access(execute_command['store_id'])
        sku = quote(execute_command['sku'])
        url = "https://merchant.wish.com/api/v2/variant?access_token=%s&id=%s"%(access_token,sku)
        r = requests.post(url)
        result = r.text
        return result


    #编辑产品
    #produt_id 或者  parent_sku   两者取其一
    def update_product(execute_command):
        access_token  = wish_common.get_wish_access(execute_command['store_id'])
        product_id = quote(execute_command['product_id'])
        name =  quote(execute_command['name'])
        description = quote(execute_command['description'])
        tags = quote(execute_command['tags'])
        url = "https://merchant.wish.com/api/v2/product/update?access_token=%s&id=%s&name=%s&description=%s&tags=%s" %(access_token, product_id,name,description,tags)
        r = requests.post(url)
        result = r.text
        return result


    #编辑变种产品信息
    def update_variation_product(execute_command):
        access_token  = wish_common.get_wish_access(execute_command['store_id'])
        sku = quote(execute_command['sku'])
        inventory =  quote(execute_command['inventory'])
        price = quote(execute_command['price'])
        shipping = quote(execute_command['shipping'])
        url = "https://merchant.wish.com/api/v2/product/variant/update?access_token=%s&sku=%s&inventory=%s&price=%s&shipping=%s" %(access_token,sku,inventory,price,shipping)
        r = requests.post(url)
        result = r.text
        return result


    #编辑变种产品的sku
    def change_variation_product_sku(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        sku = quote(execute_command['sku'])
        new_sku = quote(execute_command['new_sku'])
        url = "https://merchant.wish.com/api/v2/variant/change-sku??access_token=%s&sku=%s&new_sku=%s"%(access_token,sku,new_sku)
        r = requests.post(url)
        result = r.text
        return result


    # 启用产品
    # produt_id 或者  parent_sku   两者取其一
    def enable_product(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        product_id = quote(execute_command['product_id'])
        url = "https://merchant.wish.com/api/v2/product/enable?access_token=%s&id=%s"%(access_token, product_id)
        r = requests.post(url)
        result = r.text
        return result


    # 启用变种产品
    def enable_variation_product(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        sku = quote(execute_command['sku'])
        url = "https://merchant.wish.com/api/v2/variant/enable?access_token=%s&sku=%s"%(access_token,sku)
        r = requests.post(url)
        result = r.text
        return result


    #禁用产品
    #produt_id 或者  parent_sku   两者取其一
    def disable_product(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        product_id = quote(execute_command['product_id'])
        url = "https://merchant.wish.com/api/v2/product/disable?access_token=%s&id=%s"%(access_token, product_id)
        r = requests.post(url)
        result = r.text
        return result


    # 禁用变种产品
    def disable_variation_product(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        sku = quote(execute_command['sku'])
        url = "https://merchant.wish.com/api/v2/variant/disable?access_token=%s&sku=%s"%(access_token,sku)
        r = requests.post(url)
        result = r.text
        return result


    #更新  变种
    def update_inventory(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        sku = quote(execute_command['sku'])
        inventory = quote(execute_command['inventory'])
        url = "https://merchant.wish.com/api/v2/variant/update-inventory?access_token=%s&sku=%s&inventory=%s"%(access_token,sku,inventory)
        r = requests.post(url)
        result = r.text
        return result


    #获取所有变种产品
    #参数 start / limit      类型为integer
    def get_all_variation_product(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        start = quote(execute_command['start'])
        limit = quote(execute_command['limit'])
        url = "https://merchant.wish.com/api/v2/variant/multi-get?access_token=%s&start=%s&limit=%s"%(access_token,start,limit)
        r = requests.post(url)
        result = r.text
        return result



    #全部产品列表
    def list_product(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        limit = quote(execute_command['limit'])
        start = quote(execute_command['start'])
        url = "https://merchant.wish.com/api/v2/product/multi-get?access_token=%s&limit=%s&start=%s"%(access_token,limit,start)
        r = requests.post(url)
        result = r.text
        return result


    #从产品中移除多余的图像
    #produt_id 或者  parent_sku   两者取其一
    def remove_extra_images(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        product_id = quote(execute_command['product_id'])
        url = "https://merchant.wish.com/api/v2/product/remove-extra-images?access_token=%s&id=%s"%(access_token,product_id)
        r = requests.post(url)
        result = r.text
        return result



    #编辑产品的运输价格
    def edit_ship_price(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        product_id = quote(execute_command['product_id'])
        country = quote(execute_command['country'])
        price = quote(execute_command['price'])
        wish_express = quote(execute_command['wish_express'])
        url = "https://merchant.wish.com/api/v2/product/update-shipping?access_token=%s&id=%s&country=%s&price=%s"%(access_token,product_id,country,price)
        r = requests.post(url)
        result = r.text
        return result


    def edit_multiple_ship_price(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        product_id = quote(execute_command['product_id'])
        CA = quote(execute_command['CA'])
        AU = quote(execute_command['AU'])
        use_product_shipping_countries = quote(execute_command['use_product_shipping_countries'])
        disabled_countries = quote(execute_command['disabled_countries'])
        wish_express_countries =  quote(execute_command['wish_express_countries'])
        url = "https://merchant.wish.com/api/v2/product/update-multi-shipping?access_token=%s&id=%s&CA=%s&AU=%s&use_product_shipping_countries=%s&disabled_countries=%s&wish_express_countries=%s"%(access_token, product_id, CA, AU, use_product_shipping_countries, disabled_countries, wish_express_countries)
        r = requests.post(url)
        result = r.text
        return result


    #获取产品的航运价格
    #produt_id 或者  parent_sku   两者取其一
    def get_shipping_price(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        product_id = quote(execute_command['product_id'])
        country = quote(execute_command['country'])
        url = "https://merchant.wish.com/api/v2/product/get-shipping?access_token=%s&id=%s&country=%s"%(access_token,product_id,country)
        r = requests.post(url)
        result = r.text
        return result


    #获得产品的所有运费
    # produt_id 或者  parent_sku   两者取其一
    def get_all_shipping_price(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        product_id = quote(execute_command['product_id'])
        url = "https://merchant.wish.com/api/v2/product/get-all-shipping?access_token=%s&id=%s"%(access_token,product_id)
        r = requests.post(url)
        result = r.text
        return result


    #获得许多产品的运输价格
    #ids = 123456789009876543211234,111122223333444455556666
    def get_ship_price_many_product(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        product_ids = quote(execute_command['product_id'])
        url = "https://merchant.wish.com/api/v2/product/get-products-shipping?access_token=%s&ids=%s"%(access_token,product_ids)
        r = requests.post(url)
        result = r.text
        return result

    #获取商家航运设置
    def get_merchant_ship_setting(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        url = "https://merchant.wish.com/api/v2/product/get-shipping-setting?access_token=%s"%(access_token)
        r = requests.post(url)
        result = r.text
        return result


    #启动批量产品下载
    #since = 2016-07-01
    def batch_product_download(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        since = quote(execute_command['since'])
        url = "https://merchant.wish.com/api/v2/product/create-download-job?access_token=%s&since=%s"%(access_token,since)
        r = requests.post(url)
        result = r.text
        return result


    #获取批量产品下载的状态
    def batch_product_download_status(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        job_id = quote(execute_command['job_id'])
        url = "https://merchant.wish.com/api/v2/product/get-download-job-status?access_token=%s&job_id=%s"%(access_token,job_id)
        r = requests.post(url)
        result = r.text
        return result

    #取消批量产品下载
    def cancel_batch_product_download(execute_command):
        access_token = wish_common.get_wish_access(execute_command['store_id'])
        job_id = quote(execute_command['job_id'])
        url = "https://merchant.wish.com/api/v2/product/cancel-download-job?access_token=%s&job_id=%s" %(access_token,job_id)
        r = requests.post(url)
        result = r.text
        return result

