import os

from flask import Flask, request, send_file, jsonify, make_response
import tempfile
import os
from ip_info_output import main
from draw import generate_image

app = Flask(__name__)


@app.route('/', methods=['POST'])
def serve_image():
    try:
        body = request.get_json()
        for i in ['ip', 'mask']:
            if i not in body:
                return make_response(jsonify({'error': f'Missing required field: {i}'}), 400)

        ip, mask = body['ip'], body['mask']
        ip_output = main(ip, mask)

        if ip_output:
            image_path = generate_image(ip_output, draft=True, position=(145, 285, 315, 330))
            return send_file(image_path, mimetype='image/jpeg')
        else:
            return make_response(jsonify({'status': 'host seems down'}), 200)

    except Exception as e:
        return make_response(jsonify({'error': f'An error has occurred: {e}'}), 500)


if __name__ == '__main__':
    tmp_windows_path = tempfile.gettempdir()
    tmp_files = os.listdir(tmp_windows_path)

    for file in [tmp for tmp in tmp_files if 'blk.jpg' in tmp]:
        os.unlink(rf'{tmp_windows_path}/{file}')

    app.run(debug=True, port=8080)
