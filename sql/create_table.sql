CREATE TABLE archive_tab_info (
  id bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  db_nick_name varchar(256) DEFAULT NULL COMMENT 'DB名称',
  source_db_server varchar(128) DEFAULT NULL COMMENT '源DB服务器',
  source_db_port int(11) DEFAULT NULL COMMENT '源DB端口',
  source_user varchar(64) DEFAULT NULL COMMENT '源DB用户名',
  source_passwd varchar(128) DEFAULT NULL COMMENT '源DB密码',
  source_schema varchar(128) DEFAULT NULL COMMENT '源DB名称',
  source_tab varchar(128) DEFAULT NULL COMMENT '源归档表名',
  source_charset varchar(16) DEFAULT NULL COMMENT '源端字符集',
  dest_db_server varchar(128) DEFAULT NULL COMMENT '目标端服务器',
  dest_db_port int(11) DEFAULT NULL COMMENT '目标端服务器端口',
  dest_user varchar(64) DEFAULT NULL COMMENT '目标端DB用户名',
  dest_passwd varchar(128) DEFAULT NULL COMMENT '目标端服务器密码',
  dest_schema varchar(128) DEFAULT NULL COMMENT '目标DB名称',
  dest_tab varchar(128) DEFAULT NULL COMMENT '目标端服务器表名',
  dest_charset varchar(16) DEFAULT NULL COMMENT '目标端字符集',
  archive_condition varchar(1024) DEFAULT NULL COMMENT '归档条件',
  is_archive int(11) DEFAULT '0' COMMENT '是否归档,1归档，0不归档',
  create_time datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  modify_time datetime DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

CREATE TABLE archive_tab_log (
  id bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  dbid bigint(20) DEFAULT NULL COMMENT 'dbid关联archive_tab_info id',
  db_nick_name varchar(128) DEFAULT NULL COMMENT '归档DB名称',
  archive_starttime datetime DEFAULT NULL COMMENT '归档开始时间',
  archive_endtime datetime DEFAULT NULL COMMENT '归档结束时间',
  archive_cmd varchar(2048) DEFAULT NULL COMMENT '归档命令内容',
  archive_status int(11) DEFAULT NULL COMMENT '归档状态,0失败1成功',
  archive_qty bigint(20) DEFAULT NULL COMMENT '归档行数',
  cost_time bigint(20) DEFAULT NULL COMMENT '花费时间秒',
  create_time datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  modify_time datetime DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
