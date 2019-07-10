#!/usr/bin/env python3

import logging
import os
from pathlib import Path

from flask import Flask

import instagram_downloader as igdl

app = Flask(__name__)

def setup_log() -> None:
    ''' Setup project logger '''
    filepath = os.path.join(Path.cwd(), 'osint_result.log')
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s',
        filename=filepath,
        filemode='w' #clear everytime
    )


@app.route('/api/photos/<string:id>')
def get_photo(id: str) -> str:
    return igdl.get_image(id)


if __name__ == "__main__":
    setup_log()
    app.run(host='0.0.0.0')
