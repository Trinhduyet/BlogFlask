from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post,Comment
from flaskblog.posts.forms import PostForm,CommentForm
from flask_jwt import jwt_required

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=["GET", "POST"])
#@jwt_required()
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


# @posts.route("/post/<string:post_id>", methods=["GET", "POST"])
# def post(post_id):
     
#     sql = db.text("SELECT * FROM Post WHERE id={}".format(post_id))
#     posts = Post.query.get_or_404(post_id)
#     post = db.session.query(Post).from_statement(sql).first()
#     comment = Comment.query.filter_by(post_id=post_id).all()
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment = Comment(author=form.author.data, content=form.content.data,
#                     post_id=post_id)
#         db.session.add(comment)
#         db.session.commit()
#         flash("Your post has been created", 'success')
       
#     #post = Post.query.get_or_404(post_id)
#     return render_template('post.html', title=post.title, post=post, posts=posts,comments=comment,form=form)

@posts.route("/post/<string:post_id>")
def post(post_id):
    sql = db.text("SELECT * FROM Post WHERE id={}".format(post_id))
    post = db.session.query(Post).from_statement(sql).first()
    form = CommentForm()
    comment = Comment.query.filter_by(post_id=post_id).all()
    #post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post,comments=comment,form=form)



@posts.route('/search')
def search():
    query = request.args['query']
    page = request.args.get('page', 1, type=int)
    # posts = Post.query.filter(Post.title.endswith(query)).paginate(page=page, per_page=2)

    search = "%{}%".format(query)
    posts = Post.query.filter(Post.title.like(search)).paginate(page=page, per_page=2)
    return render_template('home.html', posts=posts,query=query)



@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
