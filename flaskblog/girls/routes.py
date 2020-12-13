from flask import render_template, url_for, flash, Blueprint
from flaskblog.girls.forms import GirlsGeneratePostForm
from flaskblog.girls.utils import get_available_gpus


girls = Blueprint('girls', __name__)


@girls.route('/girls/', methods=['GET', 'POST'])
@girls.route('/girls/generate', methods=['GET', 'POST'])
def search():
    form = GirlsGeneratePostForm()
    if form.validate_on_submit():
        gpus = get_available_gpus()
        if len(gpus) > 1:
            flash('Done!!', 'success')
            image_file = url_for('static', filename='hatena.jpg')
        else:
            flash('Sorry, This Application Server cannot use GPU', 'failed')
            image_file = url_for('static', filename='hatena.jpg')
    else:
        image_file = url_for('static', filename='hatena.jpg')
    return render_template('girls.html', title='Girls Generator',
                           form=form, legend='Girls Generator', image_file=image_file)
