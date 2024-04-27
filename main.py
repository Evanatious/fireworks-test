import argparse
from fireworks import HTTPLoadTester


def get_args():
    parser = argparse.ArgumentParser(description='Parser for command line')
    parser.add_argument('url', help='The url of the server', type=str)
    parser.add_argument('--qps', metavar='[int]', help='Queries per second', default=0, type=int)
    parser.add_argument('-j', metavar='[int]', help='Number of concurrent jobs', default=1, type=int)
    parser.add_argument('-t', metavar='[int]', help='Number of times the test is run per job', default=1, type=int)
    args = parser.parse_args()
    
    return args

def main():
    args = get_args()
    bench = HTTPLoadTester()
    results = bench.test(args.url, qps=args.qps, times=args.t, jobs=args.j)
    output = f"""Benchmarks for {args.url}
    Longest test: {results['longest']}ms
    Shortest test: {results['shortest']}ms
    Average test: {round(results['average'], 3)}ms
    Number of tests run: {args.t * args.j}
    Error rate: {len(results['errors']) / results['reqs']}%
    Errors: {len(results['errors'])}
    """
    for error in results["errors"]:
        output += f"\t- {error}\n"

    print(output)

if __name__ == '__main__':
    main()
