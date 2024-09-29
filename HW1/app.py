from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

# MySQL 連接設定
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Weihan195413",
    database="db"
)

@app.route('/')
def index():
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM hw1")
    users = cursor.fetchall()
    cursor.close()
    return render_template('index.html', users=users)  # 傳遞使用者資料到前端

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        phone = request.form['phone']
        experience = request.form['experience']

        cursor = db.cursor()
        cursor.execute("INSERT INTO hw1 (name, age, email, phone, experience) VALUES (%s, %s, %s, %s, %s)",
                       (name, age, email, phone, experience))
        db.commit()
        cursor.close()

        return redirect('/')  # 提交後重定向到首頁

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM hw1 WHERE id = %s", (user_id,))
    db.commit()
    cursor.close()
    return redirect('/')  # 刪除後重定向到首頁

if __name__ == '__main__':
    app.run(debug=True)
