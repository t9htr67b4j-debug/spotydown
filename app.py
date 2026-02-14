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
        # 1. تنظيف أي ملفات mp3 قديمة لعدم حدوث تداخل
        for f in glob.glob("*.mp3"):
            os.remove(f)

        # 2. تشغيل أمر التحميل
        # استخدمنا أمر بسيط يضمن تحميل الأغنية في المجلد الحالي
        subprocess.run(['spotdl', url], check=True)

        # 3. البحث عن الملف الذي تم تحميله (أي ملف ينتهي بـ .mp3)
        mp3_files = glob.glob("*.mp3")
        
        if mp3_files:
            target_file = mp3_files[0]
            return send_file(target_file, as_attachment=True)
        else:
            return {"error": "لم يتم العثور على ملف الموسيقى بعد التحميل"}, 404

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    # Render يحدد المنفذ تلقائياً عبر متغير البيئة PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
