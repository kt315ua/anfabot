# How to use

## Linux shell:
1. Setup env variables: `vim .env`
2. Load environment: `export $(cat .env | xargs)`
3. Install py-deps: `pip install -r src/requirements.txt`
4. Run from shell
   - Run: `python3 src/anfa.py`


## Docker:
1. Setup env variables: `vim .env`
2. Build docker image
   - Build image: `docker-compose -f docker-compose.yml build`
3. Run docker image
   - Run image: `docker-compose -f docker-compose.yml up`


# Note
Library [googletrans-py v4.0.0](https://github.com/ShivangKakkar/googletrans) have a bugs 
and it's a fork of [main project](https://github.com/ssut/py-googletrans). 
There are supported fresh HTTPX library required by python-telegram-bot

Fix can be found in this commit: [TypeError: unsupported operand type(s) for |: '_GenericAlias'](https://github.com/kt315ua/googletrans-fork/commit/6ed37997c799c9a4bc0de02a13995da6eaf835dd)

