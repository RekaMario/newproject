from flask_app import app
from flask import render_template ,session ,redirect ,request , jsonify
from flask_app.models import user , post , socialmedia ,comment
from flask_app.models.user import User 
from flask_app.models.post import Post
from flask_app.models.socialmedia import  Socialmedia
from flask_app.models.comment import Comment
from flask import flash
import os
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException, NotFound
import uuid as uuid


UPLOAD_FOLDER = 'flask_app/static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 30*1024*1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
bcrypt = Bcrypt(app)
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def homePage():
    if 'user_id' in session:
        return redirect('/homePageL') 
    return render_template('homePage.html')

@app.route('/eventsPage')
def eventsPage():
    if 'user_id' in session:
        return redirect('/eventsPageL') 
    return render_template('eventsPage.html')

@app.route('/discoverPage')
def discoverPage():
    if 'user_id' in session:
        return redirect('/discoverPageL') 
    return render_template('discoverPage.html')

@app.route('/communityPage')
def communityPage():
    if 'user_id' in session:
        return redirect('/communityPageL') 
    return render_template('communityPage.html')






@app.route('/loginPage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('loginPage.html')

@app.route('/registerPage')
def registerPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('registerPage.html')









@app.route('/homePageL')
def homePageL():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        return render_template('homePageL.html', loggedUser= user)
    return redirect('/')












@app.route('/communityPageL')
def communityPageL():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        allPosts = Post.getAllPosts()
        posts = User.get_all_user_info(data)
        userLikedPosts = User.get_logged_user_liked_posts(data)
        return render_template('communityPageL.html', loggedUser= user,allPosts = allPosts,posts= posts, userLikedPosts= userLikedPosts)
    return redirect('/')


@app.route('/profilePage')
def profilePage():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        posts = User.get_all_user_info(data)
        allPosts = Post.getAllPosts()
        userLikedPosts = User.get_logged_user_liked_posts(data)
        smedia = Socialmedia.get_socialmedia_by_id(data)
        return render_template('profilePage.html', loggedUser= user,allPosts = allPosts ,posts= posts, userLikedPosts= userLikedPosts , smedia= smedia)
    return redirect('/')


@app.route('/editprofilePage')
def editprofilePage():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        smedia = Socialmedia.get_socialmedia_by_id(data)
        return render_template('editprofilePage.html', loggedUser= user , smedia= smedia )
    return redirect('/')


@app.route('/post/<int:id>')
def postview(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'post_id': id,
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    allPosts = Post.getAllPosts()
    allComments = Comment.get_all_comments()
    userLikedPosts = User.get_logged_user_liked_posts(data)
    return render_template('postPage.html', loggedUser= user ,post = Post.get_post_by_id(data),allComments = allComments , allPosts = allPosts,  userLikedPosts= userLikedPosts )


@app.route('/editpostPage/<int:id>')
def postedit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'post_id': id,
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    allPosts = Post.getAllPosts()
    return render_template('editpostPage.html', loggedUser= user ,post = Post.get_post_by_id(data) )


#INSERT INTO socialmedia (facebook, user_id) VALUES('www.google.com', 1);


@app.route('/discoverPageL')
def discoverPageL():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        return render_template('discoverPageL.html', loggedUser= user)
    return redirect('/')



@app.route('/eventsPageL')
def eventsPageL():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        return render_template('eventsPageL.html', loggedUser= user)
    return redirect('/')







@app.route('/create_user', methods=['POST'])
def createUser():
    if not User.validate_user(request.form):
        flash('Somethings wrong!', 'signUp')
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    User.create_user(data)
    return redirect('/')

#POST method to log the user in

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    if len(request.form['email'])<1:
        flash('Email is required to login', 'emailLogin')
        return redirect(request.referrer)
    if not User.get_user_by_email(data):
        flash('This email doesnt exist in this application', 'emailLogin')
        return redirect(request.referrer)

    user = User.get_user_by_email(data)

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password", 'passwordLogin')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect('/homePageL')




@app.route('/upload_pic', methods = ['POST'])
def upload_pic():
    if 'user_id' in session:
        file = request.files['filename']
        if file and allowed_file(file.filename):
            pic_filename = secure_filename(file.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
            data = {
                'profile_pic': pic_name,
                'user_id': session['user_id']
            }
            User.add_profile_pic(data)
            return redirect('/editprofilePage')
        else:
            flash('*This image is not in the right format', 'profile_pic')
            return redirect(request.referrer)
    return redirect('/logout')



@app.route('/update_user', methods = ['POST'])
def update_user():
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'user_id': session['user_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name']
    }
    loggedUser = User.get_user_by_id(data)
    if data['first_name'] == '':
        data['first_name']=loggedUser['first_name']
    elif data['last_name'] == '':
        data['last_name'] = loggedUser['last_name']

    User.update_user(data)
    return redirect('/profilePage')


@app.route('/editprofilePage/create_socialmedia', methods=['POST'])
def create_socialmedia():

    if not Socialmedia.validate_socialmedia(request.form):
        return redirect(request.referrer)
    data = {
        'user_id': session['user_id'],
        'website': request.form['website'],
        'github': request.form['github'],
        'twitter': request.form['twitter'],
        'facebook': request.form['facebook'],
        'linkedin': request.form['linkedin']
        
    }
    Socialmedia.create_socialmedia(data)
    return redirect(request.referrer)


@app.route('/editprofilePage/update_socialmedia', methods = ['POST'])
def update_socialmedia():
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'user_id': session['user_id'],
        'website': request.form['website'],
        'github': request.form['github'],
        'twitter': request.form['twitter'],
        'facebook': request.form['facebook'],
        'linkedin': request.form['linkedin']
    }
    smedia = User.get_user_by_id(data)
    if data['website'] == '':
        data['website']=smedia['website']
    elif data['github'] == '':
        data['github'] = smedia['github']
    if data['twitter'] == '':
        data['twitter']=smedia['twitter']
    elif data['facebook'] == '':
        data['facebook'] = smedia['facebook']
    if data['linkedin'] == '':
        data['linkedin']=smedia['first_name']


    Socialmedia.update_socialmedia(data)
    return redirect(request.referrer)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.route('/404L')
def page_not_foundL():
    return render_template('404L.html')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')