#!/usr/bin/python3
import unittest
import di

class testDI(unittest.TestCase):

	def setUp(self):
		di.clear()

	def testServiceSingletone(self):
		# di.Service should be singletone!

		di.implements(di.Service, "Test/Service")
		s1 = di.inject("Test/Service")
		s2 = di.inject("Test/Service")

		self.assertIs(s1, s2)

	def testController(self):
		# di.Controller should not be singletone!

		di.implements(di.Controller, "Test/Controller")
		c1 = di.inject("Test/Controller")
		c2 = di.inject("Test/Controller")

		self.assertIsNot(c1, c2)

	def testWildcards(self):
		# Wildcards (*) at the end should return a list.

		di.implements(123, "Config/Val1")
		di.implements(234, "Config/Val2")

		dictionary = di.inject("Config/*")

		self.assertEqual(dictionary["Val1"], 123)
		self.assertEqual(dictionary["Val2"], 234)

		emptyList = di.inject("Another/*")
		self.assertIs(type(emptyList), dict)
		self.assertEqual(len(emptyList), 0)

	def testNotImplemented(self):

		with self.assertRaises(di.NotImplemented) as test:
			di.inject("TestFeature")

		self.assertEqual(test.exception.featureName, "TestFeature")

if __name__ == '__main__':
	unittest.main()