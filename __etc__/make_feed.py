#-*- coding：utf-8 -*-
import sys
import io
sys.path.append('../')
import json
from common_methods import db
# import MySQLdb as mydatabase
import pymysql as mydatabase
from common_methods import common_unit
from urllib.parse import unquote


def database_connection():
    conn = mydatabase.connect(host=db.host, port=db.port, user=db.user, passwd=db.passwd, db=db.db, charset=db.charset)
    cursor = conn.cursor()
    return cursor,conn

def get_bullet(bullet_list):
    result = ''
    for i in bullet_list:
        result +='<BulletPoint>'+i+'</BulletPoint>'
    return result
    #获得关键词

def get_search_item(search_list):
    result = ''
    for i in search_list:
        result+= '<SearchTerms>'+i+'</SearchTerms>'
    return result
    #获得搜索类别

def get_attribute(attribute_string):
    attributes = json.loads(attribute_string)

    attribute_name = attributes['option_name']
    attribute_value = attributes['option_value']

    for i in attribute_name:
        attribute_name[attribute_name.index(i)] = i[0].upper()+i[1:]

    if attribute_name != ['Size','Color']:
        attribute_name = list(reversed(attribute_name))
        attribute_value = list(reversed(attribute_value))

    theme_line = '<VariationTheme>'+'-'.join(attribute_name)+'</VariationTheme>\n'
    content_lines = ''
    for i in attribute_name:
        element = i[0].upper()+i[1:]
        content = '<'+element+'>'+attribute_value[attribute_name.index(i)].upper()+'</'+element+'>\n'
        content_lines+=content
    result = '<VariationData>\n'+theme_line+content_lines+'</VariationData>'
    return result
    # 获取商品的属性attributes

def get_time_stamp():
    time_stamp = unquote(str(common_unit.get_time_stamp()))[:17]
    time_stamp = time_stamp.split('T')
    date = time_stamp[0].split('-')
    for i in date[1:]:
        if len(i) == 1:
            date[date.index(i)] = '0'+i
    time_stamp[0] = '-'.join(date)

    c_time = time_stamp[1].split(':')
    for i in c_time:
        if len(i) == 1:
            c_time[c_time.index(i)] = '0'+i
    time_stamp[1] = ':'.join(c_time)
    time_stamp = 'T'.join(time_stamp)

    time_stamp = time_stamp[:-2]+'00+00:00'

    result = time_stamp
    return result
# def get_make_price(sku):

def get_write_category(sku):
    cursor,conn = database_connection()
    get_category_id_query = 'SELECT category_id FROM product_document WHERE sku="%s"'%sku
    cursor.execute(get_category_id_query)
    category_id = cursor.fetchall()[0][0]

    print(category_id)
    
    get_category_tree_query = 'SELECT category_name,parent_category_no,main_category_no FROM category WHERE id = "%s"'%str(category_id)
    cursor.execute(get_category_tree_query)
    category_type_tuple = cursor.fetchall()[0]
    least_category = category_type_tuple[0]

    get_parent_category_query = 'SELECT category_name FROM category WHERE category_no = "%s"'%str(category_type_tuple[1])
    cursor.execute(get_parent_category_query)
    parent_category = cursor.fetchall()[0][0]

    get_main_category_query = 'SELECT category_name FROM category WHERE category_no = "%s"'%str(category_type_tuple[2])
    cursor.execute(get_main_category_query)
    main_category = cursor.fetchall()[0][0]

    conn.close()
    return (main_category,parent_category,least_category)


def make_feed_string(execute_command):
    # execute_command = {'sku':'9500-blue-S'}

    cursor,conn = database_connection()
    sql = 'SELECT * FROM product WHERE sku = "%s"'%execute_command['sku']
    cursor.execute(sql)
    product_line = cursor.fetchall()[0]

    upper_letter = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    #attribute应该使用大写字母开头的一个单词

    product_info = {}
    attribute_string = get_attribute(product_line[38])

    product_info['sku'] = execute_command['sku']

    sql = 'SELECT * FROM dictionary WHERE id = "%s"'%product_line[12]
    cursor.execute(sql)
    product_info['standard_id_type'] = cursor.fetchall()[0][1]

    product_info['standard_id_content'] = product_line[13]

    product_info['time_stamp'] = get_time_stamp()

    sql = 'SELECT * FROM product_document WHERE sku = "%s"'%product_line[2]
    cursor.execute(sql)
    product_document = cursor.fetchall()[0]

    product_info['title'] = product_document[3]
    product_info['description'] = product_document[6]

    bullet_points = product_document[8].split(';')
    if bullet_points[-1] == '':
        bullet_points = bullet_points[:-1]
    bullet_points = get_bullet(bullet_points)

    search_item = product_document[9].split(';')
    if search_item[-1] == '':
        search_item = search_item[:-1]
    search_item = get_search_item(search_item)
    product_info['money_type'] = 'USD'

    sql = 'SELECT price FROM product WHERE sku = "%s"'%product_line[2]
    cursor.execute(sql)
    price = cursor.fetchall()[0][0]
    product_info['price'] = str(price)
    category_tuple = get_write_category(product_info['sku'])
    product_info['main_category'] = category_tuple[0].split()[0]
    product_info['parent_category'] = product_info['main_category']+'Misc'

    # print(product_info)



    feed_string = '''<?xml version="1.0" encoding="iso-8859-1"?>
    <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amznenvelope.xsd">
        <Header>
            <DocumentVersion>1.01</DocumentVersion>
            <MerchantIdentifier>DataForce</MerchantIdentifier> 
        </Header>
            <MessageType>Product</MessageType>
            <PurgeAndReplace>false</PurgeAndReplace>
        <Message>
            <MessageID>1</MessageID>
            <OperationType>Update</OperationType>
            <Product>
                <SKU>'''+product_info['sku']+'''</SKU>
                <StandardProductID>
                    <Type>'''+product_info['standard_id_type']+'''</Type>
                    <Value>'''+product_info['standard_id_content']+'''</Value>
                </StandardProductID>
                <ProductTaxCode>A GEN NOTAX</ProductTaxCode>
                <LaunchDate>'''+product_info['time_stamp']+'''</LaunchDate>
                <DescriptionData>
                    <Title>'''+product_info['title']+'''</Title>
                    <Brand>no</Brand>
                    <Description>'''+product_info['description']+'''</Description>
                    '''+bullet_points+'''
                    <MSRP currency="'''+product_info['money_type']+'''">'''+product_info['price']+product['']+'''</MSRP>
                    '''+search_item+'''
                    <IsGiftWrapAvailable>false</IsGiftWrapAvailable>
                    <IsGiftMessageAvailable>false</IsGiftMessageAvailable>
                </DescriptionData>
                <ProductData> 
                    <'''+product_info['main_category']+'''>
                        <ProductType>
                            <'''+product_info['parent_category']+'''>
                            </'''+product_info['parent_category']+'''>
                        </ProductType>
                        <Parentage>variation-parent</Parentage>
                        '''+attribute_string+'''
                        <Material>cotton</Material>
                        <ThreadCount>500</ThreadCount>
                    </'''+product_info['main_category']+'''>
                </ProductData>
            </Product>
        </Message>
    </AmazonEnvelope>
    '''
    # print(feed_string)
    conn.close()
    return feed_string

# execute_command = {'sku':'9500-blue-S'}
# feed_string = make_feed_string(execute_command)

