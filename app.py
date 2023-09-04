from flask import Flask, make_response, request, jsonify, send_file
from flask_cors import CORS, cross_origin

import qrcode
from io import BytesIO
import base64
from datetime import datetime


import sqlite3

conn = sqlite3.connect("test.db", check_same_thread=False)
cur = conn.cursor()
app = Flask(__name__)
cors = CORS(app)


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


def generate_qr_code(data):
    print(data)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill="black", back_color="white")

    buffer = BytesIO()
    image.save(buffer)
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    return image_base64


@app.route("/signup", methods=["POST", "GET"])
def signup():
    try:
        print("Running")
        if request.method == "POST":
            data = request.get_json()
            username = data["username"]
            email = data["email"]
            password = data["password"]

            try:
                qr = generate_qr_code({"username": username})
                cur.execute(
                    f"INSERT INTO users (username, email, password,points,qr) VALUES('{username}', '{email}', '{password}',0,'{qr}')",
                )

                conn.commit()

                return make_response(
                    jsonify(
                        {"success": True, "message": "User registered successfully"}
                    ),
                    200,
                )

            except Exception as e:
                return make_response(
                    jsonify({"success": False, "message": f"Unsuccessful {e}"}), 201
                )

    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/login", methods=["POST", "GET"])
def login():
    try:
        if request.method == "POST" or request.method == "GET":
            data = request.get_json()
            print(data)
            username = data["username"]
            password = data["password"]

            try:
                cur.execute(
                    f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
                )

                user = cur.fetchone()
                cur.execute(
                    f"SELECT username,transaction_date, transaction_amount FROM transaction_history WHERE username = '{username}' ORDER BY transaction_date DESC",
                )
                transaction_history = cur.fetchall()
                if user:
                    return make_response(
                        jsonify(
                            {
                                "success": True,
                                "message": "You Have successfully Logged in",
                                "user": user,
                                "transaction_history": transaction_history,
                            }
                        ),
                        201,
                    )
                else:
                    return make_response(
                        jsonify(
                            {
                                "success": False,
                                "message": "Invalid username or password",
                            }
                        ),
                        401,
                    )
            except Exception as e:
                return make_response(
                    jsonify({"success": False, "message": f"Unsuccessful: {e}"}), 500
                )
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/generate_qr", methods=["POST", "GET"])
def generate_qr():
    data = request.json.get("data")
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(fill="black", back_color="white")
    image_path = "qrcode.png"
    image.save(image_path)

    return jsonify({"image_path": image_path}), 200


@app.route("/qr_code", methods=["GET"])
def get_qr_code():
    image_path = request.args.get("image_path")
    if not image_path:
        return jsonify({"error": "Invalid image path"}), 400

    try:
        return send_file(image_path, mimetype="image/png")
    except FileNotFoundError:
        return jsonify({"error": "QR code not found"}), 404


@app.route("/buy_points", methods=["POST"])
def buy_points():
    data = request.get_json()
    username = data.get("username")
    amount = data.get("amount")

    if not username or not amount:
        return "Invalid request. Please provide both username and amount.", 400

    try:
        cur.execute(f"SELECT points FROM users WHERE username = '{username}'")
        print(".")
        current_points = cur.fetchone()
        print(current_points)
        if current_points is None:
            return "User not found.", 404

        new_points = current_points[0] + amount

        cur.execute(
            f"UPDATE users SET points = {new_points} WHERE username = '{username}'"
        )
        conn.commit()

        return jsonify({"points": new_points})
    except Exception as e:
        print(e)
        return f"An error occurred: {str(e)}", 500


@app.route("/send_points", methods=["POST"])
def send_points():
    try:
        data = request.get_json()
        print(data)
        username = data.get("username")
        sender = data.get("sender")
        amount = int(data.get("amount"))

        if not username or not amount:
            return (
                jsonify(
                    {
                        "message": "Invalid request. Please provide both username and amount."
                    }
                ),
                400,
            )

        cur.execute("SELECT points FROM users WHERE username = ?", (sender,))
        sender_points = cur.fetchone()

        if sender_points is None:
            return jsonify({"message": "User not found."}), 404

        sender_current_points = sender_points[0]

        if sender_current_points < amount:
            return jsonify({"message": "Insufficient points."}), 400

        sender_new_points = sender_current_points - amount
        sender_new_points = sender_new_points + (sender_new_points*0.05)
        sender_new_points = format(sender_new_points, '.2f')
        cur.execute(
            "UPDATE users SET points = ? WHERE username = ?",
            (sender_new_points, sender),
        )

        cur.execute(
            "INSERT INTO transaction_history (username, transaction_amount,transaction_date) VALUES (?, ?,?)",
            (sender, -amount, datetime.now().strftime("%d-%m-%Y %H:%M:%S")),
        )

        # --------------------------------------------------------------

        cur.execute("SELECT points FROM users WHERE username = ?", (username,))
        reciever_points = cur.fetchone()

        if reciever_points is None:
            return jsonify({"message": "User not found."}), 404

        reciever_current_points = reciever_points[0]

        reciever_new_points = reciever_current_points + amount
        cur.execute(
            "UPDATE users SET points = ? WHERE username = ?",
            (reciever_new_points, username),
        )

        cur.execute(
            "INSERT INTO transaction_history (username, transaction_amount,transaction_date) VALUES (?, ?,?)",
            (username, amount, datetime.now()),
        )

        conn.commit()

        return jsonify({"message": "Points sent successfully."})

    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred.", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
