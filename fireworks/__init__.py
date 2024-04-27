import requests
import time
import threading
from urllib.parse import urlparse, urlunparse


class HTTPLoadTester:
    """A general HTTP load-testing and benchmarking library for sending HTTP requests and measuring performance."""

    def test(self, url: str, **kwargs):
        """Tests a url with the provided arguments.

        Parameters
        ----------
        url: str
            The name of the url
        kwargs
            Optional additional parameters, which include:
            qps : int, optional
                The number of queries per second
            jobs : int, optional
                The concurrent threads to utilize.
            times : int, optional
                The amount of requests per job.

        Returns
        -------
        res
            A dictionary with 5 results from the test(s):
            the longest amount of time taken for a test,
            the shortest amount of time taken for a test,
            the average amount of time taken for a test,
            the errors raised,
            and the total number of requests made
        """
        qps = kwargs.get("qps", 0)
        times = kwargs.get("times", 1)
        jobs = kwargs.get("jobs", 1)
        #Check for valid URL, only positive numbers
        assert HTTPLoadTester._validate_url(url)
        assert qps >= 0
        assert times >= 0
        assert jobs >= 0

        res = {
            "longest": None,
            "shortest": None,
            "average": 0,
            "errors": [],
            "reqs": times * jobs,
        }

        max_tx = 0 #keep track of total time elapsed
        def run_test():
            nonlocal res, url, max_tx
            data = HTTPLoadTester._request(url)
            if "err" in data:
                res["errors"].append(data["err"])
                return

            elapsed = data["elapsed"]
            max_tx += elapsed
            if not res["longest"] or elapsed > res["longest"]:
                res["longest"] = elapsed
            if not res["shortest"] or elapsed < res["shortest"]:
                res["shortest"] = elapsed

        #Threads to simulate concurrent users
        threads = []
        for _ in range(times):
            if qps > 0:
                time.sleep(1 / qps)

            for _ in range(jobs):
                thread = threading.Thread(target=run_test)
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

        res["average"] = max_tx / res['reqs']
        return res

    def _request(url: str) -> dict:
        res = {}

        try:
            r = requests.get(url)
            if not r.ok:
                raise requests.HTTPError(request=r.request, response=r)
            res["isOK"] = r.ok
            res["elapsed"] = r.elapsed.microseconds / 1_000
        except Exception as e:
            # pass error as value rather than raising
            res["err"] = e

        return res

    def _validate_url(url) -> bool:
        parts = urlparse(url)
        if not all([parts.scheme, parts.netloc]):
            raise ValueError
        url = urlunparse(parts)
        return True
