#-*- coding: utf-8 -*-

import logging
import psycopg2
import utils
import config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class SqlHelper(object):
    def __init__(self):
        print('connecting to default database ...')
        self.conn = psycopg2.connect(**config.database_config)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.conn.cursor()
        database_config = config.database_config.copy()
        database_config.update({'database':config.database})
        sql = "SELECT 1 FROM pg_database where datname='{}'".format(config.database)
        self.cursor.execute(sql)
        if len(self.cursor.fetchall())==0:
            self.create_database(config.database)

        self.conn = psycopg2.connect(**database_config)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.conn.cursor()
        self.init()

    def init(self):
        # 创建商品抓取记录表
        command = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "id SERIAL PRIMARY KEY, "  # 商品 id
            "name CHAR(200) NOT NULL,  "  # 商品名称
            "average_score numeric(2) DEFAULT NULL, "  # 综合评分星级
            "good_count numeric(7) DEFAULT NULL ,  "  # 好评数量
            "good_rate FLOAT DEFAULT NULL,  "  # 好评的比例
            "general_count numeric(4) DEFAULT NULL,  "  # 中评数量
            "general_rate FLOAT DEFAULT NULL, "  # 中评比例
            "poor_count numeric(4) DEFAULT NULL, " # 差评数量
            "poor_rate FLOAT DEFAULT NULL,  "  # 差评比例
            "after_count numeric(5) DEFAULT NULL,  "# 追评数量
            "good_rate_style numeric(7) DEFAULT NULL,"
            "poor_rate_style numeric(5) DEFAULT NULL, "
            "general_rate_style numeric(5) DEFAULT NULL,"
            "comment_count numeric(7) DEFAULT NULL,"  # 总共评论数量
            "product_id numeric(15) DEFAULT NULL,  "  # 商品 id
            "good_rate_show numeric(3) DEFAULT NULL,"  # 显示的好评百分比  
            "poor_rate_show numeric(3) DEFAULT NULL, "  # 显示的差评百分比 
            "general_rate_show numeric(7) DEFAULT NULL,"  # 显示中评的百分比
            "url TEXT NOT NULL,  "  # 网站
            "item_ids TEXT DEFAULT NULL," # 同一个商品的多个 ids
            "save_time TIMESTAMP NOT NULL"  # 抓取数据的时间
            ")".format(config.jd_item_table))
        self.create_table(command)

        # 创建分析商品评论结果表
        command = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "id SERIAL PRIMARY KEY, "  # 自增 id
            "product_id numeric(15) DEFAULT NULL ,"  # 商品 id
            "info CHAR(255) DEFAULT NULL,"  # 分析结果的信息
            "type CHAR(10) DEFAULT NULL,"  # 分析结果类型
            "guid CHAR(40) NOT NULL,"  # guid
            "save_time TIMESTAMP NOT NULL"  # 分析数据的时间
            ")".format(config.analysis_item_table))
        self.create_table(command)

    def create_database(self, database_name):
        try:
            command = 'CREATE DATABASE %s WITH ENCODING \'utf8\' ' % database_name
            # utils.log('sql helper create_database command:%s' % command)
            self.cursor.execute(command)
        except Exception as e:
            utils.log('sql helper create_database exception:%s' % str(e), logging.WARNING)

    def create_table(self, command):
        try:
            # utils.log('sql helper create_table command:%s' % command)
            self.cursor.execute(command)
            self.conn.commit()
        except Exception as e:
            utils.log('sql helper create_table exception:%s' % str(e), logging.WARNING)

    def insert_data(self, command, data, commit = False):
        try:
            # utils.log('insert_data command:%s, data:%s' % (command, data))

            self.cursor.execute(command, data)
            if commit:
                self.conn.commit()
        except Exception as e:
            utils.log('sql helper insert_data exception msg:%s' % e, logging.WARNING)

    def insert_json(self, data = {}, table_name = None, commit = False):
        try:
            keys = []
            vals = []
            for k, v in list(data.items()):
                keys.append(k)
                vals.append(v)
            val_str = ','.join(['%s'] * len(vals))
            key_str = ','.join(keys)

            command = "INSERT INTO {table} ({keys}) VALUES({values})". \
                format(keys = key_str, values = val_str, table = table_name)
            # utils.log('insert_json command:%s' % command)
            self.cursor.execute(command, tuple(vals))

            if commit:
                self.conn.commit()
        except Exception as e:
            utils.log('sql helper insert_json exception msg:%s' % e, logging.WARNING)

    def commit(self):
        self.conn.commit()

    def execute(self, command, commit = True):
        try:
            # utils.log('sql helper execute command:%s' % command)
            data = self.cursor.execute(command)
            self.conn.commit()
            return data
        except Exception as e:
            utils.log('sql helper execute exception msg:%s' % str(e))
            return None

    def is_exists(self, table_name):
        try:
            command = "select 1 from pg_tables where tablename='%s'" % table_name
            utils.log('sql helper is_exists command:%s' % command)
            data = self.cursor.execute(command)
            
            return True if data == 1 else False
        except Exception as e:
            logging.exception('sql helper is_exists exception msg:%s' % e)

    def query(self, command, commit = False, cursor_type = 'tuple'):
        try:
            utils.log('sql helper execute command:%s' % command)

            cursor = None
            if cursor_type == 'dict':
                cursor = self.conn.cursor(psycopg2.extras.DictCursor)
            else:
                cursor = self.cursor

            cursor.execute(command)
            data = cursor.fetchall()
            if commit:
                self.conn.commit()
            return data
        except Exception as e:
            utils.log('sql helper execute exception msg:%s' % str(e))
            return None

    def query_one(self, command, commit = False, cursor_type = 'tuple'):
        try:
            utils.log('sql helper execute command:%s' % command)

            cursor = None
            if cursor_type == 'dict':
                cursor = self.conn.cursor(psycopg2.extras.DictCursor)
            else:
                cursor = self.cursor

            cursor.execute(command)
            data = cursor.fetchone()
            if commit:
                self.conn.commit()
            return data
        except Exception as e:
            utils.log('sql helper execute exception msg:%s' % str(e))
            return None
