# server.py
from flask import Flask, request, make_response
from transactions import Database

transactions = Database()
app = Flask(__name__)

@app.route("/fetch/transactions", methods = ['GET', 'POST'])
def get_transactions():
    if request.method == 'GET':
        return transactions.current_transactions_dict()

    if request.method == 'POST':
        data = request.get_json()
        transactions.add_payment(data['payer'], data['points'], data['timestamp'])
        return make_response("", 200)

@app.route("/fetch/spend", methods = ['POST'])
def spend():
    if request.method == 'POST':
        data = request.get_json()
        return transactions.spend_points(data['points'])