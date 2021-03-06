#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'CYX'

import aiohttp
import asyncio
import json, time, datetime, uuid

def next_id():
	return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class MyJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		elif isinstance(obj, datetime.date):
			return obj.strftime('%Y-%m-%d')
		else:
			return json.JSONEncoder.default(self, obj)

async def log_data(client, data, headers):
	r = await client.post('http://1.85.37.132/api/logs/items', data=json.dumps(data, cls = MyJsonEncoder), headers = headers)
	
	assert r.status == 200, 'connection error!'

	res = await r.content.readany()
	item = res.decode()
	print(item)
	await r.release()


data = {'item': {'click_time': int(time.time() * 1000), 'user_id': next_id(), 'keywords': 'test', 'res_id': next_id(), 'res_type': 'paper'}}
headers = {'content-type': 'application/json'}

with aiohttp.ClientSession() as client:
	tasks = [log_data(client, data, headers)]

	asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))

	
