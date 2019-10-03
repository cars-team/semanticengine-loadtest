'''
Created on Sep 12, 2019

@author: Davide Rossi, Francesco Poggi
'''

from locust import HttpLocust, TaskSet, events
import threading
import atexit
#import json

class LoaderBehavior(TaskSet):
#	@task
	def listAll(self):
		self.client.get("/api")

	def observation_temp(l):
		jObs = {
			"madeBySensor": "http://experiments.gauss.it/lsa/livingTemperatureSensor",
			"observedProperty": "http://experiments.gauss.it/lsa/livingTemperature",
			"hasFeatureOfInterest": "http://experiments.gauss.it/lsa/living",
			"hasSimpleResult": "22"
		}
		head = {'content-type': 'application/json'}
		#l.client.post('/api/observations', data=json.dumps(jObs), headers=head)
		l.client.post('/api/observations', json=jObs) #, headers=head)

	def observation_hum(l):
		jObs = {
			"madeBySensor": "http://experiments.gauss.it/lsa/livingHumiditySensor",
			"observedProperty": "http://experiments.gauss.it/lsa/livingHumidity",
			"hasFeatureOfInterest": "http://experiments.gauss.it/lsa/living",
			"hasSimpleResult": "68"
		}
		head = {'content-type': 'application/json'}
		#l.client.post('/api/observations', data=json.dumps(jObs), headers=head)
		l.client.post('/api/observations', json=jObs, headers=head)

	#tasks = { listAll }
	tasks = { observation_temp }

class SemanticEngineLoader(HttpLocust):
	task_set = LoaderBehavior
	#host = "http://127.0.0.1:9876/engineapi"
	host = "http://engine-cont:9876/engineapi"
	min_wait = 50
	max_wait = 100

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
