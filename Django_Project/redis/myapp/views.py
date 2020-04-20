from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import time
import json

from myapp.models import Data
from myapp.models import Zdata
from myapp.singleton import Singleton
from myapp.zsingleton import Zsingleton

@csrf_exempt
def index(request):
    response = json.dumps([{}])
    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def get_value(request, key):
    if request.method == 'GET':
        try:
        	s = Singleton()
        	past = s.hash[key][1]
        	curr = int(round(time.time()*1000))
        	if past == -1 or curr < past:
        		response = json.dumps([{ 'key': key, 'value': s.hash[key][0]}])
        	else:
        		data = Data.objects.get(key=key)
        		del s.hash[key]
        		data.delete()
        		response = json.dumps([{ 'status': 'nill'}])
        except:
            response = json.dumps([{ 'status': 'nill'}])
    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def set_key(request):
    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))
        key = payload['key']
        value = payload['value']
        ttl = -1

        try:
        	s = Singleton()
        	s.hash[key][0] = value
        	s.hash[key][1] = ttl

        	data = Data.objects.get(key=key)
        	data.value = value
        	data.ttl = ttl

        	try:
        		data.save()
        		print("In this set, key found in database and updated")
        		response = json.dumps([{ 'status': 'ok'}])
        	except:
        		response = json.dumps([{ 'Error': 'data could not be added!'}])

        except:
        	data = Data(key=key, value=value, ttl=ttl)
        	try:
        		s.hash[key] = [value, ttl]
        		data.save()
        		print("In this set, key is unique")
        		response = json.dumps([{ 'status': 'ok'}])
        	except:
        		response = json.dumps([{ 'Error': 'data could not be added!'}])

    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def set_expire(request, key, ttl):
	if request.method == 'GET':
		try:
			s = Singleton()
			data = Data.objects.get(key=key)
			data.ttl = int(round(time.time()*1000)) + ttl
			s.hash[key][1] = data.ttl

			try:
				data.save()
				response = json.dumps([{'status': 'ok'}])
			except:
				response = json.dumps([{'status': 'not ok'}])
		except:
			response = json.dumps([{'status': 'not ok'}])
	return HttpResponse(response, content_type='text/json')

@csrf_exempt
def zadd_key(request):
	if request.method == 'POST':
		payload = json.loads(request.body.decode('utf-8'))
		key = payload['key']
		value = payload['value']
		score = payload['score']

		s = Singleton()
		z = Zsingleton()

		try:
			check = s.hash[key]
			response = json.dumps([{'status': 'not ok'}])
		except:
			try:
				zdata = Zdata.objects.get(key=key, value=value)
				z.sorted_hash[key].discard((zdata.score, zdata.value))
				z.reverse_sorted_hash[key].discard((zdata.value, zdata.score))

				zdata.score = score
				z.sorted_hash[key].add((zdata.score, zdata.value))
				z.sorted_hash[key].add((zdata.value, zdata.score))
				try:
					zdata.save()
					response = json.dumps([{'status': 'ok'}])
				except:
					response = json.dumps([{'status': 'not ok'}])
			except:
				zdata = Zdata(key=key, value=value, score=score)
				try:
					z.sorted_hash[key].add((score, value))
				except:
					temp = SortedList()
					temp.add((score, value))
					z.sorted_hash[key] = temp

				try:
					z.reverse_sorted_hash[key].add((value, score))
				except:
					temp = SortedList()
					temp.add((value, score))
					z.reverse_sorted_hash[key] = temp

				try:
					zdata.save()
					response = json.dumps([{'status': 'ok'}])
				except:
					response = json.dumps([{'status': 'not ok'}])
	return HttpResponse(response, content_type='text/json')

@csrf_exempt
def get_range(request, key, start, end):
	if request.method == 'GET':

		z = Zsingleton()

		try:
			response_data = {}
			for i in range(start, end):
				response_data[z.sorted_hash[key][i][1]] = z.sorted_hash[key][i][0]
			response = json.dumps(response_data)
		except:
			response = json.dumps([{'status': 'not ok'}])
	return HttpResponse(response, content_type='text/json')

@csrf_exempt
def get_zrank(request, key, value):
	if request.method == 'GET':

		z = Zsingleton()

		try:
			n = len(z.reverse_sorted_hash[key])
			l = 0
			r = n-1
			ans = -1
			while l <= r:
				mid = (l + r)//2
				if z.reverse_sorted_hash[key][mid][0] == value:
					ans = mid
					break
				elif z.reverse_sorted_hash[key][mid][0] > value:
					r = mid-1
				else:
					l = mid+1
			if ans != -1:
				score = z.reverse_sorted_hash[key][ans][1]
				print(score)
				l = 0
				r = n-1
				ans = -1
				while l <= r:
					mid = (l + r)//2
					if z.sorted_hash[key][mid][0] == score:
						if z.sorted_hash[key][mid][1] == value:
							ans = mid
							break
						elif z.sorted_hash[key][mid][1] < value:
							l = mid+1
						else:
							r = mid-1
					elif z.sorted_hash[key][mid][0] < score:
						l = mid+1
					else:
						r = mid-1
				response = json.dumps([{'rank': ans}])
			else:
				response = json.dumps([{'rank': '-1'}])
		except:
			response = json.dumps([{'rank': '-1'}])
		return HttpResponse(response, content_type='text/json')