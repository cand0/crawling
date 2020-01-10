import requests
import urllib.request
import re
import os
import time
pic_pattern = 'display_url\":\"(.*?)\"'
vid_pattern = 'video_url\":\"(.*?)\"'
tot_pattern = 'edge_hashtag_to_media\":{\"count\":(.*?),\"'
Scode_pattern = 'shortcode\":\"(.*?)\"'
Scode_pattern = 'shortcode\":\"(.*?)\"'
typ_pattern = 'typename\":\"(.*?)\"'

def pat_ext(pattern, raw):
        pat_res = re.compile(pattern)
        result = pat_res.findall(raw)
        return result



hashtag = input('hashtag 를입력하세요  :')
os.system('rm -rf ./File/' + hashtag)
os.system('mkdir -p ./File/' + hashtag + '/picture/' + ' ./File/' + hashtag + '/video/')	#For file management


end_cursor = [""]
URL = 'https://www.instagram.com/graphql/query/?query_hash=90cba7a4c91000cf16207e4f3bee2fa2&variables={"tag_name":"' + hashtag + '","first":50,"after":"' + end_cursor[0] + '"}'
tag_req = requests.get(URL)
tag_raw = tag_req.text
tot_post = pat_ext(tot_pattern, tag_raw)


print('Beginning extraction URL...')


pic_URL = [""]
vid_URL = [""]
start = time.time()
for i in range(0, int(int(tot_post[0])/50) + 1):
	S_code = pat_ext(Scode_pattern, tag_raw)
	for k in range(0, len(S_code)):
		S_URL =  'https://www.instagram.com/p/' + S_code[k] + '/?__a=1'
		S_req = requests.get(S_URL)
		S_raw = S_req.text
		S_type = pat_ext(typ_pattern, S_raw)
		pic_URL = pic_URL + pat_ext(pic_pattern, S_raw)
		vid_URL = vid_URL + pat_ext(vid_pattern, S_raw)
	print("Beginning extraction ULR...", i + 1, "/", int(int(tot_post[0])/50) + 1)

print("duplication delete ...")
####duplication delete####
j = 1
i = 0

olpic_num = [""]
for i in range(0, len(pic_URL) - 2):
	for j in range(i + 1, len(pic_URL)):
		if pic_URL[i] == pic_URL[j]:
			olpic_num.append(i)
			break
j = 0
for i in range(1, len(olpic_num) - 1):
	del pic_URL[olpic_num[i] - j]
	j += 1

olvid_num = [""]
for i in range(0, len(vid_URL) - 2):
	for j in range(i + 1, len(vid_URL)):
		if vid_URL[i] == vid_URL[j]:
			olvid_num.append(i)
			break

j = 0
for i in range(1, len(olvid_num) - 1):
        del vid_URL[olvid_num[i] - j]
        j += 1

####File Download####

print("Beginning file download...")
for j in range(1, len(pic_URL)):
	urllib.request.urlretrieve(pic_URL[j], "./File/" + hashtag + "/picture/" + str(hashtag)  + str(j) + ".jpeg")

for j in range(1, len(vid_URL)):
	urllib.request.urlretrieve(vid_URL[j], "./File/" + hashtag + "/video/" + str(hashtag) + str(j) + ".mp4")

os.system('rm -rf /var/www/html/hashtag/' + hashtag)
os.system('cp -r ./File/* /var/www/html/hashtag/')	#check with the web
