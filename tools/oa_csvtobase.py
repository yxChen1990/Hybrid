#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'CYX'

import aiohttp, asyncio
import json, time
import xlrd

COLUM_FAMILY = ['first_subject', 'second_subject', 'literature_title', 'abstract', 'url', 'author', 'journal_title', 'journal_volume', 'journal_number', 'year', 'doi']

#DB_HOST = '1.85.37.132'
DB_HOST = 'localhost'

async def oa_data(client, data, headers):
	r = await client.post('http://'+DB_HOST+'/api/oa/items', data=json.dumps(data), headers = headers)
	await r.release()

workbook = xlrd.open_workbook(r'oa/oa_7_1.xlsx')

sheet1_name = workbook.sheet_names()[0]
print(sheet1_name)

sheet1 = workbook.sheet_by_name(sheet1_name)
print(sheet1.name, sheet1.nrows, sheet1.ncols)

items = []
for i in range(sheet1.nrows):
	if i == 0:
		continue
	rows = sheet1.row_values(i)
	item = {}
	for j in range(len(COLUM_FAMILY)):
		column_name = COLUM_FAMILY[j]
		item[column_name] = sheet1.cell(i,j).value

	items.append(item)

data = {'items':items}
headers = {'content-type': 'application/json'}

with aiohttp.ClientSession() as client:
	tasks = [oa_data(client, data, headers)]

	asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
