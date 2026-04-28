from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

user_account = {
    "pin": "1234",
    "balance": 1000.00
}

@app.route('/', methods=['GET', 'POST'])
def withdraw():
    if request.method == "POST":
        pin = request.form['pin']
        amount = float(request.form['amount'])

        if pin == user_account["pin"]:
            if amount <= user_account["balance"]:
                user_account["balance"] -= amount

                transaction_details = {
                    "account_number": "********1234",
                    "transaction_type": "Withdrawal",
                    "amount": amount,
                    "new_balance": user_account["balance"],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                return redirect(url_for('receipt', **transaction_details))
            else:
                return render_template('withdrawal.html', message="Insufficient Balance")
        else:
            return render_template('withdrawal.html', message="Invalid PIN")

    return render_template('withdrawal.html')


@app.route('/receipt')
def receipt():
    details = {
        "account_number": request.args.get('account_number'),
        "transaction_type": request.args.get('transaction_type'),
        "amount": float(request.args.get('amount')),
        "new_balance": float(request.args.get('new_balance')),
        "timestamp": request.args.get('timestamp')
    }
    return render_template('receipt.html', details=details)


if __name__ == "__main__":
    app.run(debug=True)
