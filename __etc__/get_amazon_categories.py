import requests
import sys
sys.path.append('../')
from urllib.parse import quote
import time
from common_methods import common_unit
import json

# cate_url_list = open('amazon_categories/amazon_category_tree.txt').readlines()

# def get_content(cate_url):
#     r = requests.get(cate_url)
#     result = r.content.decode('utf-8')
#     open('amazon_categories/'+cate_url.split('/')[-1].strip(),'w').write(result)

# for i in cate_url_list:
#     get_content(i)


def get_product_type_from_xml_content(file_name):
    xml_content = open('amazon_categories/'+file_name).read()
    result = common_unit.xmltojson(xml_content)
    result = json.loads(result)
    # print(result)
    
    # choice_list = xml_content.split('<xsd:element name="ProductType">')[1]
    # choice_list = choice_list.split('</xsd:element>')[1:]

    # choice_list = '\n'.join(choice_list)
    # # for i in choice_list:
    # #     print(i)
    # choice_list = choice_list.split('</xsd:sequence>')[0]
    # print(choice_list)
    # semi_type_list = choice_list.split('\n')
    # for i in semi_type_list:
    #     semi_type = i.strip().split()
    #     if len(semi_type) == 0:
    #         pass
    #     else:
    #         semi_type = semi_type[1][5:-3]
    # #     # .split()[1][5:-3]
    result = result['xsd:schema']['xsd:element']


        
    for key in result[1:]:
        print(key['@name'])
        print(key)
        exit()
        
        for i in key['xsd:complexType']['xsd:sequence']['xsd:element']:
           
            
            print(i['@name'])
            print(i['xsd:complexType']['xsd:sequence']['xsd:element'])
            try:
                for j in i['xsd:complexType']['xsd:sequence']['xsd:element']:
                    print(j['@name'])
                    value_list = j['xsd:simpleType']['xsd:restriction']['xsd:enumeration']
                    for z in value_list:
                        print(z['@value'])
            except:
                try:
                    for j in i['xsd:simpleType']['xsd:sequence']['xsd:element']:
                        print(j['@name'])
                        value_list = j['xsd:simpleType']['xsd:restriction']['xsd:enumeration']
                        for z in value_list:
                            print(z['@value'])
                except:
                    pass
            
            try:
                print(i['xsd:simpleType'])
            except:
                pass
            print('\n')
       
        
        print('===================')
        

        # print('\n')
    # print(result)

xsd_list = open('amazon_categories/amazon_category_tree.txt').readlines()

xsd_file_list = []
for i in xsd_list:
    xsd_file_name = i.split('/')[-1].strip()
    xsd_file_list.append(xsd_file_name)



# print(xsd_file_list)
# for file_name in xsd_file_list:
#     # try:
#     get_product_type_from_xml_content(file_name)
#     break
#     # except:
#         # print(file_name)
result = get_product_type_from_xml_content(xsd_file_list[0])

print(type(result))







