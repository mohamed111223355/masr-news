import requests
import xml.etree.ElementTree as ET
import os
import google.generativeai as genai
from datetime import datetime

# 1. استلام مفتاح الأمان من خزنة السيرفر
api_key = os.environ.get("GEMINI_API_KEY")

# إعداد الذكاء الاصطناعي لو المفتاح موجود
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
else:
    print("⚠️ تنبيه: لم يتم العثور على مفتاح API. سيتم جلب العناوين فقط.")

rss_url = "https://news.google.com/rss?ceid=EG:ar&hl=ar&gl=EG"

def create_masterpiece():
    print("⏳ بدء تشغيل غرفة الأخبار الذكية...")
    
    try:
        response = requests.get(rss_url)
        root = ET.fromstring(response.content)
        items = root.findall('.//item')
        
        # توقيت القاهرة
        now = datetime.now().strftime("%I:%M %p | %Y-%m-%d")
        
        # --- بداية تصميم الموقع (HTML + CSS الاحترافي) ---
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>مصر الآن - تغطية ذكية</title>
            <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
            <style>
                :root {{ --primary: #c0392b; --dark: #2c3e50; --light: #ecf0f1; }}
                body {{ font-family: 'Cairo', sans-serif; background-color: #f4f7f6; margin: 0; padding: 0; color: #333; }}
                header {{ background: linear-gradient(135deg, #2c3e50, #000); color: white; padding: 40px 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
                header h1 {{ margin: 0; font-size: 2.5em; letter-spacing: 1px; }}
                header p {{ color: #bdc3c7; margin-top: 10px; font-size: 1.1em; }}
                .container {{ max-width: 1100px; margin: -30px auto 40px; padding: 0 20px; display: grid; gap: 30px; }}
                
                .news-card {{ background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.05); transition: transform 0.3s ease; position: relative; }}
                .news-card:hover {{ transform: translateY(-7px); box-shadow: 0 15px 35px rgba(0,0,0,0.15); }}
                .card-header {{ background: var(--primary); color: white; padding: 5px 15px; font-size: 0.8em; display: inline-block; border-radius: 0 0 10px 0; }}
                .card-body {{ padding: 25px; }}
                h2 {{ color: var(--dark); font-size: 1.4em; margin-top: 10px; line-height: 1.4; }}
                .meta {{ color: #7f8c8d; font-size: 0.9em; margin-bottom: 20px; display: block; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
                
                .ai-section {{ background: #fdf2f2; border-right: 4px solid var(--primary); padding: 20px; border-radius: 8px; margin-top: 15px; }}
                .ai-label {{ font-weight: bold; color: var(--primary); display: flex; align-items: center; gap: 5px; margin-bottom: 10px; }}
                .ai-text {{ line-height: 1.8; color: #444; font-size: 1.05em; }}
                
                .footer {{ text-align: center; padding: 20px; color: #7f8c8d; font-size: 0.9em; margin-top: 50px; border-top: 1px solid #ddd; }}
                .source-link {{ display: inline-block; margin-top: 20px; text-decoration: none; color: var(--dark); font-weight: bold; border-bottom: 2px solid var(--primary); transition: color 0.3s; }}
                .source-link:hover {{ color: var(--primary); }}
            </style>
        </head>
        <body>
            <header>
                <h1>🔴 مصر الآن</h1>
                <p>تغطية حية ومقالات فورية بالذكاء الاصطناعي</p>
                <div style="margin-top: 15px; font-size: 0.8em; opacity: 0.8;">⏱️ آخر تحديث: {now} بتوقيت القاهرة</div>
            </header>
            <div class="container">
        """
        
        # --- مصنع المحتوى (Loop) ---
        count = 0
        for item in items:
            if count >= 6: break # كفاية 6 أخبار عشان السرعة
            
            title = item.find('title').text
            pubDate = item.find('pubDate').text
            link = item.find('link').text
            
            print(f"🤖 جاري كتابة التقرير رقم {count+1}: {title[:30]}...")
            
            ai_article = ""
            if api_key:
                try:
                    # الأمر السحري للكاتب
                    prompt = f"""
                    تصرف كصحفي محترف. لدينا هذا العنوان العاجل: "{title}".
                    اكتب مقالاً قصيراً (حوالي 80 كلمة) يلخص الحدث بأسلوب شيق.
                    لا تستخدم مقدمات. ادخل في الموضوع فوراً.
                    """
                    response = model.generate_content(prompt)
                    ai_article = response.text.replace("*", "").replace("#", "")
                except Exception as e:
                    ai_article = "عذراً، المحلل الذكي مشغول حالياً."
                    print(f"خطأ AI: {e}")
            else:
                ai_article = "يرجى إضافة مفتاح API لتفعيل الميزة الذكية."

            html_content += f"""
            <div class="news-card">
                <div class="card-header">خبر عاجل</div>
                <div class="card-body">
                    <h2>{title}</h2>
                    <span class="meta">📅 نُشر في: {pubDate}</span>
                    
                    <div class="ai-section">
                        <div class="ai-label">🤖 تقرير المحلل الذكي:</div>
                        <div class="ai-text">{ai_article}</div>
                    </div>
                    
                    <a href="{link}" target="_blank" class="source-link">🔗 قراءة الخبر الأصلي من المصدر</a>
                </div>
            </div>
            """
            count += 1
            
        html_content += """
            </div>
            <div class="footer">
                &copy; 2026 تم التطوير بواسطة Python & GitHub Actions
            </div>
        </body>
        </html>
        """
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ تمت المهمة بنجاح! الموقع جاهز للنشر.")

    except Exception as e:
        print(f"❌ حدث خطأ جسيم: {e}")

if __name__ == "__main__":
    create_masterpiece()