#coding=utf-8
import requests
import sys
sys.path.append('../')
import common_methods.common_unit as cc
import json




def parse_file():
    xml_content = open('AutoAccessory.xsd').readlines()
    print (xml_content)


def processFile(inputFile):                                     #定义一个函数
    index = 0
    fin = open(inputFile, 'r')                                  #以读的方式打开文件
        # fout = open(outputFile, 'w')                          #以写得方式打开文件
    for eachLine in fin:                                        #读取文件的每一行
        class_type = []
        index = index + 1
        if index == 25:
            break
        try:
            line = eachLine.strip()                             #去除每行的首位空格，并且将文件编码转换成Unicode编码
            line = cc.xmltojson(str(line))
            line  = json.loads(line)
            print (line)
            # tag1 = line['xsd:element']['@ref']
            # print(tag1)
            # class_type.append(tag1)

            tag2 = line['xsd:element']['@ref']
            print (tag2)
            class_type.append(tag2)
            parent_name = 'Wireless'
            class_type.append(parent_name)
            remark = ''
            class_type.append(remark)
            print(class_type)
            cursor, conn = cc.database_connection()
            cursor.execute('INSERT INTO category_upload(category_name,parent_category,remark) values(%s,%s,%s)', class_type)
            conn.commit()
            # outStr = line                                         #我没对读入的文本进行处理，只是直接将其输出到文件
            # fout.write(outStr.strip().encode('utf-8') + '\n')     #去除首位的空格，并转回到utf-8编码，然后输出
        except:
            continue

    fin.close()                                                 #关闭文件
    # fout.close()





if __name__ == '__main__':
    processFile('./amazon_categories/Wireless.xsd')