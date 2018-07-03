import requests
import json

headers = {
        'User-Agent':'Data_Force_Client',
        'Accept': 'application/json',
        'Authorization': 'Bearer DqGJnSEndchjqy3af3SRwQsP0tfuWFxzWkEdZ9cckieg8QCREdjyyKTP7Bl9e',
        'Content-Type': 'application/json'
    }

# def api_test_categories():
#     url = 'https://supply.oberlo.com/supplier/api/v1/categories'
#     r = requests.get(url,headers=headers)
#     print(r.text)

def api_test_create_product():
    url = 'https://supply.oberlo.com/supplier/api/v1/products'
    values = {
    "parent_sku": "_data_force_test_4",
    "title": "this is a cute Dva!",
    "description": "a DVa for test",
    "category_id": 1,
    "option1_name": "Color",
    "option2_name": "Size",
    "main_image": "https://i.ytimg.com/vi/umq52TdCwKw/maxresdefault.jpg",
    "additional_images": [
        "https://cdna.artstation.com/p/assets/images/images/003/142/136/large/mummy-w-dva.jpg",
        "https://img00.deviantart.net/cdce/i/2016/213/1/c/dva_1_1_by_satongsti-dac95tg.jpg"
        ]
    }
    
    values = json.dumps(values)
    r = requests.post(url,values,headers=headers)
    print(r.text)

def api_test_create_product_variant():
    url='https://supply.oberlo.com/supplier/api/v1/product-variants'
    values = {
    "parent_sku": "_data_force_test_4",
    "sku": "_data_force_test_4_red",
    "price": 9.98,
    "stock": 10,
    "weight": 0.12,
    "option1": "red",
    "option2": "little",
    "published": True,
    "parent_product": {
      "title": "this is a cute Dva!",
      "category_id": 1,
      "description": "nonono...don't buy it",
      "option1_name": "Color",
      "option2_name": "Size"
    }
    }
    values = json.dumps(values)
    r = requests.post(url,values,headers=headers)
    print(r.text)


def unpublish():
    url = 'https://supply.oberlo.com/supplier/api/v1/products/_data_force_test_4/unpublish'
    r = requests.post(url,headers=headers)
    print(r.text)

api_test_create_product()

