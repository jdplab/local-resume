from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_visitor_count():
    connection = None
    try:
        connection = sqlite3.connect("/mnt/nfs/visitors.db")
        cursor = connection.cursor()
        cursor.execute("SELECT count FROM visitors")
        count = cursor.fetchone()
        cursor.execute("UPDATE visitors SET count = count + 1")
        connection.commit()
        return count
    except Exception as e:
        print("Error:", e)
        count = 0
        return count
    finally:
        if connection:
            connection.close()

@app.route("/")
def index():
    count = get_visitor_count()
    return render_template("index.html", visitor_count=count)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
