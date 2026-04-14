from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
import database
import utils
import os

app = Flask(__name__)
app.secret_key = "super_secret_premium_key" # Required for session

# Ensure DB is initialized
database.initialize_db()

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        action = request.form.get("action")
        username = request.form.get("username")
        password = request.form.get("password")
        
        if action == "login":
            user = database.authenticate_user(username, password)
            if user:
                session["user"] = {"username": user[0], "role": user[1]}
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid username or password!", "error")
        elif action == "register":
            role = request.form.get("role", "Staff")
            success, msg = database.register_user(username, password, role)
            if success:
                flash(f"Account '{username}' created. Please login.", "success")
            else:
                flash(msg, "error")
                
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
        
    items = database.get_menu_items()
    orders = database.get_recent_orders() if session["user"]["role"] == "Admin" else []
    
    return render_template("dashboard.html", user=session["user"], items=items, orders=orders)

@app.route("/add_item", methods=["POST"])
def add_item():
    if "user" not in session or session["user"]["role"] != "Admin":
        return jsonify({"success": False, "msg": "Unauthorized"})
        
    name = request.form.get("name")
    category = request.form.get("category")
    try:
        price = float(request.form.get("price"))
        database.add_menu_item(name, category, price)
        return redirect(url_for("dashboard"))
    except ValueError:
        flash("Price must be a valid number.", "error")
        return redirect(url_for("dashboard"))

@app.route("/delete_item/<int:item_id>")
def delete_item(item_id):
    if "user" in session and session["user"]["role"] == "Admin":
        database.delete_menu_item(item_id)
    return redirect(url_for("dashboard"))

@app.route("/checkout", methods=["POST"])
def checkout():
    if "user" not in session:
        return jsonify({"success": False, "msg": "Not logged in! Please login."})
        
    data = request.json
    cart = data.get("cart", [])
    total = data.get("total", 0.0)
    
    if not cart:
        return jsonify({"success": False, "msg": "Your cart is empty."})
        
    # Convert cart frontend array object mapping to dictionary expected by db
    # Frontend: [{id, name, category, price, quantity}]
    # DB expects: [{'name', 'quantity', 'price'}]
    formatted_cart = []
    for item in cart:
        formatted_cart.append({
            "name": item["name"],
            "quantity": item["quantity"],
            "price": item["price"]
        })

    order_id, timestamp = database.create_order(session["user"]["username"], total, formatted_cart)
    pdf_filename = utils.generate_receipt(order_id, timestamp, session["user"]["username"], formatted_cart, total)
    
    return jsonify({
        "success": True, 
        "msg": f"Order #{order_id} processed! Receipt generated.",
        "pdf_url": url_for("download_receipt", filename=pdf_filename)
    })

@app.route("/receipt/<filename>")
def download_receipt(filename):
    receipts_dir = os.path.join(os.path.dirname(__file__), "receipts")
    return send_from_directory(receipts_dir, filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
