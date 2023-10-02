from flask import Flask, jsonify, request

# Create a new Flask application instance
app = Flask(__name__)

# Define an empty list to store the transactions
transactions = []


# Define a route to add a new transaction
@app.route('/add', methods=['POST'])
def add_transaction():
    # Get the payer, points, and timestamp from the request body
    payer = request.json['payer']
    points = request.json['points']
    timestamp = request.json['timestamp']
    # Add the transaction to the list of transactions
    transactions.append({'payer': payer, 'points': points, 'timestamp': timestamp})
    # Return a success message
    return '', 200


# Define a route to spend points from the transactions
@app.route('/spend', methods=['POST'])
def spend_points():
    # Get the number of points to spend from the request body
    required_points = request.json['points']
    # Create an empty list to store the spent points
    spend_points = dict()
    # Sort the transactions by timestamp in ascending order
    total_points = 0
    for transaction in sorted(transactions, key=lambda x: x['timestamp']):
        # Calculate the whole points to determine if it enough for this spend
        total_points += transaction['points']

    if total_points < required_points:
        return "Not enough points", 400
    else:
        required_points_changing = required_points
        for transaction in sorted(transactions, key=lambda x: x['timestamp']):
            # Calculate the whole points to determine if it enough for this spend
            if transaction['payer'] not in spend_points.keys():
                spend_points[transaction['payer']] = 0

            if required_points_changing <= transaction['points']:
                spend_points[transaction['payer']] -= required_points_changing
                transaction['points'] = transaction['points'] - required_points_changing
                break
            else:
                required_points_changing -= transaction['points']
                spend_points[transaction['payer']] -= transaction['points']
                transaction['points'] = 0

        # Return the list of spent points
        return spend_points, 200


# Define a route to get the current balance of each payer
@app.route('/balance', methods=['GET'])
def get_balance():
    # Create an empty dictionary to store the balance of each payer
    balance = {}
    # Iterate over all transactions and update the balance for each payer accordingly
    for transaction in transactions:
        if transaction['payer'] not in balance:
            balance[transaction['payer']] = 0
        balance[transaction['payer']] += transaction['points']
    # Return the dictionary of balances
    return jsonify(balance)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)