from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date, timedelta

app = Flask(__name__)

def db():
    conn = sqlite3.connect("finance.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def dashboard():
    d = db()
    income = d.execute("SELECT IFNULL(SUM(amount),0) FROM sales").fetchone()[0]
    expenses = d.execute("SELECT IFNULL(SUM(amount),0) FROM expenses").fetchone()[0]
    unpaid = d.execute("SELECT COUNT(*) FROM bills WHERE status='Unpaid'").fetchone()[0]
    profit = income - expenses
    return render_template("dashboard.html", income=income, expenses=expenses, profit=profit, unpaid=unpaid)

@app.route("/expenses", methods=["GET","POST"])
def expenses_page():
    d = db()
    if request.method == "POST":
        d.execute(
            "INSERT INTO expenses (date,category,amount,payment_method,notes) VALUES (?,?,?,?,?)",
            (request.form["date"], request.form["category"], request.form["amount"],
             request.form["payment"], request.form["notes"])
        )
        d.commit()
        return redirect(url_for("expenses_page"))
    rows = d.execute("SELECT * FROM expenses ORDER BY date DESC").fetchall()
    return render_template("expenses.html", rows=rows)

@app.route("/sales", methods=["GET","POST"])
def sales_page():
    d = db()
    if request.method == "POST":
        d.execute(
            "INSERT INTO sales (date,description,amount,type,notes) VALUES (?,?,?,?,?)",
            (request.form["date"], request.form["desc"], request.form["amount"],
             request.form["type"], request.form["notes"])
        )
        d.commit()
        return redirect(url_for("sales_page"))
    rows = d.execute("SELECT * FROM sales ORDER BY date DESC").fetchall()
    return render_template("sales.html", rows=rows)

@app.route("/bills", methods=["GET","POST"])
def bills_page():
    d = db()
    if request.method == "POST":
        d.execute(
            "INSERT INTO bills (name,category,amount,due_date,status) VALUES (?,?,?,?,?)",
            (request.form["name"], request.form["category"], request.form["amount"],
             request.form["due"], "Unpaid")
        )
        d.commit()
        return redirect(url_for("bills_page"))
    soon = (date.today() + timedelta(days=3)).isoformat()
    rows = d.execute(
        "SELECT *, (status='Unpaid' AND due_date<=?) as due_soon FROM bills ORDER BY due_date",
        (soon,)
    ).fetchall()
    return render_template("bills.html", rows=rows)

@app.route("/budgets", methods=["GET","POST"])
def budgets_page():
    d = db()
    if request.method == "POST":
        d.execute(
            "INSERT OR REPLACE INTO budgets (category, monthly_budget) VALUES (?,?)",
            (request.form["category"], request.form["budget"])
        )
        d.commit()
        return redirect(url_for("budgets_page"))
    rows = d.execute("""
        SELECT b.category, b.monthly_budget,
        IFNULL((SELECT SUM(amount) FROM expenses e WHERE e.category=b.category),0) as spent
        FROM budgets b
    """).fetchall()
    return render_template("budgets.html", rows=rows)

@app.route("/inventory", methods=["GET","POST"])
def inventory_page():
    d = db()
    if request.method == "POST":
        d.execute(
            """INSERT INTO inventory (sku,item_name,category,beginning_qty,purchased_qty,sold_qty,cost,price)
               VALUES (?,?,?,?,?,?,?,?)""",
            (request.form["sku"], request.form["name"], request.form["category"],
             request.form["bq"], request.form["pq"], request.form["sq"],
             request.form["cost"], request.form["price"])
        )
        d.commit()
        return redirect(url_for("inventory_page"))
    rows = d.execute("""
        SELECT *, (beginning_qty + purchased_qty - sold_qty) as ending_qty
        FROM inventory
    """).fetchall()
    return render_template("inventory.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
