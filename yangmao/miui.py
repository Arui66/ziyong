import requests, json ,time,base64,binascii,hashlib,os

# 小米签到 小米社区任务得成长值
# 配置帐号密码 一一对应 按需增删 不对上会出错 若帐号密码填写没有错误 还是报错应该是账号在非常用设备上登录, 需要验证码, 使用该设备安装图形化工具后自行前去验证https://web-alpha.vip.miui.com/page/info/mio/mio/internalTest 图形化工具怎么安装可参考https://cloud.tencent.com/developer/article/2069955
# account =['帐号1','帐号2','账号3']
# password =['密码1','密码2','密码3']
"""
cron: 57 0,9 * * *
new Env("小米社区任务得成长值");
"""
# 青龙变量 mi_account mi_password
mi_account = os.getenv("mi_account").split('&')
mi_password = os.getenv("mi_password").split('&')


# 获取cookie
def Phone(mi_account, mi_password):
    md5 = hashlib.md5()
    md5.update(mi_password.encode())
    Hash = md5.hexdigest()
    url = "https://account.xiaomi.com/pass/serviceLoginAuth2"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent":
        "Dalvik/2.1.0 (Linux; U; Android 12; 21051182C Build/SKQ1.220303.001) APP/xiaomi.vipaccount APPV/230113 MK/WGlhb21pIFBhZCA1 SDKV/5.1.0.release PassportSDK/5.1.0.release passport-ui/5.1.0.release",
        "Cookie":
        "deviceId=X0jMu7b0w-jcne-S; pass_o=2d25bb648d023d7f; sdkVersion=accountsdk-2020.01.09",
        "Host": "account.xiaomi.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    data = {
        "cc": "+86",
        "qs": "%3F_json%3Dtrue%26sid%3Dmiui_vip%26_locale%3Dzh_CN",
        "callback": "https://api.vip.miui.com/sts",
        "_json": "true",
        "user": mi_account,
        "hash": Hash.upper(),
        "sid": "miui_vip",
        "_sign": "ZJxpm3Q5cu0qDOMkKdWYRPeCwps%3D",
        "_locale": "zh_CN"
    }
    Auth = requests.post(url=url, headers=headers,
                         data=data).text.replace("&&&START&&&", "")
    Auth = json.loads(Auth)
    ssecurity = Auth["ssecurity"]
    nonce = Auth["nonce"]
    sha1 = hashlib.sha1()
    Str = "nonce=" + str(nonce) + "&" + ssecurity
    sha1.update(Str.encode("utf-8"))
    clientSign = base64.encodebytes(
        binascii.a2b_hex(sha1.hexdigest().encode("utf-8"))).decode(
            encoding="utf-8").strip()
    nurl = Auth[
        "location"] + "&_userIdNeedEncrypt=true&clientSign=" + clientSign

    sts = requests.get(url=nurl)
    return requests.utils.dict_from_cookiejar(sts.cookies)

#签到任务
for i in range(len(mi_account)):
    cookie = str(Phone(f'{mi_account[i]}', f'{mi_password[i]}')).replace('{','').replace('}','').replace(',',';').replace(': ','=').replace('\'','').replace(' ','')
    url = 'https://api.vip.miui.com/mtop/planet/vip/user/checkin'
    headers = {
        'Host': 'api.vip.miui.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; M2007J1SC Build/RKQ1.200826.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.116 Mobile Safari/537.36 XiaoMi/MiuiBrowser/15.7.22 app/vipaccount',
        'Accept': '*/*',
        'Origin': 'https://web.vip.miui.com',
        'X-Requested-With': 'com.xiaomi.vipaccount',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://web.vip.miui.com/page/info/mio/mio/checkIn?app_version=dev.220804',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': f'{cookie}'
    }
    user_url = 'https://api.vip.miui.com/api/community/user/home/page'
    html = requests.get(url=url, headers=headers)
    html_user = requests.get(url=user_url, headers=headers)
    result = json.loads(html.text)
    result_user = json.loads(html_user.text)
    userId = result_user['entity']['userId']
    print('*************'+'\n'+f'开始第{i + 1}个账号签到'+'\n'+'签到结果：')
    print('userId: '+userId + ' 用户名: '+result_user['entity']['userName']+ ' 段位: '+ result_user['entity']['userGrowLevelInfo']['showLevel'])
    print(result)
# 点赞任务
    print('开始加入点赞任务>>>>')
    for a in range(2):
        dzurl = 'https://api.vip.miui.com/mtop/planet/vip/content/announceThumbUp'
        dz_data = {
        'postId': '36625780',
        'sign': '36625780',
        'timestamp':int(round(time.time() * 1000))
        }
        dz_html = requests.get(url=dzurl, headers=headers,data=dz_data)
        dz_result = json.loads(dz_html.text)
        if dz_result['status'] == 200:
            print('点赞帖子成功成功')
        time.sleep(1)
#加入圈子
    print('开始加入圈子任务>>>>')
    unfollow_url = 'https://api.vip.miui.com/api/community/board/unfollow?boardId=558495'
    html_unfollow = requests.get(url=unfollow_url, headers=headers)
    result_unfollow = json.loads(html_user.text)
    if result_unfollow['status']==200:
        print('退出圈子成功')
    time.sleep(1)

    follow_url = 'https://api.vip.miui.com/api/community/board/follow?boardId=558495'
    html_follow = requests.get(url=follow_url, headers=headers)
    result_follow = json.loads(html_user.text)
    if result_follow['status']==200:
        print('加入圈子成功')
    time.sleep(1)

# 浏览主页
    info_url =f'https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByAction?userId={userId}&action=BROWSE_SPECIAL_PAGES_USER_HOME'
    html_info = requests.get(url=info_url, headers=headers)
    time.sleep(12)
    result_info = json.loads(html_info.text)
    if result_info['status'] == 200:
        print('浏览主页成功，获得积分： '+str(result_info['entity']['score']))
    else:
        print(result_info['message']+'，今日已达上限')
#浏览专题
    print('开始浏览专题任务>>>>')
    llzt_url = f'https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByAction?userId={userId}&action=BROWSE_SPECIAL_PAGES_SPECIAL_PAGE'
    html_llzt = requests.get(url=llzt_url, headers=headers)
    time.sleep(12)
    result_llzt = json.loads(html_llzt.text)
    # print(result_llzt)
    if result_llzt['status'] == 200:
        print('浏览主页成功，获得积分： '+str(result_llzt['entity']['score']))
    else:
        print(result_llzt['message']+'，今日已达上限')

#浏览帖子
    print('开始浏览帖子任务>>>>')
    for a in range(3):
        watch_url = f'https://api.vip.miui.com/mtop/planet/vip/member/addCommunityGrowUpPointByAction?userId={userId}&action=BROWSE_POST_10S'
        html_watch = requests.get(url=watch_url, headers=headers)
        time.sleep(12)
        result_watch = json.loads(html_watch.text)
        # print(result_watch)
        if result_watch['status'] == 200:
            print('浏览帖子成功，获得积分： ' + str(result_watch['entity']['score']))
        else:
            print(result_watch['message'] + '，今日已达上限')

    time.sleep(60)
