from flask import Flask, render_template, request, redirect, url_for  # 確保這些導入存在
from flask_caching import Cache
from database import db
from join import join_bp

app = Flask(__name__)

# 配置快取
app.config['CACHE_TYPE'] = 'simple'  # 使用簡單的快取類型
cache = Cache(app)  # 初始化快取

app.register_blueprint(join_bp)

@app.route('/')
def index():
    cursor = db.cursor()
    
    # 查詢各表格資料
    cursor.execute("SELECT * FROM personal_info")
    personal_info = cursor.fetchall()
    
    cursor.execute("SELECT * FROM experience")
    experience = cursor.fetchall()
    
    cursor.execute("SELECT * FROM status")
    status = cursor.fetchall()
    
    # 將資料轉換為字典形式，方便模板使用
    personal_info_dict = [{'id': p[0], 'name': p[1], 'gender': p[2], 'age': p[3], 'phone': p[4], 'email': p[5]} for p in personal_info]
    experience_dict = [{'id': e[0], 'user_id': e[1], 'experience_details': e[2]} for e in experience]
    status_dict = [{'record_id': s[0], 'user_id': s[1], 'status': s[2]} for s in status]
    
    cursor.close()
    return render_template('index.html', personal_info=personal_info_dict, experience=experience_dict, status=status_dict)

# 新增資料
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    gender = request.form['gender']
    age = request.form['age']
    phone = request.form['phone']
    email = request.form['email']
    experience_details = request.form['experience_details']
    
    cursor = db.cursor()
    
    try:
        # 插入 personal_info 資料
        cursor.execute("INSERT INTO personal_info (name, gender, age, phone, email) VALUES (%s, %s, %s, %s, %s)",
                       (name, gender, age, phone, email))
        user_id = cursor.lastrowid
        
        # 插入 experience 資料
        cursor.execute("INSERT INTO experience (user_id, experience_details) VALUES (%s, %s)", (user_id, experience_details))
        
        # 插入 status 資料，預設狀態為 "未處理"
        cursor.execute("INSERT INTO status (user_id, status) VALUES (%s, '未處理')", (user_id,))
        
        db.commit()
    except Exception as e:
        db.rollback()
        cursor.close()
        print(f"新增資料時發生錯誤: {str(e)}")  # 方便調試
        return f"新增資料時發生錯誤: {str(e)}", 500
    
    cursor.close()
    return redirect(url_for('index'))

# 更新個人資料
@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form['id']
    name = request.form['name']
    gender = request.form['gender']
    age = request.form['age']
    phone = request.form['phone']
    email = request.form['email']
    
    cursor = db.cursor()
    
    try:
        # 更新 personal_info 資料
        cursor.execute("UPDATE personal_info SET name=%s, gender=%s, age=%s, phone=%s, email=%s WHERE id=%s",
                       (name, gender, age, phone, email, user_id))
        db.commit()
    except Exception as e:
        db.rollback()
        cursor.close()
        print(f"更新資料時發生錯誤: {str(e)}")  # 方便調試
        return f"更新資料時發生錯誤: {str(e)}", 500
    
    cursor.close()
    return redirect(url_for('index'))

# 更新工作經驗
@app.route('/update_experience', methods=['POST'])
def update_experience():
    experience_id = request.form['id']
    experience_details = request.form['experience_details']

    cursor = db.cursor()
    
    try:
        # 更新 experience 資料
        cursor.execute("UPDATE experience SET experience_details=%s WHERE id=%s", (experience_details, experience_id))
        db.commit()
    except Exception as e:
        db.rollback()
        cursor.close()
        print(f"更新工作經驗時發生錯誤: {str(e)}")  # 方便調試
        return f"更新工作經驗時發生錯誤: {str(e)}", 500
    
    cursor.close()
    return redirect(url_for('index'))

# 更新錄取狀態
@app.route('/update_status', methods=['POST'])
def update_status():
    record_id = request.form['record_id']
    status_value = request.form['status']

    cursor = db.cursor()
    
    try:
        # 更新 status 資料
        cursor.execute("UPDATE status SET status=%s WHERE record_id=%s", (status_value, record_id))
        db.commit()
    except Exception as e:
        db.rollback()
        cursor.close()
        print(f"更新錄取狀態時發生錯誤: {str(e)}")  # 方便調試
        return f"更新錄取狀態時發生錯誤: {str(e)}", 500
    
    cursor.close()
    return redirect(url_for('index'))

# 刪除資料
@app.route('/delete/<int:id>')
def delete(id):
    cursor = db.cursor()
    
    try:
        # 刪除 experience、personal_info 和 status 資料
        cursor.execute("DELETE FROM experience WHERE user_id=%s", (id,))
        cursor.execute("DELETE FROM personal_info WHERE id=%s", (id,))
        cursor.execute("DELETE FROM status WHERE user_id=%s", (id,))
        
        db.commit()
    except Exception as e:
        db.rollback()
        cursor.close()
        print(f"刪除資料時發生錯誤: {str(e)}")  # 方便調試
        return f"刪除資料時發生錯誤: {str(e)}", 500
    
    cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
