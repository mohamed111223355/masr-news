import requests
import os
import google.generativeai as genai
from datetime import datetime
import xml.etree.ElementTree as ET
import random

# 1. إعداد المفتاح والاتصال
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')

if not GOOGLE_API_KEY:
    print("❌ Error: API Key is missing!")
    exit(1)

genai.configure(api_key=GOOGLE_API_KEY)

# 2. دالة التحليل الذكي (بتحاول مع كذا موديل عشان ميفشلش)
def get_ai_model():
    # بنجرب الموديل المستقر الأول
    try:
        return genai.GenerativeModel('gemini-pro')
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = get_ai_model()

def get_trending_news():
    print("🌍 جاري جلب الأخبار من Google Trends...")
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=EG"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            news_items = []
            for item in root.findall('.//item'):
                title = item.find('title').text
                # بنجيب رابط الخبر ورابط الصورة لو متاحين
                news_items.append(title)
            return news_items[:6]  # ناخد أهم 6 أخبار
        else:
            print("⚠️ فشل الاتصال بـ Google Trends")
            return []
    except Exception as e:
        print(f"❌ Error fetching trends: {e}")
        return []

def analyze_news(news_title):
    print(f"🧠 جاري تحليل: {news_title}")
    prompt = f"""
    أنت محلل استراتيجي ساخر ومطلع. اكتب تعليقاً مثيراً وقصيراً (سطرين فقط) عن هذا الخبر: "{news_title}".
    استخدم لغة مصرية قوية، واجعل القارئ يشعر أنك تكشف سراً.
    لا تبدأ بمقدمات مملة. ادخل في الموضوع فوراً.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"⚠️ خطأ في التحليل: {e}")
        # تحليل احتياطي عشان الخانة متبقاش فاضية
        backups = [
            "الخبر ده وراه حكايات كتير، والأيام الجاية هتكشف المستور!",
            "تطور غريب جداً، والكل بيسأل: إيه اللي هيحصل بعد كدة؟",
            "واضح إن الموضوع أكبر مما نتخيل، خلونا نتابع بحذر."
        ]
        return random.choice(backups)

def update_html(news_data):
    # كود HTML مانع للكاش (Anti-Cache)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
        <meta http-equiv="Pragma" content="no-cache" />
        <meta http-equiv="Expires" content="0" />
        
        <title>مصر الآن | تغطية حية</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Alexandria:wght@400;700;900&display=swap');
            :root {{ --main-color: #c0392b; --bg-color: #121212; --card-bg: #1e1e1e; }}
            body {{ font-family: 'Alexandria', sans-serif; background-color: var(--bg-color); color: #ecf0f1; margin: 0; padding: 0; }}
            .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
            .header {{ text-align: center; padding: 40px 0; border-bottom: 3px solid var(--main-color); margin-bottom: 30px; }}
            .header h1 {{ font-size: 3.5rem; margin: 0; color: var(--main-color); letter-spacing: -2px; }}
            .header p {{ color: #7f8c8d; font-size: 1.2rem; margin-top: 10px; }}
            .update-badge {{ background: #2c3e50; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; color: #f39c12; display: inline-block; margin-top: 10px; }}
            
            .news-card {{ background: var(--card-bg); border-radius: 16px; padding: 25px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); transition: transform 0.3s ease; border-right: 4px solid var(--main-color); position: relative; overflow: hidden; }}
            .news-card:hover {{ transform: translateY(-5px); }}
            .news-title {{ font-size: 1.6rem; font-weight: 900; margin-bottom: 15px; line-height: 1.4; }}
            
            .analysis {{ background: rgba(192, 57, 43, 0.1); padding: 15px; border-radius: 12px; margin-top: 15px; }}
            .analysis-icon {{ font-weight: bold; color: var(--main-color); margin-bottom: 5px; display: block; }}
            .analysis-text {{ color: #bdc3c7; line-height: 1.6; font-size: 1.1rem; }}
            
            .footer {{ text-align: center; margin-top: 50px; color: #7f8c8d; font-size: 0.9rem; padding-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>مصر الآن 🔴</h1>
                <p>ما لا يجرؤ الإعلام التقليدي على قوله</p>
                <div class="update-badge">آخر تحديث: {current_time}</div>
            </div>

            <div id="news-container">
                REPLACE_NEWS_ITEMS
            </div>

            <div class="footer">
                تم التطوير بواسطة الذكاء الاصطناعي - 2026
            </div>
        </div>
    </body>
    </html>
    """
    
    news_html = ""
    for item in news_data:
        news_html += f"""
        <div class="news-card">
            <div class="news-title">{item['title']}</div>
            <div class="analysis">
                <span class="analysis-icon">👁️ رأي المحلل:</span>
                <div class="analysis-text">{item['analysis']}</div>
            </div>
        </div>
        """
    
    final_html = html_template.replace("REPLACE_NEWS_ITEMS", news_html)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

def main():
    print("🚀 بدء تشغيل المحرك النووي للأخبار...")
    trending_news = get_trending_news()
    
    final_data = []
    if trending_news:
        for news in trending_news:
            analysis = analyze_news(news)
            final_data.append({"title": news, "analysis": analysis})
        
        update_html(final_data)
        print("✅ تم التحديث بنجاح! الموقع جاهز.")
    else:
        print("⚠️ لم يتم العثور على أخبار، لكن لن نوقف الموقع.")

if __name__ == "__main__":
    main()
