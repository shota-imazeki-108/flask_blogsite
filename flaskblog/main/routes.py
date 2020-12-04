from flask import render_template, Blueprint
import markdown


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    readme_file = open("flaskblog/markdown/ABOUT.md", "r")
    md_to_html = markdown.markdown(readme_file.read(), encoding="utf8")

    return render_template('about.html', about=md_to_html)
