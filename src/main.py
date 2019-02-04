from flask import Flask
import igdl

app = Flask(__name__)


@app.route('/api/photos/<string:id>')
def get_photo(id: str) -> str:
    return igdl.get_image(id)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
