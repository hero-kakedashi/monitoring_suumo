import mail
from bs4 import BeautifulSoup
import requests
import re
import json

past_bukken_dict = {}
bukken_json_data_path = "./data/bukken.json"

# 以前、アクセスした際の物件リストを取得
with open(bukken_json_data_path, "r", encoding="utf-8") as jsonfile:
  past_bukken_dict = json.loads(jsonfile.read())


# SUUMOから、現在の物件リストを取得
headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8,ko;q=0.7,pt;q=0.6',
}

params = (
    ('ar', '060'),
    ('bs', '040'),
    ('ra', '027'),
    ('rn', '2230'),
    ('ek', ['223014370', '223002530']),
    ('cb', '0.0'),
    ('ct', '9999999'),
    ('mb', '0'),
    ('mt', '9999999'),
    ('md', '10'),
    ('et', '10'),
    ('cn', '30'),
    ('tc', ['0400101', '0400103', '0400501', '0400301']),
    ('shkr1', '03'),
    ('shkr2', '03'),
    ('shkr3', '03'),
    ('shkr4', '03'),
    ('sngz', ''),
    ('po1', '25'),
    ('po2', '99'),
    ('pc', '100'),
)
response = requests.get('https://suumo.jp/jj/chintai/ichiran/FR301FC005/', headers=headers, params=params)
soup = BeautifulSoup(response.text, 'html.parser')
status_code = response.status_code
now_bukken_dict = {}
if status_code == 200:
  div_bukken_list = soup.find_all("div", attrs={"id":"js-bukkenList"})
  for div_bukken in div_bukken_list:
    div_bukken_detail_list = div_bukken.find_all("div", attrs={"class":['property js-property js-cassetLink', 'property property--highlight js-property js-cassetLink']})
    for bukken_detail in div_bukken_detail_list:
      name = bukken_detail.find("a", attrs={"class", "js-cassetLinkHref"}).text
      url = bukken_detail.find("a", attrs={"class", "js-cassetLinkHref"})["href"]
      tmp_dict = {}
      tmp_dict["name"] = name
      now_bukken_dict[url] = tmp_dict


# 新しく登録された物件があるかを確認
new_bukken_dict = {}
for now_url, now_data_dict in now_bukken_dict.items():
  if now_url not in past_bukken_dict:
    new_bukken_dict[now_url] = now_data_dict
#print(new_bukken_dict)


# 現在の物件リストをファイルへ保存
with open(bukken_json_data_path, 'w', encoding="utf-8") as f:
  json.dump(now_bukken_dict, f)


# 新しく登録された物件があれば、Gmailで通知
if len(new_bukken_dict) != 0:
  mail_addr = "xxxx@gmail.com"
  mail_content = ""
  mail_subject = "【確認】suumoで新しい物件を見つけました。"
  for url, new_data_dict in new_bukken_dict.items():
    bukken_url = "https://suumo.jp" + url
    #line = "url:" + bukken_url + "," + json.dumps(new_data_dict) + "\n"
    line = bukken_url + "\n"
    mail_content += line
  mail_obj = mail.Mail
  mail_obj.send("", mail_addr, mail_content, mail_subject)

print(len(now_bukken_dict))
print("finished.")
