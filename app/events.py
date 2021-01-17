from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
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
                (event, description, time, location, g.user['id'], "")
            )
            db.commit()
            return redirect(url_for('events.index'))

    return render_template('events/create.html')

def get_post(id, check_author=False):
    post = get_db().execute(
        'SELECT p.id, event, description, time, location, created, author_id, username, regs_id'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post
def get_user(id):
    user = get_db().execute(
        'SELECT u.id, username FROM user u WHERE u.id = ?',
        (id,)
    ).fetchone()
    return user
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
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
                (event, description, time, location, id,)
            )
            db.commit()
            return redirect(url_for('events.index'))

    return render_template('events/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('events.index'))

@bp.route('/<int:id>', methods=('GET', 'POST'))
def display_events(id):
    post = get_post(id)
    if len(post["regs_id"]) > 0:
        user_ids = post["regs_id"].split(",")
        users = []
        for u in user_ids:
            users.append(get_user(int(u)))
    else:
        users = []
    return render_template('events/event.html', users=users, post=post)


@bp.route('/<int:id>/register', methods=('POST', ))
def register(id):
    post = get_post(id)
    if request.method == 'POST':
        reg_id = g.user['id']

        error = None

        if error is not None:
            flash(error)
            return render_template('events/event.html', post=post)
        else:
            db = get_db()
            ids = post['regs_id'].split(",")
            if len(post['regs_id']) == 0:
                ids_string = reg_id
            elif len(ids) > 5:
                flash("No more space!")
                return render_template('events/event.html', post=post)

            else:
                for i in ids:
                        if str(i) == str(reg_id):
                                flash("Already registered!")
                                return render_template('events/event.html', post=post)               
                ids.append(reg_id)
                ids_string = ",".join(str(x) for x in ids)
            db.execute(
                'UPDATE post SET regs_id = ?'
                ' WHERE id = ?',
                (ids_string,id,)
            )
            post_id = post["id"]
            if  g.user['events_id'] is None:
                event_ids = str(post_id)
            else:
                event_ids = str(g.user['events_id']) + "," + str(post_id)
            db.execute(
                'UPDATE user SET events_id = ?'
                ' WHERE id = ?',
                (event_ids, g.user["id"])
            )
            db.commit()
            flash("Registered!")
    return render_template('events/event.html', post=post)
