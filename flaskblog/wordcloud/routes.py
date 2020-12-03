from flask import render_template, url_for, flash, Blueprint
from flaskblog.wordcloud.forms import WordCloudPostForm
from flaskblog.wordcloud.word_cloud import WordCloudFromTweet


wordcloud = Blueprint('wordcloud', __name__)


@wordcloud.route('/wordcloud/', methods=['GET', 'POST'])
@wordcloud.route('/wordcloud/search', methods=['GET', 'POST'])
def search():
    form = WordCloudPostForm()
    if form.validate_on_submit():
        word = form.word.data
        utc = WordCloudFromTweet().make(word)
        if utc is not None:
            image_file = url_for('static', filename=f'wordcloud_{utc}.jpg')
            flash('Done!!', 'success')
        else:
            image_file = url_for('static', filename='shape/twitter_shape.jpg')
            flash('Failed!!', 'failed')
        # return redirect(url_for('main.home'))
    else:
        image_file = url_for('static', filename='shape/twitter_shape.jpg')
    return render_template('wordcloud.html', title='Use Word Cloud',
                           form=form, legend='Use Word Cloud', image_file=image_file)
