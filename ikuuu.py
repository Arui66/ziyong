import requests, json,re

#https://ikuuu.dev/auth/register?code=C1yx 这个是注册链接 一个免费的比较稳定的机场可以 
#https://ikuuu.dev/user登录后cookie

cookie ='lang=zh-cn; uid=825633; email=757442495@qq.com; key=5db734ec5e7153d2d461705124aa635df52be53d50d7d; ip=db373a5d20d83e860cf1ebdbf3d61d02; expire_in=1673369458; _ga=GA1.2.483709748.1672764661; _gid=GA1.2.1639946823.1672764661'

url_info = 'https://ikuuu.dev/user/profile'
url = 'https://ikuuu.dev/user/checkin'
headers = {
    'cookie': f'{cookie}',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}
html_info = requests.get(url=url_info, headers=headers).text
html = requests.post(url=url, headers=headers)
result = json.loads(html.text)['msg']
info = "".join(re.findall('<div class="d-sm-none d-lg-inline-block">(.*?)</div>', html_info, re.S))
print(info+'\n'+result)
