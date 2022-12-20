from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.post import Post
from flask_app.models.user  import User
from flask_app.models.comment import Comment


@app.route('/createPost', methods=['POST'])
def createPost():

    if not Post.validate_post(request.form):
        return redirect(request.referrer)
    data = {
        'content': request.form['content'],
        'user_id': session['user_id']
    }
    Post.create_post(data)
    return redirect(request.referrer)

@app.route('/like/<int:id>')
def addLike(id):
    data = {
        'post_id': id,
        'user_id': session['user_id']
    }
    Post.addLike(data)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def removeLike(id):
    data = {
        'post_id': id,
        'user_id': session['user_id']
    }
    Post.removeLike(data)
    return redirect(request.referrer)

@app.route('/destroyPost/<int:id>')
def destroyPost(id):
    data = {
        'post_id': id,
        'user_id': session['user_id']
    }
    post = Post.get_post_by_id(data)
    if session['user_id']==post['user_id']:
        Post.deleteAllLikes(data)
        Post.destroyPost(data)
        return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/post/<int:id>/create_comment', methods=['POST'])
def create_comment(id):

    if not Comment.validate_comment(request.form):
        return redirect(request.referrer)
    data = {
        'answer': request.form['answer'],
        'user_id': session['user_id'],
        'post_id': id
    }
    Comment.create_comment(data)
    return redirect(request.referrer)


@app.route('/destroy_comment/<int:id>')
def destroy_comment(id):
    data = {
        'user_id': session['user_id'],
        'comment_id':id
    }
    comment = Comment.get_comment_by_id(data)
    if session['user_id']==comment['comment_id']:
        Comment.destroy_comment(data)
        return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/editpostPage/<int:id>/update_post', methods = ['POST'])
def update_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'user_id': session['user_id'],
        'content': request.form['content'],
        'post_id': id
    }
    post = Post.get_post_by_id(data)
    if data['content'] == '':
        data['content']=post['content']

    Post.update_post(data)
    return redirect(request.referrer)
