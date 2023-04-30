#!/usr/bin/env python
# encoding: utf-8

import mysql.connector

# 连接数据库
conn = mysql.connector.connect(host='localhost', port=3306, user='root', passwd='', db='DcData')

# 获取游标
cursor = conn.cursor()

# 执行SQL查询
cursor.execute('SELECT * FROM miyun_raw_nais')

# 获取结果
results = cursor.fetchall()

print(len(results))

# 打印结果
for i in range(4):
    print(results[i][0], results[i][1], results[i][2], results[i][3])
# for row in results:
#    print(row[0], row[1])

# 关闭连接
cursor.close()
conn.close()
