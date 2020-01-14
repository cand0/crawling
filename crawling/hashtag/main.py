import asyncio
import requests
import re
import urllib.request
import os

hashtag = ""
end_cursor = [""]
main_url = ""
shortcode = []
total_post = 0

pic_pattern = 'display_url\":\"(.*?)\"'
vid_pattern = 'video_url\":\"(.*?)\"'
tot_pattern = 'edge_hashtag_to_media\":{\"count\":(.*?),\"'
scode_pattern = 'shortcode\":\"(.*?)\"'
endcursor_pattern = 'end_cursor\":\"(.*?)\"'


#For file management
def first_setting():
	global hashtag
	global total_post

	hashtag = input('\t hashtag 를입력하세요 : ')
	print("\n\n\t###0 입력시 모든 게시물을 다 불러옵니다.###")
	total_post = input('\n\t요청할 게시물 수를 입력해 주세요 : ')

	os.system('rm -rf ./File/' + hashtag)
	os.system('mkdir -p ./File/' + hashtag + '/picture/' + ' ./File/' + hashtag + '/video/')

	main_url_setting([], 0)

#check with the web
def last_setting():
	os.system('rm -rf /var/www/html/hashtag/' + hashtag)
	os.system('cp -r ./File/' + hashtag + ' /var/www/html/hashtag/' + hashtag)


def pat_ext(pattern, raw):
	pat_res = re.compile(pattern)
	result = pat_res.findall(raw)
	return result

def main_url_setting(end_cursor_data, post_num):
	global hashtag
	global main_url
	global end_cursor
	end_cursor = end_cursor_data

	if end_cursor == []:
		end_cursor = [""]

	main_url = 'https://www.instagram.com/graphql/query/?query_hash=90cba7a4c91000cf16207e4f3bee2fa2&variables={"tag_name":"' + hashtag + '","first":' + str(post_num) +',"after":"' + end_cursor[0] + '"}'

def tot_post():
	global main_url
	req = requests.get(main_url)
	raw = req.text
	total = pat_ext(tot_pattern, raw)
	return total[0]

async  def get_Scode():
	global hashtag
	global end_cursor
	global main_url
	global shortcode
	global total_post
	total_post = int(total_post)

	#change excess value
	tot_post_value = int(tot_post())
	if total_post > tot_post_value:
		print("\t###총 게시물 수를 초과했습니다. 모든 게시물을 불러옵니다.###")
		total_post = 0
	#/change excess value

	i = 0
	while i < total_post:
		req = await loop.run_in_executor(None, requests.get, main_url)
		raw = req.text
		shortcode += pat_ext(scode_pattern,raw)
		end_cursor = pat_ext(endcursor_pattern, raw)
		print("end_cursor, i, total_post ",end_cursor, i, total_post)
		if i + 50 > total_post:
			main_url_setting(end_cursor, total_post % 50)
		else :
			main_url_setting(end_cursor, 50)
		i += 50

	if total_post == 0:
		while True:
			req = await loop.run_in_executor(None, requests.get, main_url)
			raw = req.text
			shortcode += pat_ext(scode_pattern,raw)
			end_cursor = pat_ext(endcursor_pattern, raw)

			if end_cursor == []:
				break

	shortcode = list(set(shortcode))

async def get_File():
	global shortcode
	global hashtag

	for j in range(0, len(shortcode)):
		url = 'https://www.instagram.com/p/' + shortcode[j] + '/?__a=1'
		req = await loop.run_in_executor(None, requests.get, url)
		raw = req.text
		pic_url = pat_ext(pic_pattern, raw)
		vid_url = pat_ext(vid_pattern, raw)
		await loop.run_in_executor(None, urllib.request.urlretrieve, pic_url[0], "./File/" + hashtag + "/picture/" + str(hashtag) + str(j + 1) + ".jpeg")

		if vid_url == []:
			continue
		await loop.run_in_executor(None, urllib.request.urlretrieve, vid_url[0], "./File/" + hashtag + "/video/" + str(hashtag) + str(j + 1) + ".mp4")


async def main():

	first_setting()

	url_tasks = []
	download_tasks = []

	print("extraction url...")
	url_tasks.append(asyncio.ensure_future(get_Scode()))
	await asyncio.gather(*url_tasks)

	print("download file...")
	download_tasks.append(asyncio.ensure_future(get_File()))
	await asyncio.gather(*download_tasks)

	print("wait...")
	last_setting()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
