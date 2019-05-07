import re
from threading import Thread
from os.path import getsize
from time import sleep

tfname = './x2.txt'
sfname = './x2_completed.txt'
sfname2 = './x2_error.txt'

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

with open(tfname, encoding="GB18030", errors ='ignore') as f, open(sfname, 'w', encoding="GB18030", errors ='ignore') as sf, open(sfname2, 'w', encoding="GB18030", errors ='ignore') as sferror:
	Thread(target=status_monitor, args=(tfname, (sfname, sfname2))).start()
	for line in f:
		line = re_control_char.sub('', line.strip())
		data = line.split(':')
		email = ''
		for i in range(len(data)):
			if '@' in data[i].strip('@'):
				email = data.pop(i)
				data = [data[0], email, data[1]]
				break
		if email and not ((data[0]=='' and data[1]=='') or (len(data[2]) < 4)):
			sf.write('~||`'.join(data) + '\n')
			continue
		sferror.write(line + '\n')
	completed = True