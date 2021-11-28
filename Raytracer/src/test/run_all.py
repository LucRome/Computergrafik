from unittest import TestLoader, TestSuite, TextTestRunner

from material_tests import MaterialTests
from coordinate_tests import CoordinateUtilsTests
from object_tests import PlaneTests, SphereTest


if __name__ == '__main__':
    loader = TestLoader()
    tests = [
        # add loader.loadTestsFromTestCase(<class>) for each TestCase
        loader.loadTestsFromTestCase(MaterialTests),
        loader.loadTestsFromTestCase(CoordinateUtilsTests),
        loader.loadTestsFromTestCase(PlaneTests),
        loader.loadTestsFromTestCase(SphereTest)
    ]
    suite = TestSuite(tests)
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)