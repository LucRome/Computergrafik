from unittest import TestLoader, TestSuite, TextTestRunner


if __name__ == '__main__':
    loader = TestLoader()
    tests = [
        # add loader.loadTestsFromTestCase(<class>) for each TestCase
    ]
    suite = TestSuite(tests)
    runner = TextTestRunner(verbosity=2)
    runner.run(suite)