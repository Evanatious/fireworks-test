# Setup

```sh
git clone https://github.com/Evanatious/fireworks-test fireworks
cd fireworks
pip3 install -r ./requirements.txt
python3 ./main.py --help
```

If "python3" doesn't work, try "python". Same with "pip3" and "pip"

# Setup (Docker)

```sh
git clone https://github.com/Evanatious/fireworks-test fireworks
cd fireworks
docker build . -t fireworks:latest
docker run -it fireworks:latest python3 ./main.py --help
```

# How to Use

```sh
usage: main.py [-h] [--qps [int]] [-j [int]] [-t [int]] url

Parser for command line

positional arguments:
  url          The url of the server

options:
  -h, --help   show this help message and exit
  --qps [int]  Queries per second
  -j [int]     Number of concurrent jobs
  -t [int]     Number of times the test is run per job
```

# Further Steps

If I had more time, I would include some features like accepting different 
types of requests rather than just GET, proper thread-syncing, better UX, and 
more extensive, comprehensive test cases.
