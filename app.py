import os

from flask import Flask, jsonify

from database.db import init_db
from routes.upload_route import upload_bp
from routes.download_route import download_bp

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

init_db()

app.register_blueprint(upload_bp, url_prefix='/uploads')
app.register_blueprint(download_bp, url_prefix='/downloads')


@app.route('/', methods=['GET'])
def index():
    """Rota raiz: confirma que a API está no ar e lista os endpoints."""
    return jsonify({
        "status": "online",
        "api": "Upload e Download de arquivos",
        "endpoints": {
            "upload": "POST /uploads/upload (form-data, campo 'file')",
            "download": "GET /downloads/download/<nome_do_arquivo>"
        }
    })


if __name__ == '__main__':
    # Uso local. Em produção (Render) a aplicação é iniciada pelo gunicorn.
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=port, debug=debug)
