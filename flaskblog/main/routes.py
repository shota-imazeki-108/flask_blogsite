from flask import render_template, request, Blueprint
from flaskblog.models import Post
import markdown


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    readme_file = open("flaskblog/markdown/ABOUT.md", "r")
    md_to_html = markdown.markdown(readme_file.read(), encoding="utf8")

    return render_template('about.html', about=md_to_html)
