import multiprocessing
import sys
import psutil
import time
import json
from datetime import datetime

class SysInfo():
	"""docstring for SysInfo"""
	def __init__(self, process):
		self.cpu_p = process.cpu_percent(interval=1)
		self.rss_ = process.memory_info().rss
		self.wmz_ = process.memory_info().vms
		if sys.platform ==  'win32':
			self.handles = handles.process.num_handles()
		if sys.platform ==  'linux':
			self.fds = process.num_fds()
	def info(self):
		if sys.platform ==  'linux':
			print("""Информация о запущенном процессе:
			Загрузка cpu: {}			
			Потребление памяти:
			Resident Set Size: {}
			Virtual Memory Size: {}
			Количество открытых файловых дискрипторов: {} """.format(self.cpu_p, self.rss_, self.wmz_, self.fds))
			data = {'CPU':self.cpu_p, 'rss':self.rss_, 'wmz':self.wmz_, 'fds':self.fds}
			return data
		if sys.platform ==  'win32':
			print("""Информация о запущенном процессе:
			Загрузка cpu: {}			
			Потребление памяти:
			Working Set: {}
			Private Bytes: {}
			Количество открытых хендлов: {} """.format(self.cpu_p, self.rss_, self.wmz_, self.handles))
			data = {'CPU':self.cpu_p, 'Working Set':self.rss_, 'Private Bytes':self.wmz_, 'handles':self.handles}
			return data


def f1():
	pname = multiprocessing.current_process().name
	print('Запуск процесса %s...' % pname)
	# print(multiprocessing.current_process().pid)
	process = psutil.Process(multiprocessing.current_process().pid)
	with open('data-{}.json'.format(datetime.now().strftime("%Y-%m-%d-%H.%M.%S")), 'a', encoding='utf-8') as f:
		def timer_f():
			timer = time.time()
			while True:
				if time.time() - timer > int(sys.argv[1]):
					return
				s = SysInfo(process)
				data = s.info()
				json.dump(data, f, ensure_ascii=False, indent=4)
		timer_f()

if __name__ == '__main__':
	p1 = multiprocessing.Process(name='Процесс 1', target=f1)
	p1.start()
	p1.join()