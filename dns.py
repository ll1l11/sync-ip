# -*- coding: utf-8 -*-
"""
创建的时候获取类似信息
'record': {'weight': None, 'status': 'enabled', 'name': '***', 'id': '***'}
"""
from datetime import datetime
import re
import logging
import requests

logging.basicConfig(filename='dnspod.log', level=logging.DEBUG)
logging.debug('this is debug info %s', datetime.now())

dnsfile = 'dnsip.txt'
newipfile = 'ip.txt'


class DNSPodClient():

    def __init__(self):
        # 由token_id,token组成
        token = '***'
        # UserAgent, 看文档: http://www.dnspod.cn/docs/info.html#specification
        ua = '***'

        self.headers = {
                'UserAgent': ua
        }

        self.pub_data = {
            'login_token': token,
            'format': 'json',
            'lang': 'cn',
            'error_on_empty': 'no',
        }
        self.record_id = '****'
        self.domain = '***'
        self.sub_domain = '***'

    def _post(self, path, data):
        url = 'https://dnsapi.cn{}'.format(path)
        data.update(self.pub_data)
        r = requests.post(url, data=data, headers=self.headers)
        return r.json()

    def record_create(self, ip):
        path = '/Record.Create'
        data = dict(
            domain=self.domain,
            sub_domain=self.sub_domain,
            record_type='A',
            record_line='默认',
            value=ip,
            ttl='600'
        )
        return self._post(path, data)

    def record_info(self):
        path = '/Record.Info'
        data = dict(
            domain=self.domain,
            record_id=self.record_id
        )
        return self._post(path, data)


    def record_modify(self, ip):
        path = '/Record.Modify'
        data = dict(
            domain=self.domain,
            record_id=self.record_id,
            sub_domain=self.sub_domain,
            record_type='A',
            record_line='默认',
            value=ip,
        )
        return self._post(path, data)


def get_file_dnsip():
    try:
        with open(dnsfile) as f:
            return f.read()
    except FileNotFoundError:
        return


def save_file_dnsip(ip):
    with open(dnsfile, 'w') as f:
        f.write(ip)


def get_api_dnsip():
    client = DNSPodClient()
    j = client.record_info()
    ip = j['record']['value']
    save_file_dnsip(ip)
    return ip

def get_new_ip():
    try:
        with open(newipfile) as f:
            s = f.read()
    except FileNotFoundError:
        return
    m = re.search('inet addr:(192.168.\d+.\d+) ', s)
    if m:
        return m.group(1)


def update_ip(new_ip, force_update=False):
    logging.info('new_ip %s', new_ip)
    old_ip = None
    from_api = False
    if not force_update:
        old_ip = get_file_dnsip()
        logging.info('通过文件获取的ip %s', old_ip)
    if not old_ip:
        old_ip = get_api_dnsip()
        from_api = True
        logging.info('通过api获取的ip %s', old_ip)
    logging.info('old ip %s', old_ip)
    print(new_ip==old_ip)
    print('${}$'.format(new_ip), '${}$'.format(old_ip))
    if new_ip == old_ip:
        logging.info('没有更改')
        return

    # 重新从api获取IP, 然后对比
    if not from_api:
        old_ip = get_api_dnsip()

    if new_ip == old_ip:
        logging.info('没有更改')
        return

    logging.info('%s -> %s', old_ip, new_ip)
    client = DNSPodClient()
    client.record_modify(new_ip)


if __name__ == '__main__':
    new_ip = get_new_ip()
    logging.info('获取到的new_ip是 %s', new_ip)
    update_ip(new_ip)
    logging.info('finish %s', datetime.now())
