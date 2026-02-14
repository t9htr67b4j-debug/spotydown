# -*- coding: utf-8 -*-
import os
import subprocess
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # لضمان اتصال الواجهة بالمحرك بدون قيود

# إنشاء مجلد للتنزيلات إذا لم يكن موجوداً
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/download', method=['POST'])
def download_music():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # تنظيف المجلد قبل البدء لتسريع العملية
        for f in os.listdir(DOWNLOAD_FOLDER):
            os.remove(os.path.join(DOWNLOAD_FOLDER, f))

        # أمر التحميل باستخدام spotdl (أسرع طريقة في العالم)
        # سيتم التحميل مباشرة داخل مجلد downloads
        command = f'spotdl {url} --output {DOWNLOAD_FOLDER}'
        
        # تنفيذ الأمر وانتظار انتهائه
        subprocess.check_call(command, shell=True)

        # البحث عن الملف المحمل لإرساله
        files = os.listdir(DOWNLOAD_FOLDER)
        if files:
            file_path = os.path.join(DOWNLOAD_FOLDER, files[0])
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "Failed to download"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("---")
    print("🚀 SpotyDown INFINITY Engine is Active!")
    print("🔗 المحرك يعمل الآن.. لا تغلق هذه النافذة")
    print("---")
    app.run(port=5000, debug=True)