from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
import constants
import zlib

app = Flask(__name__)

app.config['SECRET_KEY'] = constants.APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = constants.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
base_path = '/api'
db = SQLAlchemy(app)


class LINKS(db.Model):
    __tablename__ = 'LINKS'
    LINK_ID = db.Column(db.Integer, primary_key=True)
    SHORT_PATH = db.Column(db.String(100))
    FULL_LINK = db.Column(db.String(500))


def resultdata(errorcode, message, result, key):
    return make_response(jsonify({'code': errorcode, 'message': message, 'result': result, 'key': key}), errorcode)


@app.route('/<shortpath>', methods=['GET'])
def init(shortpath):
    link = LINKS.query.filter_by(SHORT_PATH=shortpath).first()
    return render_template('index.html', recUrl=link.FULL_LINK, delay=5)


@app.route('/appshortlink', methods=['POST'])
def addshortlink():
    json = request.json

    if not json or not json['url']:
        return json.resultdata(404, constants.FAILED_MESSAGE, 'URL required', 'COULD_NOT_VERIFY')

    url = bytes(json['url'], 'utf-8')
    shortPath = zlib.adler32(url)
    print(str(shortPath))

    link = LINKS(SHORT_PATH=str(shortPath), FULL_LINK=json['url'])
    db.session.add(link)
    db.session.commit()

    return resultdata(200, constants.SUCCESS_MESSAGE, shortPath, 'CREATE_SHORT_LINK')


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run()
