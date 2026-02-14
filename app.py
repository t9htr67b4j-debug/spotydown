import os
import subprocess
import glob
from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    
    if not url:
        return {"error": "No URL provided"}, 400

    try:
        # تنظيف الملفات القديمة
        for f in glob.glob("*.mp3"):
            try: os.remove(f)
            except: pass

        # تشغيل spotdl مع محاولة تجاهل أخطاء ffmpeg إذا لم تتوفر
        # سيقوم spotdl بتحميل الملف كـ m4a ثم تحويله
        result = subprocess.run(['spotdl', '--format', 'mp3', url], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Spotdl Error: {result.stderr}")
            return {"error": f"فشل التحميل: {result.stderr[:100]}"}, 500

        mp3_files = glob.glob("*.mp3")
        if mp3_files:
            return send_file(mp3_files[0], as_attachment=True)
        
        return {"error": "لم يتم العثور على الملف بعد المعالجة"}, 404

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
