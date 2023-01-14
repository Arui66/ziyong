import requests, json,re

#https://ikuuu.dev/auth/register?code=C1yx 这个是注册链接 一个免费的比较稳定的机场可以 
#https://ikuuu.dev/user登录后cookie

cookie ='lang=zh-cn; _ga=GA1.2.483709748.1672764661; uid=825633; email=757442495@qq.com; key=d23a1fa51e2d14659477c3025199111c6e98c8bb19c8e; ip=ac9e41b0763aed7ebc5a19e4f0955d3e; expire_in=1674312510'

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
