# Setup

```sh
git clone https://github.com/Evanatious/fireworks-test fireworks
cd fireworks
pip3 install -r ./requirements.txt
python3 ./main.py --help
```

# Setup (Docker)

```sh
git clone https://github.com/Evanatious/fireworks-test fireworks
cd fireworks
docker build . -t fireworks:latest
docker run -it fireworks:latest python3 ./main.py --help
```
