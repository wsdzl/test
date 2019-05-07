import re
from threading import Thread
from os.path import getsize
from time import sleep

# 读入、保存的文件名
tfname = './要处理的.txt'
sfname = './处理成功的.txt'
sfname2 = './处理失败的.txt'

# 匹配控制字符正则
re_control_char = re.compile('[\x00-\x09|\x0b-\x0c|\x0e-\x1f]')
# 匹配邮箱正则
re_email = re.compile(r'\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*')
# 匹配md5正则
re_md5 = re.compile(r'[a-fA-F0-9]{32}|[a-fA-F0-9]{16}')
# 头尾删去字符
strip = '"\'*+!%/#<.>_-?:'

# 进度监视线程函数
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
	# 启动进度监视线程
	Thread(target=status_monitor, args=(tfname, (sfname, sfname2))).start()

	# 处理每一行
	for line in f:
		# 移除控制字符
		line = re_control_char.sub('', line.strip()).lstrip(strip)
		# 分割行
		data = line.split(':')
		flag = False
		
		pass # TODO

		if flag:
			sf.write('~||`'.join(data) + '\n') # 写入处理好的行
		else:
			sferror.write(line + '\n') # 写入处理错误的行
	# 销毁进度监视进程
	completed = True