# ✦ AI Dream Studio ✦
> توليد صور بالذكاء الاصطناعي + تحريكها + نطق السيناريو

## المميزات 🚀
- 🎨 **توليد الصور** – باستخدام Stable Diffusion عبر Hugging Face
- 🎬 **تحريك الصور** – 4 أنواع من الحركات (طفو، توهج، تكبير، مسح)
- 🔊 **النطق** – نطق أي نص بالعربية أو الإنجليزية مباشرة في المتصفح
- ✨ **عرض كامل** – صورة متحركة + نطق معاً

---

## الإعداد المحلي 🖥️

```bash
# 1. استنسخ المستودع
git clone https://github.com/YOUR_USERNAME/ai-dream-studio.git
cd ai-dream-studio

# 2. ثبّت المكتبات
pip install -r requirements.txt

# 3. شغّل التطبيق
streamlit run app.py
```

---

## النشر على Streamlit Cloud ☁️

### الخطوة 1 – رفع الكود على GitHub
```bash
git init
git add .
git commit -m "✨ Initial commit – AI Dream Studio"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-dream-studio.git
git push -u origin main
```

### الخطوة 2 – نشر على Streamlit Cloud
1. اذهب إلى [share.streamlit.io](https://share.streamlit.io)
2. سجّل الدخول بحساب GitHub
3. اضغط **New app**
4. اختر المستودع والملف `app.py`
5. اضغط **Deploy**

### الخطوة 3 – الحصول على Hugging Face Token (مجاني)
1. سجّل في [huggingface.co](https://huggingface.co)
2. اذهب إلى **Settings > Access Tokens**
3. أنشئ **Read token** جديد
4. الصقه في القائمة الجانبية للتطبيق

---

## هيكل الملفات 📁
```
ai-dream-studio/
├── app.py              ← التطبيق الرئيسي
├── requirements.txt    ← المكتبات المطلوبة
└── README.md           ← هذا الملف
```

---

## ملاحظات مهمة ⚠️
- الـ TTS (النطق) يعمل مباشرة في المتصفح **بدون API key**
- توليد الصور يحتاج **Hugging Face Token مجاني**
- أول طلب قد يأخذ 30-60 ثانية (تحميل النموذج)

---

## نماذج مقترحة 🎨
| النموذج | الأسلوب |
|---------|---------|
| `stabilityai/stable-diffusion-xl-base-1.0` | عام وعالي الجودة |
| `prompthero/openjourney` | أسلوب Midjourney |
| `dreamlike-art/dreamlike-photoreal-2.0` | واقعي جداً |
| `SG161222/Realistic_Vision_V5.1_noVAE` | صور واقعية |

---

*صُنع بـ ❤️ باستخدام Streamlit + Hugging Face*
