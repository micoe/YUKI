# -*- coding:utf-8 -*-
import requests,json,time,re,os

folder = os.environ["FOLDER"]
token = os.environ["TOKEN"]
phone = os.environ["USERNAME"]
passWord = os.environ["PASSWORD"]

def allow():
    al = requests.get(folder, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0','Referer': 'https://wwa.lanzoui.com/b05mqj0fi'}).text
    if re.search(r'<title>\d</title>',al).group()[7] == '1':return True
    else:return False

def login():
    global s
    s = requests.session()
    data = {"userName": phone,"passWord": passWord,"uatoken": 'byyaohuoid34976'}
    s.post('https://yukizq.com/api/yuki/login', headers={'Content-Type': 'application/json'},data=json.dumps(data))
    print('登陆成功')

def status():
    st = s.post('https://www.yukizq.com/api/yuki/is_task')
    stu=st.json()['data']
    print(stu['message'])
    return stu['status']

def receive():
    re = s.post('https://www.yukizq.com/api/yuki/receive_task', data='{"isyp":"true","ismsg":"false","isretry":"false"}')
    print(re.json()['data']['message'])

def query():
    qu = s.post('https://www.yukizq.com/api/yuki/query_receive_task')
    print(qu.json()['data']['message'])
    if 'istask' in qu.text:return True
    else:return False

def send():
    q = s.post('https://www.yukizq.com/api/yuki/query_task_1')
    a = q.json()['data']['data']
    if a:
        requests.post('http://pushplus.hxtrip.com/send', data=json.dumps({"token": token, "title": 'YUKI接到单了，点击查看详情',"content": {'接单时间': t(a['createDate']),'开始时间': t(a['pickDate']),'接单账号': a['tbCode'],'商品主图': '<img src="' + a['picture'] + '" alt="商品主图" width="100%"/>','关键词': a['keyWord'],'价格': str(a['goodprice']),'任务说明': a['remark']},"template": "json"}),headers={'Content-Type': 'application/json'})
        s.post('https://yukizq.com/api/yuki/oktaskremark', headers={'Content-Type': 'application/json'},data=json.dumps({"taskId":a['taskId']}))


def main_handler(event, context):
    if allow():
        login()
        while status():
            receive()
            while query():
                time.sleep(3)
        send()

if __name__ == '__main__':
    main_handler("", "")
