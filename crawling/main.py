import asyncio
import requests
import re
import urllib.request
import os
import time

from utils.config import *

s = time.time()

async def Profile():
	user_name = GetRequest(1)

	FileSetting(1, user_name)

	user_ID = PatExt(2, "ID_pattern", SettingRaw(user_name))
	total_post = int(PatExt(2, "tot_pattern", SettingRaw(user_name)))
	(request_post, overlap_value) = RequestPost(total_post)


	pic_res = []
	vid_res = []
	end_cursor = [""]

	if request_post == 0:
		request_post1 = int(total_post/50)
		request_post2 = int(total_post%50)
	else :
		request_post1 = int(request_post/50)
		request_post2 = int(request_post%50)

	for i in range(request_post1):
		####Get Source####
		req = await loop.run_in_executor(None, requests.get, 'https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={"id":"' + str(user_ID) + '","first":50,"after":"' + end_cursor[0] + '"}')
		raw = req.text
		pic_res += PatExt(1, 'pic_pattern', raw)  #picture crawling
		vid_res += PatExt(1, 'vid_pattern', raw)  #video crawling
		end_cursor = PatExt(1, 'endcursor_pattern', raw)  #get next post
	req = await loop.run_in_executor(None, requests.get, 'https://www.instagram.com/graphql/query/?query_hash=e769aa130647d2354c40ea6a439bfc08&variables={"id":"' + str(user_ID) + '","first":' + str(request_post2) + ',"after":"' + end_cursor[0] + '"}')
	raw = req.text
	pic_res += PatExt(1, 'pic_pattern', raw)  #picture crawling
	vid_res += PatExt(1, 'vid_pattern', raw)  #video crawling

	####File Download####
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
	print(loop)
	hashtag = GetRequest(2)
	request_post = HRequestPost()

	shortcode = await GetScode(loop, hashtag, request_post)
	print(shortcode)
	for j in range(0, len(shortcode)):
		url = 'https://www.instagram.com/p/' + shortcode[j] + '/?__a=1'
		req = await loop.run_in_executor(None, requests.get, url)
#		req = await requests.get(url)
		raw = req.text
		pic_url = PatExt(1, "pic_pattern", raw)
		vid_url = PatExt(1, "vid_pattern", raw)
		await loop.run_in_executor(None, urllib.request.urlretrieve, pic_url[0], "./File/hashtag/" + hashtag + "/picture/" + str(hashtag) + str(j + 1) + ".jpeg")
#		await urllib.request.urlretrieve(pic_url[0], "./File/" + hashtag + "/picutre/" + str(hashtag) + str(j + 1) + ".jpeg")

		if vid_url == []:
			continue
		await loop.run_in_executor(None, urllib.request.urlretrieve, vid_url[0], "./File/hashtag/" + hashtag + "/video/" + str(hashtag) + str(j + 1) + ".mp4")


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

print("Time : ", time.time()-s)
