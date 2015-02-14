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

def __isWildcard(string):
	return string[-1] == "*"

def __filterBegin(items, begin):
	reStr = '^' + begin + '(.*)$'
	reCompiled = re.compile(reStr)

	for i in items:
		reMatch = reCompiled.match(i)

		if reMatch is None:
			continue

		i = reMatch.group(1)
		yield i

def inject(featureName):
	global features
	global staticInstances

	# Wildcards
	if __isWildcard(featureName):

		# Remove the *
		path = featureName[:-1] 
		
		result = {}
		for key in __filterBegin(features.keys(), path):

			# use recursion
			result[key] = inject(path + key) 

		return result

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