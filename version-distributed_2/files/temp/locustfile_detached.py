'''
Created on Sep 12, 2019

@author: Davide Rossi, Francesco Poggi
'''

from locust import HttpLocust, TaskSet, events
import threading
import atexit
#import json
import re

class LoaderBehavior(TaskSet):
#	@task
	def listAll(self):
		self.client.get("/api")

	def observation_temp(l):
		jObs = {
			"madeBySensor": "http://experiments.gauss.it/lsa/livingTemperatureSensor",
			"observedProperty": "http://experiments.gauss.it/lsa/livingTemperature_666",
			"hasFeatureOfInterest": "http://experiments.gauss.it/lsa/living_666",
			"hasSimpleResult": "22"
		}
		head = {'content-type': 'application/json'}
		#l.client.post('/api/observations', data=json.dumps(jObs), headers=head)
		l.client.post('/api/observations', json=jObs) #, headers=head)

	def observation_hum(l):
		jObs = {
			"madeBySensor": "http://experiments.gauss.it/lsa/livingHumiditySensor",
			"observedProperty": "http://experiments.gauss.it/lsa/livingHumidity_999",
			"hasFeatureOfInterest": "http://experiments.gauss.it/lsa/living_999",
			"hasSimpleResult": "68"
		}
		head = {'content-type': 'application/json'}
		#l.client.post('/api/observations', data=json.dumps(jObs), headers=head)
		l.client.post('/api/observations', json=jObs, headers=head)

	#tasks = { listAll }
	tasks = { observation_temp }

class SemanticEngineLoader(HttpLocust):
	def parseEnv(f):
		myvars = {}
		with open(f) as myfile:
			for line in myfile:
				#name, var = line.partition("=")[::2]
				#myvars[name.strip()] = float(var)
				temp = line.split('=')
				if len(temp) < 2:
					continue
				key,val = line.split('=')
				myvars[key] = re.sub(r"\s+", '', val)
		return myvars

	f = '.env'
	res = parseEnv(f)
	
	task_set = LoaderBehavior
	#host = "http://127.0.0.1:9876/engineapi"
	#host = "http://engine-cont:9876/engineapi"
	host = "http://" + str(res['ENGINE_IP_ADDR']) + ":" + str(res['ENGINE_API_PORT']) + "/engineapi"
	
	min_wait = int(res['LOCUST_MIN_WAIT'])
	max_wait = int(res['LOCUST_MAX_WAIT'])

	def __init__(self):
		super(SemanticEngineLoader, self).__init__()
#		self.fp = open("output.data", "w+", buffering=1)
#		self.fp.close()

def hook_request_success(request_type, name, response_time, response_length, **kw):
	global lck, fp
	msg = "request_type: "+str(request_type)+"\tname: "+str(name)+"\tresponse_length: "+str(response_length)+"\tresponse_time: "+str(response_time)+"\n"
	lck.acquire()
#		self.fp = open("output.data", "a", buffering=1)
	fp.write(msg)
#		self.fp.close()
#		self.fp.flush()
#	print(msg)
	lck.release()

def exit_handler():
	global fp
	fp.close

events.request_success += hook_request_success
lck = threading.Lock()
fp = open("output.data", "w+", buffering=1)
atexit.register(exit_handler)
