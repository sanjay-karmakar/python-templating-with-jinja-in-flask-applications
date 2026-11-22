from flask import Flask, render_template
import requests
from post import Post

app = Flask(__name__)

blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
response = requests.get(blog_url).json()
all_posts = []
for post in response:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    all_posts.append(post_obj)


@app.route('/')
def home():
    return render_template("index.html", posts=all_posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route("/post/<int:blog_id>")
def post(blog_id):
    requested_post = None
    for post in all_posts:
        if post.id == blog_id:
            requested_post = post
            break
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
