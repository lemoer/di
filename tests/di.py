#!/usr/bin/python3
import unittest
import di

class testDI(unittest.TestCase):

	def setUp(self):
		self.di = di.DI()

	def testServiceSingletone(self):
		# di.Service should be singletone!

		self.di.implements(di.Service, "Test/Service")
		s1 = self.di.inject("Test/Service")
		s2 = self.di.inject("Test/Service")

		self.assertIs(s1, s2)

	def testController(self):
		# di.Controller should not be singletone!

		self.di.implements(di.Controller, "Test/Controller")
		c1 = self.di.inject("Test/Controller")
		c2 = self.di.inject("Test/Controller")

		self.assertIsNot(c1, c2)

	def testWildcard(self):
		# Wildcards (*) at the end should return a list.

		self.di.implements(di.Value, "Config/Val1")
		self.di.implements(di.Value, "Config/Val2")

		self.di.inject("Config/Val1").set(123)
		self.di.inject("Config/Val2").set(234)

		dictionary = self.di.inject("Config/*")

		self.assertEqual(dictionary["Val1"].get(), 123)
		self.assertEqual(dictionary["Val2"].get(), 234)

		emptyList = self.di.inject("Config/*")
		self.assertEqual(len(emptyList), 0)

	def testList(self):
		# The type of an empty di.List should be list not None
		l = di.List()
		
		self.assertIsNot(l.get(), None)
		self.assertIs(l.get(), list)

		l.add('TestStr')

		self.assertEqual(l.get()[0], 'TestStr')

	def testDict(self):
		# The type of an empty di.Dict should be dict not None
		l = di.Dict()

		self.assertIsNot(l.get(), None)
		self.assertIs(l.get(), dict)

		l.put('test', 'val')

		self.assertEqual(l.get()['test'], 'val')

if __name__ == '__main__':
	unittest.main()