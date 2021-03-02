# Fetch Rewards Coding Exercise 
Exercise at: https://fetch-hiring.s3.us-east-1.amazonaws.com/points.pdf  

Simple Flask app that adds, spends, and checks transaction points through HTTP requests. In this repo is a simple client script, **but this web server can handle normal JSON HTTP requests to http://cstransky.com:4000 (or locally at http://127.0.0.1:400) with any client**.  
Full details of the exercise will be listed below.

### Show Points
```
http://cstransky.com:4000/fetch/transactions GET
```

### Add Points
```
http://cstransky.com:4000/fetch/transactions POST

Example JSON: { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }
```

### Spend Points
```
http://cstransky.com:4000/fetch/spend POST

Example JSON: { "points": 5000 }
```



## Installation Instructions:
**Native environment on Ubuntu 18.04.5 LTS**  
In order to get this working, you'll need to make sure Python3 and Flask are properly installed. I used uWSGI to run a simple local test API server. These instructions will be for Ubuntu specifically (send me a message if you need instructions for something like Windows or macOS).

Open a command window and execute the following commands within **~/\<whatever path\>/fetch/**

### Commands:  
First Python3, pip3, and uWSGI must be installed:
```
sudo apt install python3 python3-pip uwsgi-core uwsgi-plugin-python3 
```
Then use pip3 to install Flask and the requests library
```
pip3 install flask requests
```
You can now run the API server with the following command below (this will be local)
```
uwsgi --http-socket 127.0.0.1:4000 --mount /=server:app --plugin python3
```
Open another command window for the client and use the following command to see if it worked:
```
python3 test.py -u http://127.0.0.1:4000
```
The following output should appear:
```
Points added:   {'DANNON': 1100, 'MILLER COORS': 10000, 'UNILEVER': 200}
Points spent:   {'DANNON': -100, 'MILLER COORS': -4700, 'UNILEVER': -200}
Points left:    {'DANNON': 1000, 'MILLER COORS': 5300}
```
  
## Command Instructions
The following instructions are for how to use the host client.  
**This API server is actually hosted on http://cstransky.com:4000, give it a try by entering that URL as a "--url" parameter.** Look at the current "database" by loading **http://cstransky.com:4000/fetch/transactions** in your URL bar.

### NOTE:
To allow yourself a much easier time using the client, set the following **FETCH_URL** environment variable to whatever the server URL is.
```
export FETCH_URL=http://<server url>:<port>

Example: export FETCH_URL=http://127.0.0.1:4000
```
### Add Points
You can add points to the "database" by including a payer, points, and timestamp.
In order to add points, use the following command
```
python3 client.py -u <url> --add -d <payer> -p <points> -t <zulu UTC timestamp>

--add: flag that must be added to show that you wish to add points
-u, --url: url with "http://" adapter and port number, ex: http://127.0.0.1:4000
-d, --payer: String of whoever the payer is
-p, --points: Integer of points to be added (can be negative, but not zero)
-t, --timestamp: OPTIONAL. String timestamp in Zulu UTC format, ex: 2020-10-31T10:00:00Z. If no flag is added, the current time will be used
--show: Show the total amount of points in the "database" after adding
```

### Spend Points
Spends points in total transactions based off these 2 rules:
1. We want the oldest points to be spent first (oldest based on transaction timestamp, not the order they’re received)
2. We want no payer's points to go negative.
```
python3 client.py -u <url> --spend -p <points>

--spend: flag that must be added to show that you wish to spend points
-u, --url: url with "http://" adapter and port number, ex: http://127.0.0.1:4000
-p, --points: Integer of points to be added (cannot be negative)
--show: Show the total amount of points in the "database" after spending
```

### Show Points
Shows the total amount of points in the "database" based on payer. 
```
python3 client.py -u <url> --spend -p <points>

--show: flag that must be added to show you want to see the points
-u, --url: url with "http://" adapter and port number, ex: http://127.0.0.1:4000
```

## Design Decisions
To start, a simple 2D array was used as a "database" to keep track of transactions, as was allowed in the exercised. The Database object in transactions.py uses the 2D array "self.transactions" to store an array of arrays ordered by their timestamps.
```
self.transactions = [[payer1, points1, timestamp1],
                     [payer2, points2, timestamp2],
                     [payer3, points3, timestamp3]]
```
The 2D array needed to be ordered to allow for the spending algorithm to work based off of time, so every time a transaction is added, it's inserted at a O(n) time in the transaction array based on how old it is (older -> newer).

When it comes to spend the points, because the transactions are ordered based on timestamps, all that's needed is to find the split point in the array to find where the spending "cutoff" is.
```
self.transactions = [[guy, 10, 2001],
                     [dude, 30, 2004],
                     [guy, 20, 2006]]
points = 20
----
self.transactions = [[dude, 20, 2004],
                     [guy, 20, 2006]]
points_list =   [[guy, 10, 2001],
                [dude, 10, 2004]]
points_json =   {   "guy": -10
                    "dude": -10 }
```
Instead of having a seperate "database" to keep track of all transactions, there's only one "database" that keeps track of the total points available to spend, meaning that **entries are actually removed**. If more functionality was needed, this could be easily added by including another Database object array called "all_transactions" that would add to it the same time payments are added, effectively keeping 2 databases of all transactions, and only transactions available.

### Edge Cases
1. Not enough points to spend. If there aren't enough points, then the returning JSON will actually add an extra entry called "MORE_POINT_NEEDED" that will show how many points were not spent. In the background the "database" will remove all entries, as all points have been spent. An example:
```
points = 10000
{'DANNON': -1000, 'MILLER COORS': -5300, 'MORE_POINTS_NEEDED': 3700}
```
2. Trying to spend with no points. An error JSON will be returned as the following:
```
{'ERROR': 'NO POINTS TO SPEND!'}
```
3. Negative points are "spent"/added. This behavior is forbidden by the client, but if someone were to make an HTTP request with negative points, it will send an error JSON back as below:
```
{'ERROR': 'CANNOT SPEND NEGATIVE POINTS! ADD THEM INSTEAD!'}
```