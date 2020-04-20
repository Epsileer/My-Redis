from sortedcontainers import SortedList
from myapp.models import Zdata

class Zsingleton(object):
	_instance = None
	def __new__(self):
		if not self._instance:
			self._instance = super(Zsingleton, self).__new__(self)
			self.sorted_hash = dict()
			self.reverse_sorted_hash = dict()
			for i in Zdata.objects.raw('select * from myapp_zdata'):
				try:
					self.sorted_hash[i.key].add((i.score, i.value))
				except:
					temp = SortedList()
					temp.add((i.score, i.value))
					self.sorted_hash[i.key] = temp
				try:
					self.reverse_sorted_hash[i.key].add((i.value, i.score))
				except:
					temp = SortedList()
					temp.add((i.value, i.score))
					self.reverse_sorted_hash[i.key] = temp
		return self._instance