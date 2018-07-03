文件编码统一使用utf-8，运行环境为python3.4以上，需要tornado和requests包，程序主入口为./main.py文件

项目文件夹名称为python-erp

公用方法统一添加于./common_methods/common_unit.py

数据库信息位于./common_methods/db.py

路由表内的接口方法统一位于./common_methods/http_method.py，每个路由在./main.py文件中采用一个class封装

接口名称统一使用下划线命名法，命名规则为'/平台名称_execute/方法大类'

接口主方法名称为'平台名_execute_method_方法大类'

接口类位于./平台名称/interface_方法大类.py中，一个方法大类一个文件，文件内包含共有方法和python类'class interface_方法大类'

其中该文件应用到的公共方法不需要额外使用class封装，可以直接写入公共位置，随着文件被import就直接执行入内存，网络接口直接调用的方法写入class中封装

每个方法的命名方式为平台官方提供的接口名称，即每个单词都为大写，在http_method中，应该使用eval()函数链接到对应的方法中，而不是使用if判断传入的语句

内部使用变量，函数，类，方法命名统一使用下划线命名法。

大括号换行可以使用K&R或allman，禁止出现GNU风格换行，由于python使用缩进实现逻辑，缩进统一使用四个空格，严禁使用'\t'作为缩进符号

除了main函数以外，所有函数必须存在至少一个返回值，不需要返回值的函数采用return 0作为函数正常执行的标志 