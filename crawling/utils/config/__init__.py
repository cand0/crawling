import requests
import re
import os
import asyncio

def GetRequest(option):
	if option == 1:
		return input('\n\n\t###아이디를 입력해 주세요###\n\tinput:')
	elif option == 2:
		return input('\n\n\t###hashtag를 입력해 주세요###\n\tinput:')


def RequestPost(total_post):
	print("\n\t###0 입력시 모든 게시물을 불러옵니다.###")
	request_post = int(input('\t###게시물 수를 입력해 주세요###\n\tinput: '))

	if request_post == 0 or request_post >= total_post:
		print("\###모든 게시물을 불러옵니다.###")
		return 0
	else:
		return request_post

def PatExt(option, pattern, raw):
	pattern_dic = {
			'pic_pattern' : 'display_url\":\"(.*?)\"',
			'vid_pattern' : 'video_url\":\"(.*?)\"',
			'tot_pattern' : 'edge_owner_to_timeline_media\":\{\"count\":(.*?),\"',
			'hashtag_tot_pattern' : 'edge_hashtag_to_media\":{\"count\":(.*?),\"',
			'endcursor_pattern' : 'end_cursor\":\"(.*?)\"',
			'scode_pattern' : 'shortcode\":\"(.*?)\"',
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


def FileSetting(option, value):
	#profile file management
	if option == 1:
		os.system('rm -rf ./File/profile/' + value)
		os.system('mkdir -p ./File/profile/' + value + '/picture/' + ' ./File/profile/' + value + '/video/')
	elif option == 2:
		os.system('rm -rf /var/www/html/profile/' + value)
		os.system('mkdir -p /var/www/html/profile/')
		os.system('cp -r ./File/profile/' + value + ' /var/www/html/profile/')
	#hashtag file management
	elif option == 3:
		os.system('rm -rf ./File/hashtag/' + value)
		os.system('mkdir -p ./File/hashtag/' + value + '/picture/' + ' ./File/hashtag/' + value + '/video/')
	elif option == 4:
		os.system('rm -rf /var/www/html/hashtag/' + value)
		os.system('mkdir -p /var/www/html/hashtag/')
		os.system('cp -r ./File/hashtag/' + value + ' /var/www/html/hashtag/')
	else:
		print("error")

async def GetScode(loop, hashtag):
	#shortcode variable setting
	shortcode = []
	end_cursor = [""]

	url = 'https://www.instagram.com/graphql/query/?query_hash=90cba7a4c91000cf16207e4f3bee2fa2&variables={"tag_name":"' + str(hashtag) + '","first":' + '50' +',"after":"' + end_cursor[0] + '"}'
	req = requests.get(url)
	raw = req.text

	total_post = PatExt(1, "hashtag_tot_pattern", raw)
	total_post = int(total_post[0])
	request_post = RequestPost(total_post)
	overlap_value = int(input("\n\t###중복 값 제거 설정###\n\t###1을 입력하면 중복값이 제거가 됩니다.###\n\tinput : "))

	if request_post == 0:
		request_post1 = int(total_post/50)
		request_post2 = int(total_post%50)
	else :
		request_post1 = int(request_post/50)
		request_post2 = int(request_post%50)

	#get scode
	for i in range(request_post1):
		req = await loop.run_in_executor(None, requests.get, url)
		raw = req.text
		shortcode += PatExt(1, "scode_pattern", raw)
		end_cursor = PatExt(1, "endcursor_pattern", raw)
	if request_post2 != 0:
		url = 'https://www.instagram.com/graphql/query/?query_hash=90cba7a4c91000cf16207e4f3bee2fa2&variables={"tag_name":"' + str(hashtag) + '","first":' + str(request_post2) +',"after":"' + end_cursor[0] + '"}'
		req = await loop.run_in_executor(None, requests.get, url)
		raw = req.text
		shortcode += PatExt(1, "scode_pattern", raw)

	if (overlap_value == 1):
		shortcode = list(set(shortcode))
	return shortcode

