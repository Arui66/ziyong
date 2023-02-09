import requests, json,re

#https://ikuuu.dev/auth/register?code=C1yx 这个是注册链接 一个免费的比较稳定的机场可以 
#https://ikuuu.dev/user登录后cookie

cookie ='lang=zh-cn; _ga=GA1.2.483709748.1672764661; uid=825633; email=757442495@qq.com; key=edeef5e50ddd8acdff7a051e0dc10dadbf62c14ba92df; ip=d0f5cb98e82d0f8c46154581032b707f; expire_in=1676527109; _gid=GA1.2.343446607.1675922312; _gat_gtag_UA_158605448_1=1'

url_info = 'https://ikuuu.dev/user/profile'
url = 'https://ikuuu.dev/user/checkin'
headers = {
    'cookie': f'{cookie}',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
html_info = requests.get(url=url_info, headers=headers).text
html = requests.post(url=url, headers=headers)
result = json.loads(html.text)['msg']
info = "".join(re.findall('<div class="d-sm-none d-lg-inline-block">(.*?)</div>', html_info, re.S))
print(info+'\n'+result)
