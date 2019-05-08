from threading import Thread
from os.path import getsize
from time import sleep

fname = "./NetEase(126.com&163.com).txt"
x1_sf= "./x1.txt"
x2_sf = "./x2.txt"
x3_sf = "./x3.txt"
x4_sf = "./x4.txt"
other_sf = "./other.txt"

completed = False
def status_monitor(target, save_files):
	total = '%.2fMB' % (getsize(target)/1024/1024)
	while not completed:
		completed_size = 0
		for fname in save_files:
			completed_size += getsize(fname)
		print('%.2f/%s' % (completed_size/1024/1024, total))
		sleep(1)

with open(fname, encoding="GB18030", errors ='ignore') as rf, open(x1_sf, 'w', encoding="GB18030", errors ='ignore') as x1, open(x2_sf, 'w', encoding="GB18030", errors ='ignore') as x2, open(x3_sf, 'w', encoding="GB18030", errors ='ignore') as x3, open(x4_sf, 'w', encoding="GB18030", errors ='ignore') as x4, open(other_sf, 'w', encoding="GB18030", errors ='ignore') as other:
	Thread(target=status_monitor, args=(fname, (x1_sf, x2_sf, x3_sf, x4_sf, other_sf))).start()
	mapping = {1: x1, 2: x2, 3: x3, 4: x4}
	for line in rf:
		line = line.strip()
		if not line: continue
		count_x = line.count(':')
		line += '\n'
		if count_x in mapping:
			mapping[count_x].write(line)
		else:
			other.write(line)
	completed = True
