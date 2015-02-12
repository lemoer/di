#!/usr/bin/python3

import re

class DI(object):
	"""This class should provide the main functions for the DI-Pattern"""
	def __init__(self):
		super(DI, self).__init__()
		self.modules = {}
		self.staticInstances = {}

	def implements(self, classType, moduleName):
		self.modules[moduleName] = classType

	def inject(self, moduleName):
		# Wildcards
		if moduleName[-1] == "*":
			reStr = '^' + moduleName[:-1] + '(.*)$'
			reCompiled = re.compile(reStr)

			result = {}
			for key, val in self.modules.items():
				reMatch = reCompiled.match(key)
				
				if reMatch is None:
					continue
				
				key = reMatch.group(1)
				longKey = moduleName[:-1] + key
				result[key] = self.inject(longKey)

			return result

		# Check for an existing service instance
		if moduleName in self.staticInstances.keys():
			return self.staticInstances[moduleName]

		classType = self.modules[moduleName]
		instance = classType()

		# If the class is a service save the instance
		if classType.isStatic():
			self.staticInstances[moduleName] = instance

		return instance

# Singletone
class Service(object):
	@staticmethod
	def isStatic():
		return True

# Generates multiple instances die.
class Controller(object):
	@staticmethod
	def isStatic():
		return False

class Value(object):
	@staticmethod
	def isStatic():
		return True

	def __init__(self):
		self.value = None
	
	def get(self):
		return self.value

	def set(self, value):
		self.value = value

class List(Value):

	def __init__(self):
		self.value = []

	def add(self, value):
		if type(self.value) is list:
			self.value += [value]

class Dict(Value):

	def __init__(self):
		self.value = {}

	def put(self, key, value):
		if type(self.value) is dict:
			self.value[key] = value

di = DI()