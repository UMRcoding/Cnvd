import requests
import re
import execjs
import hashlib
import json
from requests.utils import add_dict_to_cookiejar
# 反爬虫机制的绕过
"""
通过加密对比得到正确cookie参数
:param data: 参数
:return: 返回正确cookie参数
"""
def getCookie(data):
    chars = len(data['chars'])
    for i in range(chars):
        for j in range(chars):
            clearance = data['bts'][0] + data['chars'][i] + data['chars'][j] + data['bts'][1]
            encrypt = None
            if data['ha'] == 'md5':
                encrypt = hashlib.md5()
            elif data['ha'] == 'sha1':
                encrypt = hashlib.sha1()
            elif data['ha'] == 'sha256':
                encrypt = hashlib.sha256()
            encrypt.update(clearance.encode())
            result = encrypt.hexdigest()
            if result == data['ct']:
                return clearance

url = 'https://www.cnvd.org.cn/flaw/list.htm'
header = {
    'User-Agent': 'User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
}

# 使用session保持会话
session = requests.session()
res1 = session.get(url, headers=header)
jsl_clearance_s = re.findall(r'cookie=(.*?);location', res1.text)[0]


# 执行js代码
jsl_clearance_s = str(execjs.eval(jsl_clearance_s)).split('=')[1].split(';')[0]

# add_dict_to_cookiejar方法添加cookie
add_dict_to_cookiejar(session.cookies, {'__jsl_clearance_s': jsl_clearance_s})
res2 = session.get(url, headers=header)

# 提取go方法中的参数
data = json.loads(re.findall(r';go\((.*?)\)', res2.text)[0])
jsl_clearance_s = getCookie(data)

# 修改cookie
add_dict_to_cookiejar(session.cookies, {'__jsl_clearance_s': jsl_clearance_s})
res3 = session.get("https://www.cnvd.org.cn/", headers=header)



