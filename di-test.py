#!/usr/bin/python3
import unittest
import di

class testDI(unittest.TestCase):

	def setUp(self):
		self.di = di

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

		self.di.implements(123, "Config/Val1")
		self.di.implements(234, "Config/Val2")

		#self.di.inject("Config/Val1").set(123)
		#self.di.inject("Config/Val2").set(234)

		dictionary = self.di.inject("Config/*")

		self.assertEqual(dictionary["Val1"], 123)
		self.assertEqual(dictionary["Val2"], 234)

		emptyList = self.di.inject("Another/*")
		self.assertIs(type(emptyList), dict)
		self.assertEqual(len(emptyList), 0)

if __name__ == '__main__':
	unittest.main()