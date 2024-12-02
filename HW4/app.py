from flask import Flask, render_template, request, redirect, url_for, flash
from bson.objectid import ObjectId
from db_utils import MongoDB

app = Flask(__name__)
app.secret_key = 'your_secret_key'
db = MongoDB()

@app.route('/')
def index():
    items = db.get_all_items()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form.get('name', '').strip()
    value = request.form.get('value', '').strip()
    if not name or not value.isdigit():
        flash('Invalid input. Please provide a valid name and numeric value.')
        return redirect(url_for('index'))
    
    db.insert_item({'name': name, 'value': int(value)})
    flash('Item added successfully!')
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_item(id):
    if request.method == 'GET':
        item = db.get_item_by_id(id)
        if not item:
            flash('Item not found!')
            return redirect(url_for('index'))
        return render_template('edit.html', item=item)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        value = request.form.get('value', '').strip()
        if not name or not value.isdigit():
            flash('Invalid input. Please provide a valid name and numeric value.')
            return redirect(url_for('edit_item', id=id))
        
        db.update_item(id, {'name': name, 'value': int(value)})
        flash('Item updated successfully!')
        return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete_item(id):
    if db.delete_item(id):
        flash('Item deleted successfully!')
    else:
        flash('Failed to delete item.')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
