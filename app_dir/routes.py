from flask import render_template, flash, redirect, url_for, session, current_app
from app_dir.forms import RequestedWord
from app_dir import app, req, db
from app_dir.models import Word, Sentence


@app.route('/', methods=['GET', 'POST'])
def index():
    form = RequestedWord()
    if form.validate_on_submit():
        input_word = form.word.data
        input_language = form.language.data
        if Word.query.filter_by(text=input_word).first() is not None:
            sentence_object_list = Word.query.filter_by(text=input_word).first().sentences.all()
            sentences_list = [item.body for item in sentence_object_list]
        else:
            if 'API_KEY' not in current_app.config or not current_app.config['API_KEY']:
                return '<h3>Oxford live dictionary service is not configured!</h3>'
            new_word = Word(text=input_word)
            db.session.add(new_word)
            sentences_list = req.find_sentences(input_word, input_language)
            if isinstance(sentences_list, str):
                return render_template('results.html', title='Results', word=form.word.data, lang=form.language.data)
            for sentence in sentences_list:
                new_sentence = Sentence(body=sentence, keyword=new_word)
                db.session.add(new_sentence)
            db.session.commit()

        session['sentences'] = sentences_list
        return redirect(url_for('result'))
    return render_template('index.html', title='Home', form=form)


@app.route('/results/', methods=['GET', 'POST'])
def result():
    sentences = session.get('sentences')
    return render_template('results.html', title='Results', sentences=sentences)

