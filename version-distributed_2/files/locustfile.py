'''
Created on Sep 12, 2019

@author: Davide Rossi, Francesco Poggi
'''

from locust import HttpLocust, TaskSet, events
from locust.wait_time import between, constant, constant_pacing
from locust.contrib.fasthttp import FastHttpLocust
import threading
import atexit
import json
import re

class LoaderBehavior(TaskSet):
#	@task
	def listAll(self):
		self.client.get("/api")

	def observation_temp(self):
		jObs = {
			"madeBySensor": "http://experiments.gauss.it/lsa/livingTemperatureSensor",
			"observedProperty": "http://experiments.gauss.it/lsa/livingTemperature/pipppero",
			"hasFeatureOfInterest": "http://experiments.gauss.it/lsa/living",
			"hasSimpleResult": "22"
		}
		head = {'content-type': 'application/json'}
		self.client.request('POST', '/api/observations', data=json.dumps(jObs), headers=head)

	def observation_hum(self):
		jObs = {
			"madeBySensor": "http://experiments.gauss.it/lsa/livingHumiditySensor",
			"observedProperty": "http://experiments.gauss.it/lsa/livingHumidity",
			"hasFeatureOfInterest": "http://experiments.gauss.it/lsa/living",
			"hasSimpleResult": "68"
		}
		head = {'content-type': 'application/json'}
		self.client.request('POST', '/api/observations', data=json.dumps(jObs), headers=head)

	def observation_twice(self):
		jObs = {
			"madeBySensor": "http://experiments.gauss.it/lsa/testOnceSensor",
			"observedProperty": "http://experiments.gauss.it/lsa/testOnce",
			"hasFeatureOfInterest": "http://experiments.gauss.it/lsa/test",
			"hasSimpleResult": "11"
		}
		head = {'content-type': 'application/json'}
		self.client.request('POST', '/api/observations', data=json.dumps(jObs), headers=head)

	def observation_dummy(self):
		jObs = {
			"madeBySensor": "http://experiments.gauss.it/lsa/dummySensor",
			"observedProperty": "http://experiments.gauss.it/lsa/dummy",
			"hasFeatureOfInterest": "http://experiments.gauss.it/lsa/dummy",
			"hasSimpleResult": "42"
		}
		head = {'content-type': 'application/json'}
		self.client.request('POST', '/api/observations', data=json.dumps(jObs), headers=head)

#		self.client.post('/api/observations', json=jObs) #, headers=head)
#		self.client.request('POST', '/api/observations', data=json.dumps(jObs), headers=head)
#		print("Hello")
#		try:
#			response = self.client.request('POST', '/api/observations', data=json.dumps(jObs), headers=head)
#			print("Response: "+str(response.status_code))
#		except Exception as e:
#			print(e)
#		self.client.post('/api/observations', json.dumps(jObs))

	def wait_if_needed(self):
		if('LOCUST_RPS' in self.locust.res):
			self.rps_sleep(float(self.locust.res['LOCUST_RPS']))

#	tasks = { listAll }
#	tasks = { observation_temp, observation_hum }
	tasks = { observation_dummy }

class SemanticEngineLocust(FastHttpLocust):
	def parseEnv(f):
		myvars = {}
		with open(f) as myfile:
			for line in myfile:
				temp = line.split('=')
				if len(temp) < 2:
					continue
				key,val = line.split('=')
				myvars[key] = re.sub(r"\s+", '', val)
		return myvars

	f = '.env'
	res = parseEnv(f)
	
	task_set = LoaderBehavior
	host = "http://" + str(res['ENGINE_IP_ADDR']) + ":" + str(res['ENGINE_API_PORT']) + "/engineapi"
	
	if('LOCUST_PACING' in res):
		print("Running at pace: "+res['LOCUST_PACING'])
		wait_time = constant_pacing(int(res['LOCUST_PACING']))
	else:
		wait_time = between(int(res['LOCUST_MIN_WAIT']), int(res['LOCUST_MAX_WAIT']))

	def __init__(self):
		super(SemanticEngineLocust, self).__init__()

#def hook_request_success(request_type, name, response_time, response_length, **kw):
#	global lck, fp
#	msg = "request_type: "+str(request_type)+"\tname: "+str(name)+"\tresponse_length: "+str(response_length)+"\tresponse_time: "+str(response_time)+"\n"
#	lck.acquire()
#	fp.write(msg)
#	lck.release()

#def exit_handler():
#	global fp
#	fp.close

#events.request_success += hook_request_success
#lck = threading.Lock()
#fp = open("output.data", "w+", buffering=1)
#atexit.register(exit_handler)
