#!/usr/bin/env python3

import logging
import os
from pathlib import Path

from typing import List
from flask import Flask, jsonify

import instagram_downloader as igdl

app = Flask(__name__)


def setup_log() -> None:
    ''' Setup project logger '''
    filepath = os.path.join(Path.cwd(), 'igdl.log')
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)-15s][%(clientip)s][%(user)-8s] %(message)s',
        filename=filepath,
        filemode='w'
    )


@app.route('/api/photos/<string:id>')
def get_photo(id: str) -> str:
    return jsonify(igdl.get_image(id))


@app.route('/api/profile/<string:username>')
def get_profile_photos(username: str) -> List[str]:
    return jsonify(igdl.get_images(username))


if __name__ == "__main__":
    setup_log()
    app.run(host='0.0.0.0', debug=True)
