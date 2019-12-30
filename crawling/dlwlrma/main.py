import requests
import re
from bs4 import BeautifulSoup

#str로 형변환을 해줘야 수월하게 진행이 된다.

req = requests.get('https://www.instagram.com/dlwlrma/?__a=1')
raw = req.text

html = str(BeautifulSoup(raw, 'html.parser'))
html_res = html.replace('&amp;', '&')

pattern = 'display_url":"(.*?)\",'
pat_res = re.compile(pattern)
url_res = str(pat_res.findall(html_res))


fp = open('dlwlrma_url', 'w')
fp.write(url_res)
fp.close()
