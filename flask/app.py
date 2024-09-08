from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config.Config')
mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()
    cursor.close()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:id>')
def post(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    cursor.close()
    return render_template('post.html', post=post)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('index'))
    return render_template('edit.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (title, content, id))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('post', id=id))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    cursor.close()
    return render_template('edit.html', post=post)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        search_type = request.form['search_type']
        query = "SELECT * FROM posts WHERE {} LIKE %s".format('title' if search_type == 'title' else 'content' if search_type == 'content' else 'title OR content')
        cursor = mysql.connection.cursor()
        cursor.execute(query, ('%' + search_term + '%',))
        posts = cursor.fetchall()
        cursor.close()
        return render_template('index.html', posts=posts)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
