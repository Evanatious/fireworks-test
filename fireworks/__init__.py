import requests
import time
import threading


class HTTPLoadTester:
    """A general HTTP load-testing and benchmarking library for sending HTTP requests and measuring performance."""

    def test(self, server: str, **kwargs):
        """Tests a server with the provided arguments.

        Parameters
        ----------
        server: str
            The name of the server
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
            and the number of requests made
        """
        qps = kwargs.get("qps", 0)
        times = kwargs.get("times", 1)
        jobs = kwargs.get("jobs", 1)
        res = {
            "longest": None,
            "shortest": None,
            "average": 0,
            "errors": [],
            "reqs": times,
        }

        max_tx = 0
        def run_test():
            nonlocal res, server, max_tx
            data = HTTPLoadTester._request(server)
            if "err" in data:
                res["errors"].append(data["err"])
                return

            elapsed = data["elapsed"]
            max_tx += elapsed
            if not res["longest"] or elapsed > res["longest"]:
                res["longest"] = elapsed
            if not res["shortest"] or elapsed < res["shortest"]:
                res["shortest"] = elapsed

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

        res["average"] = max_tx / (times * jobs)
        return res

    def _request(url: str) -> dict:
        res = {}

        try:
            r = requests.get(url)
            res["isOK"] = r.ok
            res["elapsed"] = r.elapsed.microseconds / 1_000
        except Exception as e:
            res["err"] = e

        return res


