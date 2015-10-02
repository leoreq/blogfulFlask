from flask import render_template

from blog import app
from .database import session
from .models import Post

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages,
    )


@app.route("/post/<int:postid>")
def post(postid=1):
    post = session.query(Post).get(postid)
    return render_template("post.html",
        post=post
    )
    
#############This is the post add section############# 
@app.route("/post/add", methods=["GET"])
def add_post_get():
    return render_template("add_post.html",post_title_value="",post_content_value="")

import mistune
from flask import request, redirect, url_for

@app.route("/post/add", methods=["POST"])
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))

#############This is the post edit section############# 
@app.route("/post/<int:postid>/edit", methods=["GET"])
def edit_post_get(postid=1):
    post = session.query(Post).get(postid)
    return render_template("add_post.html",post_title_value=post.title,post_content_value=post.content)

@app.route("/post/<int:postid>/edit", methods=["POST"])
def edit_post_post(postid):
    post = session.query(Post).get(postid)
    #post = Post(
    #    title=request.form["title"],
    #    content=mistune.markdown(request.form["content"]),
    #)
    post.title=request.form["title"]
    post.content=mistune.markdown(request.form["content"])
    session.commit()
    return redirect(url_for("post",postid=postid))

@app.route("/post/<int:postid>/delete", methods=["GET","POST"])
def delete_post_post(postid):
    post = session.query(Post).get(postid)
    session.delete(post)
    session.commit()
    return redirect(url_for("posts"))