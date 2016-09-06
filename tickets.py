#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
func: Train tickets query via command-line
Usage:
	tickets [-gdtkz] <from> <to> <date>

Options:
	-h, --help    show help menu
	-g    gaotei
	-d    dongche
	-t    tekuai
	-k    kuaishu
	-z    zhida

Example:
	tickets beijing shanghai 2016-10-01
"""

from docopt import docopt
from stations import stations
import requests
from prettytable import PrettyTable

class TrainCollection(object):
	header = 'train station time duration first second softsleep hardsleep hardsit'.split()

	def __init__(self,rows):
		self.rows = rows

	def _get_durataion(self,row):
		"""get duration time"""
		duration = row.get('lishi').replace(':','h') + 'm'
		if duration.startswith('00'):
			return duration[4:]
		if duration.startswith('0'):
			return duration[1:]
		return duration

	@property
	def trains(self):
		for row in self.rows:
			train = [
			row['station_train_code'],
			'\n'.join([row['from_station_name'],row['to_station_name']]),
			'\n'.join([row['start_time'],row['arrive_time']]),
			self._get_durataion(row),
			row['zy_num'],
			row['ze_num'],
			row['rw_num'],
			row['yw_num'],
			row['yz_num']
			]
			yield train

	def pretty_print(self):
		"""展示数据"""
		pt = PrettyTable()
		pt._set_field_names(self.header)
		for train in self.trains:
			pt.add_row(train)
		print(pt)



def cli():
	"""comman-line interface"""
	args = docopt(__doc__)
	from_station = stations.get(args['<from>'])
	to_station = stations.get(args['<to>'])
	date = args['<date>']
	url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={}&from_station={}&to_station={}'.format(date,from_station,to_station)
	r = requests.get(url, verify=False)
	rows = r.json()['data']['datas']
	trains = TrainCollection(rows)
	trains.pretty_print()
	

if __name__ == '__main__':
	cli()