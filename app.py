# -*- coding: utf-8 -*-
from flask import Flask, request, send_file
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    if not url:
        return {"error": "No URL provided"}, 400

    try:
        # مسار مؤقت للتحميل
        download_path = "music.mp3"
        
        # أمر التحميل باستخدام spotdl
        result = subprocess.run(['spotdl', '--output', download_path, url], capture_code=True)
        
        return send_file(download_path, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    # Render يطلب تشغيل السيرفر على بورت يحدده هو
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
