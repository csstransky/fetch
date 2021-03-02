# client.py
import os
import requests
import sys
import getopt
from datetime import datetime

TRANSACTION_ROUTE = "/fetch/transactions"
SPEND_ROUTE = "/fetch/spend"

def get_args(argv):
    url = os.environ["FETCH_URL"] if "FETCH_URL" in os.environ else ""
    points = 0
    payer = ""
    timestamp = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ")
    is_spend = False
    is_add = False
    is_show = False
    try:
        opts, _ = getopt.getopt(argv,"hd:p:t:u:",["spend","add","show","payer=","points=","timestamp=","url="])
    except getopt.GetoptError:
        print('\nERROR: Issue getting command args')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("\nUse one of the following commands below:"
            + '\nclient.py -u <server url> --add -d <payer> -p <points> [-t <zulu utc timestamp>]'
            + '\nclient.py -u <server url> --spend -p <points>'
            + '\nclient.py -u <server url> --show')
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-d", "--payer"):
            payer = arg
        elif opt in ("-p", "--points"):
            points = int(arg)
        elif opt in ("-t", "--timestamp"):
            timestamp = arg
        elif opt in ("--spend"):
            is_spend = True
        elif opt in ("--add"):
            is_add = True
        elif opt in ("--show"):
            is_show = True
    return url, points, payer, timestamp, is_spend, is_add, is_show

def add_request(url, payer, points, timestamp):
    if payer == "" or points == 0:
        print("\nERROR: Need proper \"--payer\" and non 0 \"--points\" arguments")
    else:
        args_dict = {"payer": payer, "points": points, "timestamp": timestamp}
        response = requests.post(url + TRANSACTION_ROUTE, json=args_dict)
        print(response)

def spend_request(url, points):
    if points < 0:
        print("\nERROR: Need \"--points\" argument above 0")
    else:
        args_dict = {"points": points}
        response = requests.post(url + SPEND_ROUTE, json=args_dict)
        print(f"Points that were spent below:\n{response.json()}")

def show_request(url):
    response = requests.get(url + TRANSACTION_ROUTE)
    print(f"Total points left to spend from transactions:\n{response.json()}")

if __name__ == "__main__":
    url, points, payer, timestamp, is_spend, is_add, is_show = get_args(sys.argv[1:])
    if not url:
        print(f"\nERROR: URL \"{url}\" is not correct, either set the environment variable \"FETCH_URL\" or use the \"--url\" flag."
            + "\nRemember to add the appropriate url adapter and port."
            + "\nExample: python3 client.py --url https://127.0.0.1:5000 --show")
    else:
        if is_add or is_spend or is_show:
            if is_add:
                add_request(url, payer, points, timestamp)
            elif is_spend:
                spend_request(url, points)
            if is_show:
                show_request(url)
        else:
            print("\nERROR: Denote which action to commit with \"--add\", \"--spend\", or \"--show\"")



