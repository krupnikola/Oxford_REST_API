from app_dir import db


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(30), unique=True, nullable=False)
    sentences = db.relationship('Sentence', backref='keyword', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.text)


class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(350), unique=True, nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)

    def __repr__(self):
        return '{}'.format(self.body)
