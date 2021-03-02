# fetch
## Fetch Rewards Coding Exercise 
Simple Flask app that adds, spends, and checks transaction points through HTTP requests.

**Native environment on Ubuntu 18.04.5 LTS**




Commands:
sudo apt install uwsgi-core uwsgi-plugin-python3 
uwsgi --http-socket 127.0.0.1:5000 --mount /=server:app --plugin python3
export FETCH_URL=http://127.0.0.1:5000
python3 client.py
