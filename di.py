#!/usr/bin/python3

import re

features = {}
staticInstances = {}

def implements(feature, featureName):
	global features
	global staticInstances

	features[featureName] = feature

	if type(feature) is not type:
		staticInstances[featureName] = feature

def __injectWildcard(featureName):
	reStr = '^' + featureName[:-1] + '(.*)$'
	reCompiled = re.compile(reStr)

	result = {}
	for key, val in features.items():
		reMatch = reCompiled.match(key)
		
		if reMatch is None:
			continue
		
		key = reMatch.group(1)
		longKey = featureName[:-1] + key
		result[key] = inject(longKey)

	return result


def inject(featureName):
	global features
	global staticInstances

	# Wildcards
	if featureName[-1] == "*":
		return __injectWildcard(featureName)

	# Check for an existing service instance
	if featureName in staticInstances.keys():
		return staticInstances[featureName]

	# Create the feature
	if featureName in features.keys():
		classType = features[featureName]
		instance = classType()

		# If the class is a service save the instance
		if classType.isStatic():
			staticInstances[featureName] = instance

		return instance

	raise NotImplemented(featureName)

def clear():
	global features
	global staticInstances

	features = {}
	staticInstances = {}

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

# Exceptions

class NotImplemented(RuntimeError):

	def __init__(self, featureName):
		
		self.featureName = featureName