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


###total posts###
pattern = 'edge_owner_to_timeline_media\":\{\"count\":(.*?),\"'
pat_res = re.compile(pattern)
tot_post = pat_res.findall(user_name_raw)

####Get Source####
req = requests.get('https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={"id":"' + str(user_id[0]) + '","first":1000,"after":""}')
raw = req.text


####pciture crawling###
pat_pic = 'display_url\":\"(.*?)\",'
pat_res = re.compile(pat_pic)
pic_res = pat_res.findall(raw)

####video crawling###
pat_vid = 'video_url\":\"(.*?)\",'
pat_res = re.compile(pat_vid)
vid_res = pat_res.findall(raw)


print('Beginning file download...')

pic_num = 1
vid_num = 1

end_cursor = [""]
for j in range(0, int(int(tot_post[0])/50) + 1):
	print(str(j) + "번째 진행중 \n")
	####Get Source####
	req = requests.get('https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={"id":"' + str(user_id[0]) + '","first":50,"after":"' + end_cursor[0] + '"}')
	raw = req.text

        ####pciture crawling###
	pat_pic = 'display_url\":\"(.*?)\",'
	pat_res = re.compile(pat_pic)
	pic_res = pat_res.findall(raw)

        ####video crawling###
	pat_vid = 'video_url\":\"(.*?)\",'
	pat_res = re.compile(pat_vid)
	vid_res = pat_res.findall(raw)

	pat_post = 'end_cursor\":\"(.*?)\"'
	pat_res = re.compile(pat_post)
	end_cursor = pat_res.findall(raw)

	for i in range(0, len(pic_res) - 1):
		urllib.request.urlretrieve(pic_res[i], "./File/" + user_name + "/picture/" + str(user_name)  + str(pic_num + i) + ".jpeg")
	pic_num = i

	for i in range(0, len(vid_res) - 1):
		urllib.request.urlretrieve(vid_res[1], "./File/" + user_name + "/video/" + str(user_name) + str(vid_num + i) + ".mp4")
	vid_num = i

        ####pciture crawling###
#        pat_pic = 'display_url\":\"(.*?)\",'
#        pat_res = re.compile(pat_pic)
#        pic_res = pat_res.findall(raw)
#
#        ####video crawling###
#        pat_vid = 'video_url\":\"(.*?)\",'
#        pat_res = re.compile(pat_vid)
#        vid_res = pat_res.findall(raw)


###finsish###
