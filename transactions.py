import datetime

class Database:
    # TODO NOTE: In the future, we could keep a seperate database of ALL transcations, 
    # and another database of AVAILABLE transactions to spend. 
    # NOTE: As it stands, when points are used, they are removed from the transactions list
    def __init__(self):
        # array of transactions = [payer, points, timestamp]
        # NOTE: tuples are NOT used because points may be mutated in the future based on points spent
        self.transactions = []

    def transaction_list_to_dict(self, transactions, is_spend):
        """ 
        Inputs:
            transactions - array of arrays (2d array of "transactions" = [payer, points, timestamp])
            is_spend - boolean, TRUE: all points are negative, FALSE: all points are positive
        Returns:
            Returns a dictionary of all the transactions passed into function.
            { payer -> total_points }
        """
        modifier = -1 if is_spend else 1
        trans_dict = {}
        for transaction in transactions:
            trans_payer = transaction[0]
            trans_points = transaction[1]
            if trans_payer in trans_dict:
                trans_dict[trans_payer] = trans_dict[trans_payer] + (modifier * trans_points)
            else:
                trans_dict[trans_payer] = modifier * trans_points
        return trans_dict

    def current_transactions_dict(self):
        """
        Returns the current transaction list in dictionary form
        { payer -> total_points }
        """
        return self.transaction_list_to_dict(self.transactions, False)
        
    def add_payment(self, payer, points, timestamp):
        """
        Adds a transaction to total transactions
        Inputs:
            payer - string of the payer giving points
            points - integer of points given
            timestamp - datetime object when points were added
        NOTE: Mutates self.transactions
        """
        lo = 0
        hi = len(self.transactions)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.transactions[mid][2] < timestamp:
                lo = mid + 1
            else:
                hi = mid
        self.transactions.insert(lo, [payer, points, timestamp])
        return

    def spend_points(self, spend_points):
        """
        Spends points in total transactions based off these 2 rules:
        1. We want the oldest points to be spent first (oldest based on transaction timestamp, not the order they’re received)
        2. We want no payer's points to go negative.
        Inputs:
            spend_points - integer of points to spend
        Returns:
            Dictionary of all points needed to be spent from different payers
            { payer -> points spent }
        NOTE: If more points are spent than there are available, all transaction points are spent,
        and an entry of MORE_POINTS_NEEDED is added to the final dict to show points not available
        """
        if spend_points < 0:
            print(f"\nERROR: Tried to spend points negative points!!!")
            return {"ERROR": "CANNOT SPEND NEGATIVE POINTS! ADD THEM INSTEAD!"}
        if not self.transactions:
            print(f"\nERROR: Tried to spend points without any transactions!!!")
            return {"ERROR": "NO POINTS TO SPEND!"}

        # This for loop is only for finding where in the trans array the split needs to happen
        for index in range(len(self.transactions)):
            spend_points = spend_points - self.transactions[index][1]
            if spend_points <= 0:
                break

        spent_transactions = self.transactions[:index]
        # I want a copy of the last split transaction to be seperate from the reference of self.transactions
        # Ex:   transactions = {a: 2, b: 3}
        #       spend_points = 3
        #       --------
        #       transactions = {b: 2}
        #       spent_transactions = {a: 2, b: 1}
        # Notice "b" appears twice because its points are being split to make up the remaining points spent
        temp_trans = self.transactions[index]
        if spend_points > 0:
            print(f"\nERROR: Not enough points to spend, need {spend_points} more points!!!")
            last_spent_transaction = [temp_trans[0], temp_trans[1], temp_trans[2]]
            spent_transactions.append(["MORE_POINTS_NEEDED", -1 * spend_points, datetime.datetime.now()])
        else:
            last_spent_transaction = [temp_trans[0], temp_trans[1] + spend_points, temp_trans[2]]
        spent_transactions.append(last_spent_transaction)

        # Mutating the original transactions to remove points spent
        if spend_points < 0:
            self.transactions = self.transactions[index:]
            self.transactions[0][1] = -1 * spend_points
        else:
            # Since there will be no "partial" points left, we can cleanly break the first element
            self.transactions = self.transactions[index + 1:]
            
        return self.transaction_list_to_dict(spent_transactions, True)
