# coding=utf-8

# local
database_config = {
    'host': '127.0.0.1',
    'port': 5433,
    'database': 'jdcm',
    'user': 'jcr_user',
    'password': '7ujm',
    # 'charset': 'utf8',
}

database = 'jd'

jd_item_table = 'item'
analysis_item_table = 'analysis'

redis_pass = ''
redis_host = '127.0.0.1'
redis_part = '6379'
redis_db = 10

is_distributed = False

is_proxy = False
proxy_address = 'http://127.0.0.1:8000/'

email_type = 'gmail'

# gmail
if email_type == 'gmail':
    self_email = '******'
    self_password = '******'
elif email_type == 'qq':  # qq
    self_email = '******@qq.com'
    self_password = '******'
