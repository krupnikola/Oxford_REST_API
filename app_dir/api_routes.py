from flask import jsonify, make_response, request
from app_dir import app, db
from app_dir.models import Word, Sentence
from app_dir.req import find_sentences


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'URL not found'}), 404)


@app.route('/api/words/', methods=['GET'])
def return_words():
    word_object_list = Word.query.all()
    word_list = [item.text for item in word_object_list]

    return jsonify({'words in db': word_list})


@app.route('/api/words/<word>/sentences/', methods=['GET'])
def return_sentences(word):
    word_object_list = Word.query.all()
    word_list = [item.text for item in word_object_list]
    if word in word_list:
        sentences_object_list = Word.query.filter_by(text=word).first().sentences.all()
        sentence_list = [item.body for item in sentences_object_list]

        return jsonify({'sentences for a given word: ' + word: sentence_list})
    else:
        return jsonify({word: "Word is not in the database, try adding it."})


@app.route('/api/words/', methods=['POST'])
def add_word():
    new_word = request.json["new_word"]
    lang = request.json['lang']
    sentences_list = find_sentences(new_word, lang)
    if isinstance(sentences_list, str):
        return jsonify({new_word: "This word does not exist in the dictionary."})
    new_entry = Word(text=new_word)
    db.session.add(new_entry)
    for sentence in sentences_list:
        new_sentence = Sentence(body=sentence, keyword=new_entry)
        db.session.add(new_sentence)
    db.session.commit()
    word_object_list = Word.query.all()
    word_list = [item.text for item in word_object_list]

    return jsonify({'words in db': word_list})


@app.route('/api/words/<word>/', methods=['POST'])
def add_custom_sentence(word):
    new_sentence = request.json['new_sentence']
    word_id = Word.query.filter_by(text=word).first().id
    new_entry = Sentence(body=new_sentence, word_id=word_id)
    db.session.add(new_entry)
    db.session.commit()
    sentences_object_list = Word.query.filter_by(text=word).first().sentences.all()
    sentence_list = [item.body for item in sentences_object_list]

    return jsonify({'sentences for a given word: ' + word: sentence_list})


@app.route('/api/words/<word>/', methods=['DELETE'])
def delete_word_and_sentences(word):
    word_to_remove = Word.query.filter_by(text=word).first()
    sentences_to_remove = Sentence.query.filter_by(keyword=word_to_remove).all()
    for sentence in sentences_to_remove:
        db.session.delete(sentence)
    db.session.delete(word_to_remove)
    db.session.commit()

    word_object_list = Word.query.all()
    word_list = [item.text for item in word_object_list]

    return jsonify({'words in db': word_list})
