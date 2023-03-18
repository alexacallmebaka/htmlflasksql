#import the relevant stuff.
from flask import redirect, render_template, request, url_for, Flask
from db import get_db, init_app
from os import path, makedirs

#app setup
app = Flask(__name__, instance_relative_config=True)
init_app(app)
app.config.from_mapping(DATABASE=path.join(app.instance_path, 'todo.db'))

#ensure the instance folder exists
if not path.isdir(app.instance_path):
    makedirs(app.instance_path)

@app.route('/')
def show_todo():
    #the database connection.
    db=get_db()

    #get all todos from the database and pass them to the template.
    todos = db.execute('SELECT * FROM todo').fetchall() 
    return render_template('todo.html', todos=todos)

@app.route('/add', methods=('GET', 'POST'))
def add_todo():
    #if post, then insert data from form into db.
    if request.method == 'POST':
        db = get_db()
        db.execute('INSERT INTO todo (task_name) VALUES (?)', (request.form['name'],))

        #write changes to db.
        db.commit()

        return redirect(url_for('show_todo'))

    #if not post, then show add_todo page.
    return render_template('add_todo.html')

#edit task from todo list.
@app.route('/edit', methods=('GET', 'POST'))
def edit_todo():
    #if post, then update db with data from form.
    if request.method == 'POST':
        db = get_db()

        #update task by id.
        db.execute('UPDATE todo SET task_name=? WHERE id=?', (request.form['name'], request.form['id']))

        #write changes to db.
        db.commit()

        return redirect(url_for('show_todo'))

    #if not post, then show edit_todo page.
    return render_template('edit_todo.html')

#delete task from todo list.
@app.route('/delete', methods=('GET', 'POST'))
def del_todo():

    #if post, delete task from db.
    if request.method == 'POST':
        db = get_db()

        #delete by id.
        db.execute('DELETE from todo WHERE id=?', (request.form['id'],))

        #write changes to db.
        db.commit()
        return redirect(url_for('show_todo'))

    #if not post, then show del_todo page.
    return render_template('del_todo.html')

if __name__ == '__main__':
    #default to showing the todos.
    show_todo()
