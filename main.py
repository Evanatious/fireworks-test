import argparse
from fireworks import HTTPLoadTester

def get_args():
    parser = argparse.ArgumentParser(description='Parser for command line')
    parser.add_argument('url', help='The url of the server', type=str)
    parser.add_argument('--qps', metavar='[int]', help='Queries per second', default=0, type=int)
    parser.add_argument('-j', metavar='[int]', help='Number of concurrent jobs', default=1, type=int)
    parser.add_argument('-t', metavar='[int]', help='Number of times the test is run per job', default=1, type=int)

    return parser.parse_args()

def main():
    args = get_args()
    bench = HTTPLoadTester()
    results = bench.test(args.url, qps=args.qps, times=args.t, jobs=args.j)
    print(f"""Benchmarks for {args.url}
    Longest test: {results['longest']}ms
    Shortest test: {results['shortest']}ms
    Average test: {round(results['average'], 3)}ms
    Errors: {len(results['errors'])}
    Error rate: {len(results['errors']) / results['reqs']}%
    """)

if __name__ == '__main__':
    main()
