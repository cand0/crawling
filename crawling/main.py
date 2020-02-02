import asyncio
import requests
import re
import urllib.request
import os

from utils.config import *

async def Profile():
	user_name = GetRequest(1)

	FileSetting(1, user_name)

	req = requests.get('https://www.instagram.com/' + user_name + '?__a=1')
	raw = req.text

	user_ID = PatExt(2, "ID_pattern", raw)
	total_post = int(PatExt(2, "tot_pattern", raw))

	request_post = RequestPost(total_post)
	overlap_value = int(input("\n\t###중복 값 제거 설정###\n\t###1을 입력하면 중복값이 제거가 됩니다.###\n\tinput : "))

	#crawling variable setting
	pic_res = []
	vid_res = []
	end_cursor = [""]

	if request_post == 0:
		request_post1 = int(total_post/50)
		request_post2 = int(total_post%50)
	else :
		request_post1 = int(request_post/50)
		request_post2 = int(request_post%50)

	#get url
	for i in range(request_post1):
		req = await loop.run_in_executor(None, requests.get, 'https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={"id":"' + str(user_ID) + '","first":50,"after":"' + end_cursor[0] + '"}')
		raw = req.text
		pic_res += PatExt(1, 'pic_pattern', raw)  #picture crawling
		vid_res += PatExt(1, 'vid_pattern', raw)  #video crawling
		end_cursor = PatExt(1, 'endcursor_pattern', raw)  #get next post
	req = await loop.run_in_executor(None, requests.get, 'https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={"id":"' + str(user_ID) + '","first":' + str(request_post2) + ',"after":"' + end_cursor[0] + '"}')
	raw = req.text
	pic_res += PatExt(1, 'pic_pattern', raw)  #picture crawling
	vid_res += PatExt(1, 'vid_pattern', raw)  #video crawling

	#File Download
	if (overlap_value == 1):
		pic_res = list(set(pic_res))
		vid_res = list(set(vid_res))
	print("Downloading...")

	for i in range(len(pic_res)):
		await loop.run_in_executor(None, urllib.request.urlretrieve, pic_res[i], "./File/profile/" + user_name + "/picture/" + str(user_name) + str(i + 1) + ".jpeg")
	for i in range(len(vid_res)):
		await loop.run_in_executor(None, urllib.request.urlretrieve, vid_res[i], "./File/profile/" + user_name + "/video/" + str(user_name) + str(i + 1) + ".mp4")

	FileSetting(2, user_name)

async def Hashtag():
	hashtag = GetRequest(2)
	FileSetting(3, hashtag)

	#get shortcode
	shortcode = await GetScode(loop, hashtag)

	#get url
	pic_url = []
	vid_url = []
	for s_code in shortcode:
		req = await loop.run_in_executor(None, requests.get, 'https://www.instagram.com/p/' + s_code + '/?__a=1')
		raw = req.text
		pic_url += PatExt(1, "pic_pattern", raw)
		vid_url += PatExt(1, "vid_pattern", raw)

	#File Download
	for i in range(0, len(pic_url)):
		await loop.run_in_executor(None, urllib.request.urlretrieve, pic_url[i], "./File/hashtag/" + hashtag + "/picture/" + str(hashtag) + str(i + 1) + ".jpeg")
	for i in range(0, len(vid_url)):
		await loop.run_in_executor(None, urllib.request.urlretrieve, vid_url[i], "./File/hashtag/" + hashtag + "/video/" + str(hashtag) + str(i + 1) + ".mp4")

	FileSetting(4, hashtag)

async def main():

	kinds = int(input('\n\n\tprofile은 1을, \n\thashtag는 2를 입력해주세요\n\tinput:'))
	if kinds == 1:
		download_tasks = []
		download_tasks.append(asyncio.ensure_future(Profile()))
		await asyncio.gather(*download_tasks)
	elif kinds == 2:
		download_tasks = []
		download_tasks.append(asyncio.ensure_future(Hashtag()))
		await asyncio.gather(*download_tasks)
	else :
		print("\n\tError!!!")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

