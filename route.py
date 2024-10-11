from flask import Blueprint, request, redirect, url_for, flash, render_template,jsonify
from werkzeug.utils import secure_filename
import os
from connection import get_connection
import sys

bp = Blueprint('student', __name__, url_prefix='/')

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', data=data,)

@bp.route('/page')
def page():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("Select COUNT(*) from data ")
    total_count = cursor.fetchall()

    rows_per_page = 10

    pages = total_count / rows_per_page
    start = (page - 1) * rows_per_page
    end = start + rows_per_page
    items = [start:end]
    cursor.close()
    connection.close()
    return render_template()
    
     

@bp.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        name = request.form.get('name')
        about = request.form.get('about')
        f = request.files.get('image')

        if f and f.filename:
            if allowed_file(f.filename):
                filename = secure_filename(f.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                f.save(file_path)

                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute("INSERT INTO data (name, image, about) VALUES (%s, %s, %s)", (name, filename, about))
                connection.commit()
                new_id = cursor.lastrowid
                cursor.close()
                connection.close()

        return jsonify({
            'status': 'success',
            'id': new_id,
            'name': name,
            'image': filename,
            'about': about
        })
    else:
        return jsonify({'status': 'error', 'message': 'Failed to upload image or invalid file'})


@bp.route('/update/<int:id>', methods=['POST'])
def update(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    name = request.form.get('name')
    about = request.form.get('about')         
    f = request.files.get('image')

    if f and f.filename:
            if allowed_file(f.filename):
                filename = secure_filename(f.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                f.save(file_path)
                cursor.execute("UPDATE data SET name=%s, image=%s, about=%s WHERE id=%s", (name, filename, about, id))
            else:
                return jsonify({'status': 'error', 'message': 'Invalid file type. Only JPG, JPEG, PNG, and GIF are allowed.'}), 400
    else:
            cursor.execute("UPDATE data SET name=%s, about=%s WHERE id=%s", (name, about, id))
        
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'status': 'success', 'message': 'Data updated successfully!'})
   
    

@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM data WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash('Data deleted successfully!')
    return jsonify({'status': 'success'})

@bp.route('/page',methods=['GET'])
def page():
     connection = get_connection()
     cursor= connection.cursor()
     
     rows_per_page = 10
     offset = (page -1) * rows_per_page
     cursor.execute("Select COUNT(*) from data ")
     total_count = cursor.fetchone()
     pages = total_count / rows_per_page
     next = page+1
     previous = page -1
     if previous<1:
          previous=1
     
     cursor.execute("Select * from data ORDER BY  id LIMIT %s OFFSET %s",(rows_per_page,offset))
     data= cursor.fetchall()

     connection.commit()
     cursor.close()
     connection.close()
     return jsonify({'status': 'sucess'})

























# @app.route('/page', methods=['GET'])
# def page():
#     connection = get_connection()
#     cursor = connection.cursor()
    
#     # Get the page number from the request arguments (default to page 1 if not provided)
#     page = int(request.args.get('page', 1))
#     rows_per_page = 10
    
#     # Calculate the offset
#     offset = (page - 1) * rows_per_page
    
#     # Fetch the total count of rows
#     cursor.execute("SELECT COUNT(*) FROM data")
#     total_count = cursor.fetchone()[0]
    
#     # Calculate the total number of pages
#     pages = (total_count + rows_per_page - 1) // rows_per_page  # Ceiling division
    
#     # Fetch the rows for the current page
#     cursor.execute("SELECT * FROM data ORDER BY id LIMIT %s OFFSET %s", (rows_per_page, offset))
#     data = cursor.fetchall()
    
#     # Close the cursor and connection
#     cursor.close()
#     connection.close()
    
#     # Return the results as JSON
#     return jsonify({
#         'page': page,
#         'total_pages': pages,
#         'total_count': total_count,
#         'data': data
#     })



