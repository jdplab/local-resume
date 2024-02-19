from flask import Flask, render_template, request, send_from_directory
import sqlite3

app = Flask(__name__, static_folder="static")

def get_visitor_count():
    connection = None
    try:
        connection = sqlite3.connect("/mnt/nfs/visitors-prod.db")
        cursor = connection.cursor()
        cursor.execute("SELECT count FROM visitors")
        count = cursor.fetchone()[0]
        cursor.execute("UPDATE visitors SET count = count + 1")
        connection.commit()
        return count
    except Exception as e:
        print("Error:", e)
        return count
    finally:
        if connection:
            connection.close()

def get_unique_visitors():
    connection = None
    uniquevisitors = 0
    try:
        connection = sqlite3.connect("/mnt/nfs/visitors-prod.db")
        cursor = connection.cursor()
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip_address.startswith("10.") or ip_address.startswith("172.") or ip_address.startswith("192."):
            ip_address = "home"
        cursor.execute("CREATE TABLE IF NOT EXISTS uniquevisitors (id INTEGER PRIMARY KEY AUTOINCREMENT, ip_address TEXT, visits INTEGER)")
        cursor.execute("SELECT visits FROM uniquevisitors WHERE ip_address = ?", (ip_address,))
        visits_row = cursor.fetchone()
        if visits_row is not None:
            visits = visits_row[0] + 1
            cursor.execute("UPDATE uniquevisitors SET visits = ? WHERE ip_address = ?", (visits, ip_address,))
            cursor.execute("SELECT COUNT(*) FROM uniquevisitors")
            uniquevisitors = cursor.fetchone()[0]
        else:
            print('Visits = None')
            cursor.execute("INSERT INTO uniquevisitors VALUES (NULL, ?, 1)", (ip_address,))
            cursor.execute("SELECT COUNT(*) FROM uniquevisitors")
            uniquevisitors = cursor.fetchone()[0]
        connection.commit()
        return uniquevisitors
    except Exception as e:
        print("Error:", e)
        return uniquevisitors
    finally:
        if connection:
            connection.close()

def get_visit_count():
    connection = None
    visits = 0
    try:
        connection = sqlite3.connect("/mnt/nfs/visitors-prod.db")
        cursor = connection.cursor()
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip_address.startswith("10.") or ip_address.startswith("172.") or ip_address.startswith("192."):
            ip_address = "home"
        cursor.execute("SELECT visits FROM uniquevisitors WHERE ip_address = ?", (ip_address,))
        visits = cursor.fetchone()[0]
        connection.commit()
        return visits
    except Exception as e:
        print("Error:", e)
        return visits
    finally:
        if connection:
            connection.close()

@app.route("/")
def index():
    count = get_visitor_count()
    uniquevisitors = get_unique_visitors()
    visits = get_visit_count()
    return render_template("index.html", visitor_count=count, unique_visitors=uniquevisitors, user_visits=visits)

@app.route("/JonathanPolanskyResume.docx")
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == "__main__":
    app.run(host="0.0.0.0")
