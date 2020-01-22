import requests
import re
import os


def GetRequest(option):
	if option == 1:
		user_name = input('\n\n\t###아이디를 입력해 주세요###\n\tinput:')
	return user_name


def RequestPost(total_post):
	print("\n\t###0 입력시 모든 게시물을 불러옵니다.###")
	request_post = int(input('\t###게시물 수를 입력해 주세요###\n\tinput: '))

	overlap_value = int(input("\n\t###중복 값 제거 설정###\n\t###1을 입력하면 중복값이 제거가 됩니다.###\n\tinput : "))

	if request_post == 0 or request_post >= total_post:
		return 0, overlap_value
	else:
		return request_post, overlap_value

def SettingRaw(user_name):
	req = requests.get('https://www.instagram.com/' + user_name + '?__a=1')
	raw = req.text
	return raw


def PatExt(option, pattern, raw):
	pattern_dic = {
			'pic_pattern' : 'display_url\":\"(.*?)\"',
			'vid_pattern' : 'video_url\":\"(.*?)\"',
			'tot_pattern' : 'edge_owner_to_timeline_media\":\{\"count\":(.*?),\"',
			'endcursor_pattern' : 'end_cursor\":\"(.*?)\"',
			'ID_pattern' : 'profilePage_(.*?)\"'
			}

	pattern = pattern_dic.get(pattern)
	pat_res = re.compile(pattern)
	result = pat_res.findall(raw)

	#return to list or str
	if option == 1:
		return result
	elif option == 2:
		if result == []:
			return ['']
		return result[0]


def FileSetting(option, user_name):
	if option == 1:
		os.system('rm -rf ./File/' + user_name)
		os.system('mkdir -p ./File/' + user_name + '/picture/' + ' ./File/' + user_name + '/video/')
	elif option == 2:
		os.system('rm -rf /var/www/html/profile/' + user_name)
		os.system('cp -r ./File/' + user_name + ' /var/www/html/profile/' + user_name)
	else:
		print("error")

#async def ProfileLoop(user_ID, end_cursor):
#	req = await loop.run_in_executor(None, requests.get, 'https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={"id":"' + str(user_ID) + '","first":50,"after":"' + end_cursor[0] + '"}')
#	raw = req.text
#	pic_res += PatExt(1, 'pic_pattern', raw)        #picture crawling
#	vid_res += PatExt(1, 'vid_pattern', raw)        #video crawling
#	end_cursor = PatExt(1, 'endcursor_pattern', raw)        #get next post)
