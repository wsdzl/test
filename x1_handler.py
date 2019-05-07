import re
from threading import Thread
from os.path import getsize
from time import sleep

tfname = './x1.txt'
sfname = './x1_completed.txt'

re_control_char = re.compile('[\x00-\x09|\x0b-\x0c|\x0e-\x1f]')
re_email = re.compile(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')

completed = False
def status_monitor(target, save_files):
	total = '%.2fMB' % (getsize(target)/1024/1024)
	while not completed:
		completed_size = 0
		for fname in save_files:
			completed_size += getsize(fname)
		print('%.2f/%s' % (completed_size/1024/1024, total))
		sleep(1)

with open(tfname, encoding="GB18030", errors ='ignore') as f, open(sfname, 'w', encoding="GB18030", errors ='ignore') as sf:
	Thread(target=status_monitor, args=(tfname, (sfname,))).start()
	for line in f:
		line = re_control_char.sub('', line.strip())
		data = line.split(':')
		if re_email.match(data[1]): data.reverse()
		if (data[0]=='') or (data[1]=='') or (len(data[1]) < 4):
			continue
		sf.write('~||`'.join(data) + '\n')
	completed = True