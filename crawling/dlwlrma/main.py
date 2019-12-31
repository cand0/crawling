import requests
import urllib.request
import re
from bs4 import BeautifulSoup

req = requests.get('https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={"id":"1692800026","first":1000,"after":"QVFCaVBhUGtHNDI5XzRBMlczeHh1TVBZVHRqS2hBUkpDazJjanBna1IybHd0N2pJUXNwdWN0UmZCNktNTmRoSUktNFBmYmlwVGZuOUZzci1tRFNNd2NZUA=="}')
raw = req.text

html = str(BeautifulSoup(raw, 'html.parser'))	#str로 형변환을 해줘야 수월하게 진행이 된다.
html_res = html.replace('&amp;', '&')

pattern = 'display_url":"(.*?)\",'
pat_res = re.compile(pattern)
url_res = pat_res.findall(html_res)

print('Beginning file download...')

for i in range(1, 300):
	urllib.request.urlretrieve(url_res[i], "./imagefile/test" + str(i) + ".png")


#fp = open('dlwlrma_url', 'w')
#fp.write(str(url_res))
#fp.close()
