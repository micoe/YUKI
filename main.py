import requests,datetime,json,time,re,os

def allow():
    all = requests.get(os.environ["FOLDER"], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0','Referer': 'https://www.lanzous.com/b0ejh22pa', }).text
    if re.search(r'<title>\d</title>',all).group()[7] == '1':return True
    else:return False

def login():
    data = {"userName": os.environ["USERNAME"],"passWord": os.environ["PASSWORD"],"uatoken": 'byyaohuoid34976'}
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
    time.sleep(3)
    if 'istask' in qu.text:return True
    else:return False

def send():
    q = s.post('https://www.yukizq.com/api/yuki/query_task_1')
    a = q.json()['data']['data']
    print(a)
    if a:
        requests.get('https://sc.ftqq.com/' + os.environ["SCKEY"] + '.send?text=YUKI接到单了点击查看&desp=' + a['createDate'] + '\n\n' + a['pickDate'] + '\n\n' + a['goodprice'] + '\n\n' + a['keyWord'] + '\n\n' + a['remark'] + '\n\n![logo](' + a['picture'] + ')')
        s.post('https://yukizq.com/api/yuki/oktaskremark', headers={'Content-Type': 'application/json'},data=json.dumps({"taskId":a['taskId']}))


def main_handler(event, context):
    wait_until = datetime.datetime.now() + datetime.timedelta(hours=0.24)
    global break_loop,s
    s = requests.session()
    break_loop = False
    if allow():
        login()
        while not break_loop and status():
            receive()
            while not break_loop and query():
                if wait_until < datetime.datetime.now():
                    break_loop = True
        send()

if __name__ == '__main__':
    main_handler("", "")
