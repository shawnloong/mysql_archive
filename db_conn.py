#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：mysql_archive_db -> db_conn.py
@IDE    ：PyCharm
@Author ：Netdata
@Date   ：2020/5/10 19:18
@Desc   ：
=================================================='''

import pymysql
import sys
import datetime

conn = pymysql.connect(
    host="192.168.137.3",
    port=3306,
    user="netdata",
    password="netdata",
    database="ops",
    charset="utf8")