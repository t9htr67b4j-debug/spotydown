# -*- coding: utf-8 -*-
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

        # السر هنا: استخدام --provider-visual لتقليل ضغط البحث التقليدي
        # وإضافة --bitrate لجعل التحميل أسرع
        print(f"Direct Music Engine starting for: {url}")
        
        result = subprocess.run([
            'spotdl', 
            '--format', 'mp3',
            '--bitrate', '128k', # تقليل الجودة قليلاً يجعل السيرفر أسرع بكثير
            '--search-query', '{artist} - {title}',
            '--no-cache',
            url
        ], capture_output=True, text=True)

        # إذا فشل المحرك الأول، نحاول بمحرك الطوارئ (YouTube Music بجودة منخفضة)
        if result.returncode != 0:
            print("Swapping to Emergency Engine...")
            subprocess.run(['spotdl', '--format', 'mp3', '--bitrate', '128k', url], check=True)

        mp3_files = glob.glob("*.mp3")
        if mp3_files:
            return send_file(mp3_files[0], as_attachment=True)
        else:
            return {"error": "المحركات مشغولة حالياً، كرر المحاولة"}, 404

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
