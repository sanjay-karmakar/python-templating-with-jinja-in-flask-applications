from flask import Flask, render_template, request
import requests
from post import Post
import os
import smtplib
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()


# Get blogs from external link
blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
response = requests.get(blog_url).json()
all_posts = []
for post in response:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    all_posts.append(post_obj)


# Home page
@app.route('/')
def home():
    return render_template("index.html", posts=all_posts)


# About page
@app.route('/about')
def about():
    return render_template("about.html")


# Contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        sendmail(name, email, phone, message)

        # print(name, email, phone, message)
        return render_template("contact.html", msg_sent=True)

    return render_template("contact.html")


# Post page
@app.route("/post/<int:blog_id>")
def post(blog_id):
    requested_post = None
    for post in all_posts:
        if post.id == blog_id:
            requested_post = post
            break
    return render_template("post.html", post=requested_post)



# Send email
def sendmail(name, email, phone, message):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"

        connection.starttls()
        connection.login(
            user=os.environ.get("FROM_EMAIL"),
            password=os.environ.get("PASSWORD")
        )
        connection.sendmail(
            from_addr=os.environ.get("FROM_EMAIL"),
            to_addrs=os.environ.get("TO_EMAIL"),
            msg=email_message
        )


if __name__ == "__main__":
    app.run(debug=True)
