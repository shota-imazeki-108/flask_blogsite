from flask import render_template, url_for, flash, Blueprint
from flaskblog.girls.forms import GirlsGeneratePostForm
from flaskblog.girls.utils import get_available_gpus
from flaskblog.girls.girls_generator import GirlsGenerator


girls = Blueprint('girls', __name__)


@girls.route('/girls/', methods=['GET', 'POST'])
@girls.route('/girls/generate', methods=['GET', 'POST'])
def search():
    form = GirlsGeneratePostForm()
    if form.validate_on_submit():
        gpus = get_available_gpus()
        if len(gpus) > 0:
            gg = GirlsGenerator()
            utc = gg.generate()  # TODO: psiいじれるようにする
            if utc is not None:
                image_file = url_for('static', filename=f'girls_{utc}.jpg')
                flash('Done!!', 'success')
            else:
                image_file = url_for('static', filename='hatena.jpg')
                flash('Failed!!', 'failed')
        else:
            flash('Sorry, This Application Server cannot use GPU', 'failed')
            image_file = url_for('static', filename='hatena.jpg')
    else:
        image_file = url_for('static', filename='hatena.jpg')
    return render_template('girls.html', title='Girls Generator',
                           form=form, legend='Girls Generator', image_file=image_file)
