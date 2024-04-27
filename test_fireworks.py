import unittest
from fireworks import HTTPLoadTester


class TestFireworks(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.url = "http://localhost:3001"
        self.qps = 0
        self.t = 1
        self.j = 1
        self.bench = HTTPLoadTester()

    def test_errors(self):
        codes = [400, 500]
        for code in codes:
            url = f"{self.url}/status/{code}"
            results = self.bench.test(url, qps=self.qps, times=self.t, jobs=self.j)
            self.assertEqual(len(results['errors']), results['reqs'])
            for err in results['errors']:
                self.assertEqual(err.response.status_code, code)

    def test_invalid_url(self):
        with self.assertRaises(AssertionError):
            self.bench.test('https:/example.com')
        
        with self.assertRaises(AssertionError):
            self.bench.test('example.com')
            
        with self.assertRaises(AssertionError):
            self.bench.test('randomtext')

    def test_success(self):
        results = self.bench.test(self.url, qps=self.qps, times=self.t, jobs=self.j)
        self.assertFalse(results['errors'])
        self.assertEqual(results['reqs'], 1)

    def test_success2(self):
        results = self.bench.test(self.url, qps=5, times=50, jobs=5)
        self.assertFalse(results['errors'])
        self.assertEqual(results['reqs'], 250)

    def test_negative_nums(self):
        with self.assertRaises(AssertionError):
            self.bench.test(self.url, qps=-1, times=1, jobs=1)
        
        with self.assertRaises(AssertionError):
            self.bench.test(self.url, qps=0, times=-1, jobs=1)
            
        with self.assertRaises(AssertionError):
            self.bench.test(self.url, qps=0, times=1, jobs=-1)

if __name__ == '__main__':
    unittest.main()
