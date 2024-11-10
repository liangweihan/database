from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# 連接 MongoDB 資料庫
client = MongoClient("mongodb://localhost:27017/")
db = client['hw3']  # 這是你的 MongoDB 資料庫名稱
collection = db['testCollection']  # 這是你的 MongoDB 集合名稱

@app.route('/')
def index():
    # 查詢 MongoDB 中所有資料
    items = collection.find()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        value = request.form['value']
        # 將資料插入 MongoDB
        collection.insert_one({'name': name, 'value': int(value)})
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
