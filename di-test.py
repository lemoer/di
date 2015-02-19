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

		self.assertIsNot(s1, None)
		self.assertIs(s1, s2)

	def testController(self):
		# di.Controller should not be singletone!

		di.implements(di.Controller, "Test/Controller")
		c1 = di.inject("Test/Controller")
		c2 = di.inject("Test/Controller")

		self.assertIsNot(c1, c2)

	def testNotImplemented(self):

		with self.assertRaises(di.NotImplemented) as test:
			di.inject("TestFeature")

		self.assertEqual(test.exception.featureName, "TestFeature")

	def testContext(self):

		context = di.context("Config/Module/TestSetting")
		arr = di.rootContext.subcontexts("Config/Module/TestSetting")

		self.assertIs(arr[0], context)
		self.assertIs(arr[1], context.parent)
		self.assertIs(arr[-1], di.rootContext)

	def testProvider(self):

		class TestProvider(di.Provider):

			def provide(self, path):

				if path.match("."):
					return 1234
				elif path.match("SubPath"):
					return 2345

				raise NotImplemented

		di.implements(TestProvider, "Test")

		self.assertEqual(di.inject("Test"), 1234)
		self.assertEqual(di.inject("Test/SubPath"), 2345)

	def testPath(self):

		p = di.Path("level1/level2/level3")

		self.assertEqual(p.first(), "level1")

		p2 = p.sub()

		self.assertEqual(p.first(), "level1")
		self.assertEqual(p2.first(), "level2")

		self.assertEqual(str(p2), "level2/level3")

		p3 = di.Path(".")
		self.assertTrue(p3.empty())
		self.assertTrue(p3.match("."))

if __name__ == '__main__':
	unittest.main()
