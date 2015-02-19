#!/usr/bin/python3

import re

def clear():
	# TODO: Restart the di-lib
	pass

def implements(feature, path):
	global rootContext
	handler = rootContext.subcontexts(path)
	handler[0].implements(feature, "")

def inject(path):
	"""
	This function walks through the context tree to
	the given path. As it found the certain node, it ask's
	the context to provide the demanded feature.
	"""
	global rootContext
	path = Path(path)

	handler = rootContext.subcontexts(path)

	i = 0
	# Walk trough the hierarchy (backwards)
	for h in handler:
		try:
			return h.provide(path.last(i))
		except NotImplemented:
			pass

		i += 1

	raise NotImplemented(str(path))

def context(path):
	global rootContext
	path = Path(path)
	return rootContext.subcontexts(path)[0]

class Context(object):

	def __init__(self, parent=None, scope=""):
		self.parent = parent
		self.provider = None
		self.children = {}
		self.scope = Path(scope)

	def inject(self, path="."):
		"""
		The function walks from the rootContext
		trough the tree, because if there is no Context that
		can provide the feature below in the tree, the Contexts
		above these might have an Provider for the feature.
		"""
		return inject(self.scope.append(path))

	def implements(self, feature, path="."):
		path = Path(path)

		if not path.match("."):
			handler = self.subcontexts(path)
			handler[0].implements(feature, "")
			return

		if issubclass(feature, Service):
			self.provider = ServiceProvider(feature)
		
		if issubclass(feature, Controller):
			self.provider = ControllerProvider(feature)

		if issubclass(feature, Provider):
			self.provider = feature()

		# TODO implement

	def provide(self, path):
		if self.provider is None:
			raise NotImplemented
		else:
			return self.provider.provide(path)

	def subcontexts(self, path):
		"""
		
		"""
		path = Path(path)

		if path.empty():
			return [self]
		
		subdir = path.first()

		if subdir not in self.children.keys():
			self.children[subdir] = Context(self, self.scope.append(subdir))

		element = self.children[subdir]

		return element.subcontexts(path.sub()) + [self]


class Path(object):

	def __init__(self, raw):
		if isinstance(raw, Path):
			self.data = raw.data
		elif isinstance(raw, list):
			self.data = raw
		else:
			self.data = raw.split("/")

		if "." in self.data:
			self.data.remove(".")
		if "" in self.data:
			self.data.remove("")

	def __str__(self):
		return "/".join(self.data)

	def match(self, other):
		other = Path(other)

		return str(self) == str(other)

	def first(self):
		return self.data[0]

	def last(self, n=0):
		if n == 0:
			return Path("")

		return Path(self.data[-n:])

	def sub(self):
		return Path(self.data[1:])

	def empty(self):
		return len(self.data) == 0

	def append(self, other):
		other = Path(other)
		return Path(self.data + other.data)


class Feature(object):
	pass

class Service(Feature):
	pass

class Controller(Feature):
	pass

class Provider(object):
	
	def provide(self):
		raise NotImplemented

class ServiceProvider(Provider):

	def __init__(self, service):
		self.instance = None
		self.service = service

	def provide(self, path):

		if not path.match("."):
			raise NotImplemented

		if self.instance is None:
			self.instance = self.service()

		return self.instance

class ControllerProvider(Provider):

	def __init__(self, controller):
		self.controller = controller

	def provide(self, path):

		if not path.match("."):
			raise NotImplemented

		return self.controller()


# Exceptions

class NotImplemented(RuntimeError):

	def __init__(self, featureName=""):
		
		self.featureName = featureName

rootContext = Context()
