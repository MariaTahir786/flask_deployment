from app import app
from flask import Flask, render_template, request, redirect, flash, session

from app.models.chore_model import Chores
from app.models.user_model import User


# @app.route('/chore/<int:chore_id>')
# def get_chore(chore_id):
#     return render_template('/chores/view_chores.html', chore = Chores.get_one_chore(chore_id))

@app.route('/chore/<int:chore_id>')
def get_chore(chore_id):
    return render_template('/chores/view_chores.html', chore = Chores.get_one_with_likes(chore_id))


@app.route('/chore/my')
def my_chores():

    if not 'user_id' in session:
        return redirect('/')

    return render_template('/chores/my_chores.html', user = User.get_one_by_id(session['user_id']))

@app.route('/chore/add')
def get_add_chore_form():
    if not 'user_id' in session:
        return redirect('/')
    return render_template('/chores/add_chore.html')

@app.route('/chore/add', methods=['POST'])
def add_chore():
    if not 'user_id' in session:
        return redirect('/')

    # form = request.form
    # form['user_id'] = session['user_id']
    # Chore.create_chore(form)

    Chores.create_chore({
        **request.form,
        'user_id': session['user_id']
    })
    flash("Chore Added")
    return redirect('/chore/my')

@app.route('/chore/update/<int:chore_id>')
def get_update_chore_form(chore_id):
    if not 'user_id' in session:
        return redirect('/')
    return render_template('/chores/update_chore.html', chore = Chores.get_one_chore(chore_id))


@app.route('/chore/update', methods=['POST'])
def update_chore():
    if not 'user_id' in session:
        return redirect('/')

    Chores.update_chore(request.form)
    flash("Chore Updated")

    return redirect('/chore/my')

@app.route('/chore/delete/<int:chore_id>')
def delete(chore_id):
        Chores.delete_chore(chore_id)
        return redirect('/chore/my')
    
@app.route('/chore/like/<int:chore_id>')
def like_chore(chore_id):
    if not 'user_id' in session:
        return redirect('/')
    Chores.add_like(chore_id, int(session['user_id']))
    return redirect('/user/dashboard')