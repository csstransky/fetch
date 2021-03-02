# client.py
import os
import requests
import sys
import getopt
import datetime

def get_url(argv):
    url = os.environ["FETCH_URL"] if "FETCH_URL" in os.environ else ""

    try:
        opts, _ = getopt.getopt(argv,"hu:",["url="])
    except getopt.GetoptError:
        print('\nERROR: Issue getting command args')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("\n'test.py -u <server url>")
        elif opt in ("-u", "--url"):
            url = arg
    return url

def test_points_example(url):
    trans_url = url + "/fetch/transactions"
    add1 = { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
    add2 = { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
    add3 = { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
    add4 = { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
    add5 = { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }
    requests.post(trans_url, json=add1)
    requests.post(trans_url, json=add2)
    requests.post(trans_url, json=add3)
    requests.post(trans_url, json=add4)
    requests.post(trans_url, json=add5)
    all_added_transactions = requests.get(trans_url)
    print(f'Points added:\t{all_added_transactions.json()}')

    points_url = url + "/fetch/spend"
    points = { "points": 5000 }
    spent_points = requests.post(points_url, json=points)
    print(f"Points spent:\t{spent_points.json()}")

    points_left = requests.get(trans_url)
    print(f"Points left:\t{points_left.json()}")

if __name__ == "__main__":
    url = get_url(sys.argv[1:])
    if not url:
        print(f"\nERROR: URL \"{url}\" is not correct, either set the environment variable \"FETCH_URL\" or use the \"--url\" flag."
            + "\nRemember to add the appropriate url adapter and port."
            + "\nExample: python3 test.py -u https://127.0.0.1:5000")
    else:
        test_points_example(url)



