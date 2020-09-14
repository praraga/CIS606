import sys
import time
import re
from datetime import timedelta
from collections import defaultdict


def calculate_delta(start_time, end_time):
	if end_time > start_time:
		delta = timedelta(hours=end_time.tm_hour, minutes=end_time.tm_min) - timedelta(hours=start_time.tm_hour, minutes=start_time.tm_min)
	else:
		delta = timedelta(hours=24) - timedelta(hours=start_time.tm_hour, minutes=start_time.tm_min) + timedelta(hours=end_time.tm_hour, minutes=end_time.tm_min)
	return delta

def Log_parser(file):
		f = open(file).readlines()
		length = len(f)
		i = 0
		days = {'M': 0, 'T': 1, 'W': 2, 'Th': 3, 'F': 4, 'Sa': 5, 'Su': 6}
		"""
		To replace unicode/junk characters
		"""
		for index, val in enumerate(f):
			f[index] = f[index].encode('ASCII', 'ignore').decode().replace('\x00','')
		Excluding_dict = defaultdict(list)
		total_duration = timedelta(seconds=0)
		"""
		Calculating excluding periods to exclude in total time duration
		"""
		while not f[i].startswith('Time Log'):
			if not f[i].startswith('Excluding'):
				day, times = f[i].split(' ', 1)[0], f[i].split(' ', 1)[1]
				for t in times.split(','):
					start_time, end_time = t.split(' - ')
					Excluding_dict[days[day]].append((time.strptime(start_time.strip(), "%I:%M%p") , time.strptime(end_time.strip(), "%I:%M%p")))
			i += 1
		i += 1

		while i < length:
			line = f[i]
			line = line.strip().split('- ')
			if len(line) > 1 and line[0]:
				date_str = line[0].strip().split()
				if len(date_str) > 1:
					date = time.strptime(date_str[0].strip(':'), "%m/%d/%y")
					week_Day = date.tm_wday

				start_time = time.strptime(line[0].strip().split()[-1], "%I:%M%p")
				end_time = re.split(" |,", line[1], 1)[0]
				end_time = time.strptime(end_time, "%I:%M%p")
				deduct = timedelta(hours=0)
				Excluding_times = Excluding_dict[week_Day]
				"""
				Checking if the time duration contains excluded durations
				"""
				for s_time, e_time in Excluding_times:
					if start_time <= s_time <= e_time <= end_time:
						deduct += calculate_delta(s_time, e_time)
					elif start_time <= s_time <= end_time:
						end_time = e_time
					elif start_time <= e_time <= end_time:
						start_time = e_time 
				delta = calculate_delta(start_time, end_time) - deduct
				"""
				Adding current duration total
				"""
				total_duration += delta
			i += 1
		print("Total time spent on project {} is {}".format(file, total_duration))


if len(sys.argv) == 1:
	print("provide project name as input")
	sys.exit()
file  = sys.argv[1]
Log_parser(file)
