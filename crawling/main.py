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
		await loop.run_in_executor(None, urllib.request.urlretrieve, pic_res[i], "./File/" + user_name + "/picture/" + str(user_name) + str(i + 1) + ".jpeg")
	for i in range(len(vid_res)):
		await loop.run_in_executor(None, urllib.request.urlretrieve, vid_res[i], "./File/" + user_name + "/video/" + str(user_name) + str(i + 1) + ".mp4")

	FileSetting(2, user_name)


async def main():
	download_tasks = []
	download_tasks.append(asyncio.ensure_future(Profile()))
	await asyncio.gather(*download_tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

print("Time : ", time.time()-s)
