from flask import Flask, request, send_file, jsonify
import io
from picflip.processing import remove_background_bytes, convert_image_bytes

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "flipflop api!",
        "endpoints": {
            "POST /remove-bg": "Upload an image to remove background",
            "POST /convert/<format>": "Upload an image and convert it to given format"
        }
    })

@app.route('/remove-bg', methods=['POST'])
def api_remove_bg():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    input_bytes = file.read()

    try:
        output_bytes = remove_background_bytes(input_bytes)
        return send_file(
            io.BytesIO(output_bytes),
            mimetype='image/png',
            as_attachment=False,
            download_name='output.png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/convert/<fmt>', methods=['POST'])
def api_convert(fmt):
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    input_bytes = file.read()

    try:
        output_bytes = convert_image_bytes(input_bytes, fmt)
        mime = f"image/{'jpeg' if fmt in ['jpg', 'jpeg'] else fmt}"
        return send_file(
            io.BytesIO(output_bytes),
            mimetype=mime,
            as_attachment=False,
            download_name=f'output.{fmt}'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
