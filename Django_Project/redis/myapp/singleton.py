from myapp.models import Data

class Singleton(object):
   _instance = None
   def __new__(self):
      if not self._instance:
         self._instance = super(Singleton, self).__new__(self)
         self.hash = dict()
         for i in Data.objects.raw('select * from myapp_data'):
            self.hash[i.key] = [i.value, i.ttl]
         print('initialized hash')
      return self._instance