import requests
import xml.etree.ElementTree as ET
import os
import google.generativeai as genai
from datetime import datetime
import json

# --- 1. إعدادات "الوحش" (الذكاء الاصطناعي الشجاع) ---
api_key = os.environ.get("GEMINI_API_KEY")

# إعدادات الأمان (إلغاء الخوف تماماً)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

if api_key:
    genai.configure(api_key=api_key)
    # استخدام موديل فلاش السريع
    model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
else:
    print("⚠️ تنبيه: لم يتم العثور على مفتاح API. سيتم جلب العناوين فقط.")

rss_url = "https://news.google.com/rss?ceid=EG:ar&hl=ar&gl=EG"

# --- 2. دالة "العبقرية" (SEO Injection) ---
def get_seo_magic(title, description, image_url, site_url="https://masr-news.github.io"):
    """
    هنا بنحقن كود جوجل السري (JSON-LD) عشان نطلع تريند
    """
    date_now = datetime.now().isoformat()
    
    # 1. البيانات الهيكلية (اللغة اللي بيفهمها جوجل)
    schema = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": title,
        "description": description,
        "image": [image_url],
        "datePublished": date_now,
        "dateModified": date_now,
        "author": {
            "@type": "Person",
            "name": "المحلل الذكي"
        },
        "publisher": {
            "@type": "Organization",
            "name": "مصر الآن",
            "logo": {
                "@type": "ImageObject",
                "url": "https://masr-news.github.io/logo.png" # لو عندك لوجو حط رابطه هنا
            }
        }
    }
    
    # 2. ميتا تاج للسوشيال ميديا
    meta_tags = f"""
    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta property="og:locale" content="ar_EG">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{site_url}">
    <meta property="og:site_name" content="مصر الآن">
    <meta property="og:image" content="{image_url}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
    """
    return meta_tags

# --- 3. المحرك الرئيسي ---
def create_masterpiece():
    print("⏳ بدء تشغيل غرفة الأخبار (الوضع الشجاع)...")
    
    try:
        response = requests.get(rss_url)
        root = ET.fromstring(response.content)
        items = root.findall('.//item')
        
        # توقيت القاهرة
        now = datetime.now().strftime("%I:%M %p | %Y-%m-%d")

        # ** خطوة ذكية: سحب أول خبر عشان نعمل عليه SEO **
        top_news_title = "أخبار مصر العاجلة"
        top_news_desc = "تابع أحدث الأخبار لحظة بلحظة من موقع مصر الآن"
        if len(items) > 0:
            top_news_title = items[0].find('title').text
            top_news_desc = f"تغطية خاصة لخبر: {top_news_title}"

        # توليد كود الـ SEO
        seo_code = get_seo_magic(top_news_title, top_news_desc, "https://via.placeholder.com/1200x630.png?text=Breaking+News")
        
        # --- تصميم الموقع ---
        html_content = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{top_news_title} | مصر الآن</title>
            <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
            {seo_code}
            <style>
                :root {{ --primary: #e74c3c; --dark: #1a252f; --bg: #f0f2f5; }}
                body {{ font-family: 'Cairo', sans-serif; background-color: var(--bg); margin: 0; color: #333; }}
                header {{ background: linear-gradient(135deg, #000, #2c3e50); color: white; padding: 30px 20px; text-align: center; border-bottom: 5px solid var(--primary); }}
                header h1 {{ margin: 0; font-size: 2.8em; font-weight: 900; letter-spacing: -1px; }}
                .container {{ max-width: 1000px; margin: 30px auto; padding: 0 15px; display: grid; gap: 25px; }}
                
                .news-card {{ background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.08); transition: transform 0.2s; border: 1px solid #eee; }}
                .news-card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 30px rgba(0,0,0,0.15); border-color: var(--primary); }}
                
                .card-header {{ background: var(--primary); color: white; padding: 8px 15px; font-size: 0.85em; font-weight: bold; display: inline-block; border-radius: 0 0 10px 0; }}
                .card-body {{ padding: 20px; }}
                h2 {{ margin: 10px 0; color: var(--dark); line-height: 1.4; font-size: 1.3em; }}
                .meta {{ font-size: 0.85em; color: #777; margin-bottom: 15px; display: block; }}
                
                .ai-box {{ background: #fff5f5; border-right: 4px solid var(--primary); padding: 15px; border-radius: 6px; margin-top: 15px; position: relative; }}
                .ai-box::before {{ content: "🤖 تحليل خاص"; position: absolute; top: -12px; right: 10px; background: var(--primary); color: white; font-size: 0.7em; padding: 2px 8px; border-radius: 4px; }}
                .ai-text {{ color: #444; line-height: 1.7; font-size: 1em; }}
                
                .source-btn {{ display: block; text-align: center; margin-top: 20px; padding: 10px; background: #ecf0f1; color: var(--dark); text-decoration: none; border-radius: 6px; font-weight: bold; transition: 0.3s; }}
                .source-btn:hover {{ background: var(--dark); color: white; }}
            </style>
        </head>
        <body>
            <header>
                <h1>🔴 مصر الآن</h1>
                <p>أخبار لا يجرؤ الآخرون على تحليلها</p>
                <div style="opacity: 0.7; font-size: 0.9em;">آخر تحديث: {now}</div>
            </header>
            <div class="container">
        """
        
        # --- حلقة التكرار (الأخبار) ---
        count = 0
        for item in items:
            if count >= 8: break # زودنا العدد لـ 8 أخبار
            
            title = item.find('title').text
            pubDate = item.find('pubDate').text
            link = item.find('link').text
            
            print(f"🔥 جاري تحليل الخبر {count+1}: {title[:30]}...")
            
            ai_article = ""
            if api_key:
                try:
                    # الأمر "الوقح" للموديل عشان يكتب بحرية
                    prompt = f"""
                    أنت صحفي جريء ومحلل سياسي لا يخاف في الحق لومة لائم.
                    الخبر: "{title}"
                    المطلوب:
                    1. اكتب تحليل ناري ومثير للجدل لهذا الخبر (حوالي 60 كلمة).
                    2. استخدم لغة قوية تجذب القارئ (مثل: كارثة، مفاجأة، صدمة).
                    3. لا تستخدم مقدمات مملة مثل "في سياق متصل". ادخل في صلب الموضوع فوراً.
                    """
                    response = model.generate_content(prompt)
                    ai_article = response.text.replace("*", "").replace("#", "")
                except Exception as e:
                    ai_article = "نعتذر، المحلل يواجه ضغطاً شديداً حالياً."
                    print(f"Error: {e}")
            else:
                ai_article = "يرجى تفعيل مفتاح API لرؤية التحليل السري."

            html_content += f"""
            <div class="news-card">
                <div class="card-header">🔥 عاجل وحصري</div>
                <div class="card-body">
                    <h2>{title}</h2>
                    <span class="meta">📅 {pubDate}</span>
                    <div class="ai-box">
                        <div class="ai-text">{ai_article}</div>
                    </div>
                    <a href="{link}" target="_blank" class="source-btn">🔗 قراءة المصدر الأصلي</a>
                </div>
            </div>
            """
            count += 1
            
        html_content += """
            </div>
            <div style="text-align:center; padding:30px; color:#777; font-size:0.9em;">
                &copy; 2026 جميع الحقوق محفوظة لشبكة مصر الآن الإخبارية
            </div>
        </body>
        </html>
        """
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ تم الإطلاق! الموقع جاهز ومحمي ضد المنافسين.")

    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    create_masterpiece()
