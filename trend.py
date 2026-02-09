import requests
import json
import os
import google.generativeai as genai
from datetime import datetime
import xml.etree.ElementTree as ET

# إعداد مفتاح API
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')

if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found.")
    exit(1)

genai.configure(api_key=GOOGLE_API_KEY)

# استخدام موديل gemini-pro (الأكثر استقراراً)
model = genai.GenerativeModel('gemini-pro')

def get_trending_news():
    print("...جاري جلب الأخبار من Google Trends...")
    url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=EG"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            news_items = []
            for item in root.findall('.//item'):
                title = item.find('title').text
                news_items.append(title)
            return news_items[:5]  # نأخذ أهم 5 أخبار فقط
        else:
            print("Error fetching trends")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def analyze_news(news_title):
    print(f"🔥 ...جاري تحليل الخبر: {news_title}")
    prompt = f"""
    تصرف كمحلل سياسي واستراتيجي "جريء جداً" ولا يخشى في الحق لومة لائم.
    مهمتك: اكتب تحليل ناري ومثير للجدل عن هذا الخبر: "{news_title}".

    الشروط الصارمة:
    1. ابدأ فوراً بجملة صادمة (مثال: "كارثة جديدة تضرب...", "هل يضحكون علينا؟").
    2. استخدم لغة حادة وقوية (عامية مصرية مثقفة).
    3. اكشف "ما وراء الكواليس" وافضح النوايا الخفية (حتى لو تخيلية).
    4. لا تكن محايداً أبداً.. انحاز للمواطن الغلبان.
    5. انهي التحليل بسؤال مرعب للمستقبل.
    6. الطول: فقرة واحدة مركزة (4-5 سطور).

    الخبر هو: {news_title}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error analyzing news: {e}")
        return "نعتذر، المحلل تحت المراقبة حالياً ولا يستطيع الكلام!"

def update_html(news_data):
    html_template = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>مصر الآن - تغطية ذكية</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
            body { font-family: 'Cairo', sans-serif; background-color: #1a1a1a; color: #fff; margin: 0; padding: 20px; }
            .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #e50914; padding-bottom: 10px; }
            .header h1 { font-size: 3em; margin: 0; color: #e50914; }
            .header p { color: #888; font-size: 1.2em; }
            .news-card { background: #2b2b2b; border-radius: 15px; margin-bottom: 20px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border-right: 5px solid #e50914; }
            .news-title { font-size: 1.8em; font-weight: 900; color: #fff; margin-bottom: 10px; }
            .analysis-box { background: #3a3a3a; padding: 15px; border-radius: 10px; margin-top: 15px; position: relative; }
            .analysis-box::before { content: "🕵️‍♂️ تحليل سري:"; position: absolute; top: -12px; right: 20px; background: #e50914; padding: 2px 10px; border-radius: 5px; font-size: 0.9em; font-weight: bold; }
            .analysis-text { font-size: 1.1em; line-height: 1.6; color: #ddd; margin-top: 10px; }
            .footer { text-align: center; margin-top: 40px; color: #555; font-size: 0.8em; }
            .timestamp { text-align: center; color: #e50914; font-weight: bold; margin-bottom: 20px; direction: ltr; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>مصر الآن 🔴</h1>
            <p>أخبار لا يجرؤ الآخرون على تحليلها</p>
        </div>
        
        <div class="timestamp">Last Update: REPLACE_TIME</div>

        <div id="news-container">
            REPLACE_NEWS_ITEMS
        </div>

        <div class="footer">
            جميع الحقوق محفوظة - المحلل الذكي 2026
        </div>
    </body>
    </html>
    """
    
    news_html = ""
    for item in news_data:
        news_html += f"""
        <div class="news-card">
            <div class="news-title">{item['title']}</div>
            <div class="analysis-box">
                <div class="analysis-text">{item['analysis']}</div>
            </div>
        </div>
        """
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    final_html = html_template.replace("REPLACE_NEWS_ITEMS", news_html).replace("REPLACE_TIME", current_time)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)

def main():
    print("...بدء تشغيل غرفة الأخبار (الوضع الشجاع) ⏳")
    trending_news = get_trending_news()
    
    final_data = []
    if trending_news:
        for news in trending_news:
            analysis = analyze_news(news)
            final_data.append({"title": news, "analysis": analysis})
        
        update_html(final_data)
        print("✅ تم الإطلاق! الموقع جاهز ومحمي ضد المنافسين.")
    else:
        print("⚠️ لم يتم العثور على أخبار جديدة.")

if __name__ == "__main__":
    main()
