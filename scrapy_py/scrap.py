import requests
from bs4 import BeautifulSoup
import base64

cookies = {
    '_ga': 'GA1.1.1121920274.1698583208',
    '__gads': 'ID=0d97e58039c034bf:T=1700914167:RT=1700983459:S=ALNI_MbqtWlLK4KMWay5sp5N_W540r8JRw',
    '__gpi': 'UID=00000cdb4f0556c7:T=1700914167:RT=1700983459:S=ALNI_MZifS602oT1AgP8aWYHKX2Y6UAbCQ',
    'fp': '9a101a91e779f045efea1f7a1606e76d',
    '_ga_FS4ESHM7K5': 'GS1.1.1701697825.9.1.1701698679.0.0.0',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': '_ga=GA1.1.1121920274.1698583208; __gads=ID=0d97e58039c034bf:T=1700914167:RT=1700983459:S=ALNI_MbqtWlLK4KMWay5sp5N_W540r8JRw; __gpi=UID=00000cdb4f0556c7:T=1700914167:RT=1700983459:S=ALNI_MZifS602oT1AgP8aWYHKX2Y6UAbCQ; fp=9a101a91e779f045efea1f7a1606e76d; _ga_FS4ESHM7K5=GS1.1.1701697825.9.1.1701698679.0.0.0',
    'Referer': 'http://free-proxy.cz/ru/proxylist/country/AU/http/ping/all',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0',
}

response = requests.get(
    'http://free-proxy.cz/ru/proxylist/country/all/all/ping/all',
    cookies=cookies,
    headers=headers,
    verify=False,
)

#with open('proxy1.html', 'w', encoding='utf-8') as file:
#    file.write(response.text)

#with open('proxy.html', 'r', encoding='utf-8') as file:
#    f = file.read()

inp = input(f'[INPUT] Введите страну: ')
protocol_inp = input(f'[INPUT] Введите протокол [all\http\htpps\socks\socks4\socks5\]: ')

lst_country = {}

soup = BeautifulSoup(response.text, 'lxml')
all_country = soup.find_all('select', id="frmsearchFilter-country")
pages = soup.find('div', class_="paginator").find_all('a')
#for page in pages[-2]:
#    res_page = page.text
#    print(res_page)

country = [i for i in all_country]

for c in country:
    res_c = c.find_all('option')[1:]
    for x in res_c:
        text_country = x.text.capitalize().split('(')[0].strip()
        two_country = x.get('value').strip()

        lst_country[text_country] = two_country
#print(lst_country)

for k,v in lst_country.items():
    if inp in k:
        for page in range(1, 6):
            try:
                resp = requests.get(url=f'http://free-proxy.cz/ru/proxylist/country/{v}/{protocol_inp}/ping/all/{page}', cookies=cookies, headers=headers)
                soup2 = BeautifulSoup(resp.text, 'lxml')
                prox = soup2.find('table', id="proxy_list").find_all('tr')
                for p in prox:
                    port = p.find_all('span', class_="fport")
                    for pp in port:
                        res_pp = pp.text
                    res = p.find_all('script', type="text/javascript")
                    for l in res:
                        res_l = l.text.split('"')
                        res_base64 = base64.b64decode(res_l[1]).decode("ascii")
                        print(f'{res_base64}:{res_pp}')
            except AttributeError as e:
                print('[INFO] Page not found!!!')

# for k,v in lst_country.items():
#     if inp in k:
#         resp = requests.get(url=f'http://free-proxy.cz/ru/proxylist/country/{v}/all/ping/all', cookies=cookies, headers=headers)
#         soup2 = BeautifulSoup(f, 'lxml')
#         prox = soup2.find('table', id="proxy_list").find_all('script')
#         port = soup2.find('table', id="proxy_list").text
#         for p in prox:
#             res = p.text.split('"')#.find('script', type="text/javascript") Австралия
#             if res[0] == 'document.write(Base64.decode(':
#                 res_base64 = base64.b64decode(res[1]).decode("ascii")
#                 print(f'{res_base64}:{port}')