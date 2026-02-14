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
        # 1. تنظيف أي ملفات قديمة لمنع تداخل الأغاني
        for f in glob.glob("*.mp3"):
            try: os.remove(f)
            except: pass

        # 2. تشغيل أمر التحميل بإعدادات تخطي الحظر (Rate Limit)
        # أضفنا --format mp3 و إعدادات البحث الذكي لتقليل ضغط الطلبات
        print(f"Starting download for: {url}")
        
        # استخدام subprocess لتنفيذ التحميل
        result = subprocess.run([
            'spotdl', 
            '--format', 'mp3',
            '--search-query', '{artist} - {title}',
            url
        ], capture_output=True, text=True)
        # 3. التأكد من نجاح العملية
        if result.returncode != 0:
            print(f"Spotdl Error: {result.stderr}")
            return {"error": "يوتيوب يفرض قيوداً حالياً، حاول مرة أخرى بعد قليل"}, 500

        # 4. البحث عن الملف الناتج وإرساله
        mp3_files = glob.glob("*.mp3")
        if mp3_files:
            target_file = mp3_files[0]
            print(f"Sending file: {target_file}")
            return send_file(target_file, as_attachment=True)
        else:
            return {"error": "لم يتم العثور على الملف، قد يكون الرابط غير مدعوم"}, 404

    except Exception as e:
        print(f"System Error: {str(e)}")
        return {"error": str(e)}, 500

if __name__ == "__main__":
    # Render يحدد المنفذ تلقائياً
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    
