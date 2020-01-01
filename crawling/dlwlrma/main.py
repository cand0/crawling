import requests
import urllib.request
import re
import os		#For file management

#user_id = 1692800026
user_name = input('ID 를 입력하세요 :')
os.system('mkdir -p ./File/' + user_name + '/picture/' + ' ./File/' + user_name + '/video/')	#For file management


user_name_req = requests.get('https://www.instagram.com/' + user_name + '?__a=1')
user_name_raw = user_name_req.text


####user.name to user.id####
pattern = 'profilePage_(.*?)\"'
pat_res = re.compile(pattern)
user_id = pat_res.findall(user_name_raw)


####Get Source####
req = requests.get('https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={"id":"' + str(user_id[0]) + '","first":1000,"after":""}')
raw = req.text

####pciture crawling###
pattern = 'display_url\":\"(.*?)\",'
pat_res = re.compile(pattern)
picture_res = pat_res.findall(raw)

####video crawling###
pattern = 'video_url\":\"(.*?)\",'
pat_res = re.compile(pattern)
video_res = pat_res.findall(raw)


print('Beginning file download...')

for i in range(0, len(picture_res) - 1):
	urllib.request.urlretrieve(picture_res[i], "./File/" + user_name + "/picture/" + str(user_name)  + str(i + 1) + ".jpeg")
for i in range(0, len(video_res) - 1):
	urllib.request.urlretrieve(video_res[1], "./File/" + user_name + "/video/" + str(user_name) + str(i + 1) + ".mp4")

