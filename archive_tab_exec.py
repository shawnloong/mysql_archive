#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：mysql_archive_db -> archive_tab_exec
@IDE    ：PyCharm
@Author ：Netdata
@Date   ：2020/5/10 22:02
@Desc   ：
=================================================='''
import sys
import os
import time
import db_conn
import subprocess
from subprocess import Popen
import datetime

db = db_conn.conn
cursor = db.cursor()

try:
    sql = "SELECT id,db_nick_name,source_db_server,source_db_port,source_user,source_passwd,source_schema, \
source_tab,source_charset,dest_db_server,dest_db_port,dest_user,dest_passwd,dest_schema,dest_tab,dest_charset, \
archive_condition,is_archive FROM ops.archive_tab_info  where is_archive=1"

    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        v_id = row[0]
        v_nick_name = row[1]
        v_source_db_server = row[2]
        v_source_db_port = row[3]
        v_source_user = row[4]
        v_source_passwd = row[5]
        v_source_schema = row[6]
        v_source_tab = row[7]
        v_source_charset = row[8]
        v_dest_db_server = row[9]
        v_dest_db_port = row[10]
        v_dest_user = row[11]
        v_dest_passwd = row[12]
        v_dest_schema = row[13]
        v_dest_tab = row[14]
        v_dest_charset = row[15]
        v_archive_condition = row[16]
        v_is_archive = row[17]

        archive_cmd_utf8mb4 = "pt-archiver " \
                      "--source h='%s',P='%s',u='%s',p='%s',D='%s',t='%s',A=utf8mb4 " \
                      "--dest h='%s',P='%s',u='%s',p='%s',D='%s',t='%s',A=utf8mb4 " \
                      "--where '%s' --progress 5000 --limit 1000 --txn-size 1000 " \
                      "--statistics --purge " % \
                      (v_source_db_server, v_source_db_port, v_source_user, v_source_passwd, v_source_schema,v_source_tab, \
                       v_dest_db_server, v_source_db_port, v_dest_user, v_dest_passwd, v_dest_schema, v_dest_tab, \
                       v_archive_condition)

        archive_cmd_utf8 = "pt-archiver " \
                      "--source h='%s',P='%s',u='%s',p='%s',D='%s',t='%s' " \
                      "--dest h='%s',P='%s',u='%s',p='%s',D='%s',t='%s' " \
                      "--charset=UTF8 --where '%s' --progress 5000 --limit 1000 --txn-size 1000 --bulk-insert --bulk-delete " \
                      "--statistics --purge " % \
                      (v_source_db_server, v_source_db_port, v_source_user, v_source_passwd, v_source_schema,v_source_tab, \
                       v_dest_db_server, v_source_db_port, v_dest_user, v_dest_passwd, v_dest_schema, v_dest_tab, \
                       v_archive_condition)
        print(archive_cmd_utf8mb4)
        log_file_name = "./logs/db_archive_%s_%s.log" % (v_source_db_server, v_source_tab)
        myoutput = open(log_file_name,'w+')
        
        #判断字符集
        if v_source_charset == 'utf8mb4':
            archive_starttime = datetime.datetime.now()
            p = subprocess.Popen(archive_cmd_utf8mb4, shell=True, stdout=myoutput, stderr=myoutput, universal_newlines=True)
            output, errors = p.communicate()
            with open(log_file_name,"r") as f:
                print(f.read())
            archive_endtime = datetime.datetime.now()
            #计算时间   
            print(archive_starttime,archive_endtime)
            v_cost_time = (archive_starttime - archive_endtime).seconds
 
            inserted_qty = 0
            deleted_qty = 0
            with open(log_file_name,"r") as f:
                for line in f:
                    if 'INSERT' in line:
                        i = line.index(" ")
                        inserted_qty = line[i+1:]
                    elif 'DELETE' in line:
                        i = line.index(" ")
                        deleted_qty = line[i+1:]

                if inserted_qty == deleted_qty:
                    archive_status = 1
                else:
                    archive_status = 0

              #记录log
            sql_insert = "insert into archive_tab_log(dbid, db_nick_name, archive_starttime, archive_endtime, " \
                     "archive_cmd, archive_status, archive_qty, cost_time ) " \
                     "values('%s','%s','%s','%s','%s','%s','%s','%s')" % \
                     (v_id, v_nick_name, archive_starttime, archive_endtime, \
                        db.escape_string(archive_cmd_utf8mb4), archive_status, inserted_qty, v_cost_time)
            #print(sql_insert)
            cursor.execute(sql_insert)
            # exec commit
            db.commit()            

        elif v_source_charset == 'utf8':
            archive_starttime = datetime.datetime.now()
            p = subprocess.Popen(archive_cmd_utf8, shell=True, stdout=myoutput, stderr=myoutput, universal_newlines=True)
            output, errors = p.communicate()
            with open(log_file_name,"r") as f:               
                print(f.read())
            archive_endtime = datetime.datetime.now()
            v_cost_time = (archive_starttime - archive_endtime).seconds

            inserted_qty = 0
            deleted_qty = 0
            with open(log_file_name,"r") as f:
                for line in f:
                    if 'INSERT' in line:
                        i = line.index(" ")
                        inserted_qty = line[i+1:]
                    elif 'DELETE' in line:
                        i = line.index(" ")
                        deleted_qty = line[i+1:]

                if inserted_qty == deleted_qty:
                    archive_status = 1
                else:
                    archive_status = 0

              #记录log
            sql_insert = "insert into archive_tab_log(dbid, db_nick_name, archive_starttime, archive_endtime, " \
                     "archive_cmd, archive_status, archive_qty, cost_time ) " \
                     "values('%s','%s','%s','%s','%s','%s','%s','%s')" % \
                     (v_id, v_nick_name, archive_starttime, archive_endtime, \
                        db.escape_string(archive_cmd_utf8), archive_status, inserted_qty, v_cost_time)
            cursor.execute(sql_insert)
            # exec commit
            db.commit()

        else:
            print("charset is error!!!!")

except Exception as e:
    raise e
finally:
    db.close()
