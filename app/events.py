from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('events', __name__, url_prefix='/events')

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, event, description, time, location, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('events/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        event = request.form['event']
        description = request.form['description']
        time = request.form['time']
        location = request.form['location']
        error = None

        if not event:
            error = 'event is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (event, description, time, location, author_id, regs_id)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (event, description, time, location, g.user['id'], "0,0,0,0,0")
            )
            db.commit()
            return redirect(url_for('events.index'))

    return render_template('events/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, event, description, time, location, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        event = request.form['event']
        description = request.form['description']
        time = request.form['time']
        location = request.form['location']
        
        error = None

        if not event:
            error = 'event is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET event = ?, description = ?, time = ?, location = ?'
                ' WHERE id = ?',
                (event, description, time, location, id)
            )
            db.commit()
            return redirect(url_for('events.index'))

    return render_template('events/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('events.index'))

@bp.route('/<int:id>', methods=('GET', 'POST'))
@login_required
def display_events(id):
    post = get_post(id)
    return render_template('events/event.html', post=post)

@bp.route('/<int:id>/register', methods=('POST', ))
def register(id):
    post = get_post(id)
    print(post)
    if request.method == 'POST':
        reg_id = g.user['id']

        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            ids = post['regs_id'].split(",")
            counter = 0
            for i in ids:
                if i == reg_id:
                    flash("Already Registered!")
                    break
                if i == 0:
                    ids[i] = reg_id
                else:
                    counter += 1
                    if counter == 5:
                        flash("No more space!")
                        break

            ids = ",".join(ids)
            db.execute(
                'UPDATE post SET regs_id = ?',
                ids
            )
            db.commit()
            flash("Registered!")
