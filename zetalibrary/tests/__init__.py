import unittest


def all_tests_suite():
    return unittest.TestLoader().loadTestsFromNames([
        'zetalibrary.tests.main',
        'zetalibrary.tests.zeta',
        'zetalibrary.tests.frameworks',
    ])


def main():
    runner = unittest.TextTestRunner()
    suite = all_tests_suite()
    runner.run(suite)


if __name__ == '__main__':
    import os.path
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    main()

