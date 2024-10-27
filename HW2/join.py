from flask import Blueprint, render_template, current_app
from database import db
from flask_caching import Cache

# 創建 join_bp Blueprint
join_bp = Blueprint('join', __name__)

@join_bp.route('/application', methods=['GET'])
def show_application():
    # 清除快取
    cache = Cache(current_app)  # 使用當前應用的快取
    cache.clear()  # 清除所有快取

    cursor = db.cursor()

    query = """
    SELECT 
        personal_info.name, 
        personal_info.gender, 
        personal_info.age, 
        personal_info.phone, 
        personal_info.email, 
        GROUP_CONCAT(experience.experience_details SEPARATOR ', ') AS experience_details, 
        MAX(status.status) AS status  
    FROM 
        personal_info
    JOIN 
        experience ON personal_info.id = experience.user_id
    JOIN 
        status ON personal_info.id = status.user_id
    GROUP BY 
        personal_info.id
    """

    cursor.execute(query)
    join_data = cursor.fetchall()
    
    print("Fetched application data:", join_data)  # Debug line to see fetched data
    
    cursor.close()  # 確保關閉游標以釋放資源
    
    return render_template('application.html', join_data=join_data)
