import requests
import urllib.request
import re
import os



def pat_ext(pattern, raw):
        pat_res = re.compile(pattern)
        result = pat_res.findall(raw)
        return result


#dlwlrma user_id = 1692800026
user_name = input('ID 를 입력하세요 :')
os.system('mkdir -p ./File/' + user_name + '/picture/' + ' ./File/' + user_name + '/video/')	#For file management


user_req = requests.get('https://www.instagram.com/' + user_name + '?__a=1')
user_raw = user_req.text

pattern = 'profilePage_(.*?)\"'
user_id = pat_ext(pattern, user_raw)		#user_name to user_id

pattern = 'edge_owner_to_timeline_media\":\{\"count\":(.*?),\"'
tot_post = pat_ext(pattern, user_raw)		#total post count


print('Beginning file download...')

pic_num = 1
vid_num = 1

end_cursor = [""]
for i in range(0, int(int(tot_post[0])/50) + 1):
	print(str(i + 1) + "번째 진행 중")
	####Get Source####
	req = requests.get('https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={"id":"' + str(user_id[0]) + '","first":50,"after":"' + end_cursor[0] + '"}')
	raw = req.text


	pattern = 'display_url\":\"(.*?)\",'
	pic_res = pat_ext(pattern, raw)		#picture crawling

	pattern = 'video_url\":\"(.*?)\",'
	vid_res = pat_ext(pattern, raw) 	#video crawling

	pattern = 'end_cursor\":\"(.*?)\"'
	end_cursor = pat_ext(pattern, raw)	#get next post

	####File Download####
	for j in range(0, len(pic_res)):
		urllib.request.urlretrieve(pic_res[j], "./File/" + user_name + "/picture/" + str(user_name)  + str(pic_num + j) + ".jpeg")
	pic_num += j + 1

	for j in range(0, len(vid_res) - 1):
		urllib.request.urlretrieve(vid_res[j], "./File/" + user_name + "/video/" + str(user_name) + str(vid_num + j) + ".mp4")
	vid_num += j + 1

os.system('cp -r ./File/* /var/www/html/')	#check with the web
