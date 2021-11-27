from unittest import TestLoader, TestSuite, TextTestRunner

from material_tests import MaterialTests


if __name__ == '__main__':
    loader = TestLoader()
    tests = [
        # add loader.loadTestsFromTestCase(<class>) for each TestCase
        loader.loadTestsFromTestCase(MaterialTests)
    ]
    suite = TestSuite(tests)
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)