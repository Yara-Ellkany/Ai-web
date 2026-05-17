import streamlit as st
import requests
import base64
import os
import io
import time
from PIL import Image
import json

# ─── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Dream Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Raleway:wght@300;400;600&display=swap');

:root {
    --gold: #c9a96e;
    --dark: #0a0a0f;
    --glass: rgba(255,255,255,0.04);
    --border: rgba(201,169,110,0.25);
}

* { box-sizing: border-box; }

.stApp {
    background: radial-gradient(ellipse at 20% 50%, #1a0a2e 0%, #0a0a0f 50%, #0d1a0a 100%);
    font-family: 'Raleway', sans-serif;
    color: #e8e0d0;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem; max-width: 1200px; }

/* ── Hero Title ── */
.hero-title {
    font-family: 'Cinzel', serif;
    font-size: clamp(2.5rem, 6vw, 5rem);
    font-weight: 900;
    background: linear-gradient(135deg, #c9a96e, #fff5e0, #a67c52);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    letter-spacing: 0.15em;
    margin: 0;
    animation: shimmer 4s infinite;
    background-size: 200% auto;
}
@keyframes shimmer {
    0%   { background-position: 0% center; }
    50%  { background-position: 100% center; }
    100% { background-position: 0% center; }
}

.hero-sub {
    text-align: center;
    color: rgba(201,169,110,0.7);
    font-size: 1rem;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    margin-top: 0.4rem;
    font-weight: 300;
}

.divider {
    width: 60%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    margin: 2rem auto;
}

/* ── Glass Cards ── */
.glass-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.8rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1.5rem;
}

.section-label {
    font-family: 'Cinzel', serif;
    font-size: 0.75rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.8rem;
}

/* ── Inputs ── */
textarea, .stTextArea textarea {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: #e8e0d0 !important;
    font-family: 'Raleway', sans-serif !important;
    font-size: 0.95rem !important;
    resize: vertical !important;
}
textarea:focus { border-color: var(--gold) !important; box-shadow: 0 0 0 2px rgba(201,169,110,0.15) !important; }

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #c9a96e, #a67c52) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'Cinzel', serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(201,169,110,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(201,169,110,0.4) !important;
}

/* ── Image Frame ── */
.image-frame {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid var(--border);
    box-shadow: 0 20px 60px rgba(0,0,0,0.6), 0 0 40px rgba(201,169,110,0.08);
}

/* ── Animated Image Effects ── */
.img-float { animation: floatY 6s ease-in-out infinite; }
.img-pulse { animation: pulseGlow 3s ease-in-out infinite; }
.img-zoom  { animation: slowZoom 12s ease-in-out infinite alternate; }
.img-pan   { animation: panX 10s ease-in-out infinite alternate; }

@keyframes floatY {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-18px); }
}
@keyframes pulseGlow {
    0%, 100% { filter: brightness(1) saturate(1); box-shadow: 0 0 20px rgba(201,169,110,0.2); }
    50%       { filter: brightness(1.1) saturate(1.2); box-shadow: 0 0 40px rgba(201,169,110,0.5); }
}
@keyframes slowZoom {
    from { transform: scale(1); }
    to   { transform: scale(1.08); }
}
@keyframes panX {
    from { object-position: 0% center; }
    to   { object-position: 100% center; }
}

/* ── Status Badge ── */
.status-badge {
    display: inline-block;
    padding: 0.35rem 1rem;
    border-radius: 50px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.1em;
}
.status-success { background: rgba(80,200,120,0.15); border: 1px solid rgba(80,200,120,0.4); color: #50c878; }
.status-error   { background: rgba(220,80,80,0.15); border: 1px solid rgba(220,80,80,0.4); color: #dc5050; }

/* ── API key input ── */
.stTextInput input {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: #e8e0d0 !important;
    font-family: 'Raleway', sans-serif !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: rgba(0,0,0,0.4) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: #e8e0d0 !important;
}

/* ── Audio player ── */
audio { width: 100%; border-radius: 10px; margin-top: 1rem; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,0,0,0.3);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Cinzel', serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.15em !important;
    color: rgba(201,169,110,0.6) !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(201,169,110,0.15) !important;
    color: var(--gold) !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Hero Header ─────────────────────────────────────────────
st.markdown('<h1 class="hero-title">✦ AI DREAM STUDIO ✦</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Generate · Animate · Narrate</p>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ─── Sidebar – API Keys ───────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ API Configuration")
    hf_token = st.text_input("Hugging Face Token", type="password",
                              help="من huggingface.co/settings/tokens")
    st.markdown("---")
    st.markdown("**روابط مفيدة:**")
    st.markdown("• [Hugging Face Tokens](https://huggingface.co/settings/tokens)")
    st.markdown("• [Free Image Models](https://huggingface.co/models?pipeline_tag=text-to-image)")


# ─── Helper Functions ─────────────────────────────────────────

def generate_image_hf(prompt: str, token: str, model: str) -> bytes | None:
    """Generate image via Hugging Face Inference API (free tier)."""
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": prompt,
                "parameters": {"num_inference_steps": 30, "guidance_scale": 7.5}}
    try:
        with st.spinner("🎨 يتم توليد الصورة..."):
            resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        if resp.status_code == 200:
            return resp.content
        elif resp.status_code == 503:
            # Model loading – wait and retry once
            st.info("⏳ النموذج يشتغل، سيُعاد المحاولة خلال 30 ثانية...")
            time.sleep(30)
            resp2 = requests.post(API_URL, headers=headers, json=payload, timeout=120)
            return resp2.content if resp2.status_code == 200 else None
        else:
            st.error(f"❌ خطأ في توليد الصورة: {resp.status_code} – {resp.text[:200]}")
            return None
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال: {e}")
        return None


def text_to_speech_free(text: str, lang: str = "ar") -> bytes | None:
    """TTS via free MyMemory API (no key needed)."""
    try:
        encoded = requests.utils.quote(text[:500])  # limit chars
        url = f"https://api.mymemory.translated.net/get?q={encoded}&langpair={lang}|{lang}"
        # Actually use gTTS-compatible endpoint via another free service
        # We'll use the browser Web Speech API instead (client-side)
        return None
    except Exception:
        return None


def img_to_base64(img_bytes: bytes) -> str:
    return base64.b64encode(img_bytes).decode()


# ─── Main Tabs ────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🎨  توليد الصورة", "🎬  التحريك", "🔊  النطق"])


# ════════════════════════════════════════════════════════════════
# TAB 1 – IMAGE GENERATION
# ════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([1.2, 1], gap="large")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">📝 وصف الصورة (Prompt)</p>', unsafe_allow_html=True)

        img_prompt = st.text_area(
            label="",
            placeholder="صف الصورة التي تريدها... مثال:\nA magical forest at night, glowing mushrooms, ethereal light rays, fantasy art, 8K",
            height=130,
            key="img_prompt"
        )

        model_choice = st.selectbox(
            "اختر النموذج",
            options=[
                "stabilityai/stable-diffusion-xl-base-1.0",
                "runwayml/stable-diffusion-v1-5",
                "prompthero/openjourney",
                "dreamlike-art/dreamlike-photoreal-2.0",
                "SG161222/Realistic_Vision_V5.1_noVAE",
            ],
            index=0
        )

        negative_prompt = st.text_input(
            "Negative Prompt (اختياري)",
            placeholder="ugly, blurry, low quality, distorted..."
        )

        generate_btn = st.button("✦ توليد الصورة", key="gen_img")
        st.markdown('</div>', unsafe_allow_html=True)

        # Tips
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">💡 نصائح للـ Prompt</p>', unsafe_allow_html=True)
        st.markdown("""
- أضف **8K, ultra detailed, masterpiece** للجودة
- حدّد الأسلوب: *oil painting, digital art, cinematic*
- أضف الإضاءة: *golden hour, neon lights, dramatic lighting*
- الكاميرا: *close-up, wide shot, bird's eye view*
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-label">🖼 الصورة المولّدة</div>', unsafe_allow_html=True)

        if generate_btn:
            if not hf_token:
                st.error("⚠️ أدخل Hugging Face Token في الإعدادات (القائمة الجانبية)")
            elif not img_prompt.strip():
                st.warning("⚠️ اكتب وصفاً للصورة أولاً")
            else:
                img_bytes = generate_image_hf(img_prompt.strip(), hf_token, model_choice)
                if img_bytes:
                    st.session_state["generated_img"] = img_bytes
                    st.session_state["img_prompt_used"] = img_prompt
                    st.markdown('<span class="status-badge status-success">✓ تم التوليد بنجاح</span>',
                                unsafe_allow_html=True)

        if "generated_img" in st.session_state:
            img_b64 = img_to_base64(st.session_state["generated_img"])
            st.markdown(f'''
            <div class="image-frame">
                <img src="data:image/png;base64,{img_b64}"
                     style="width:100%;display:block;border-radius:14px;" />
            </div>''', unsafe_allow_html=True)

            # Download button
            st.download_button(
                label="⬇ تحميل الصورة",
                data=st.session_state["generated_img"],
                file_name="ai_dream_studio.png",
                mime="image/png"
            )
        else:
            st.markdown("""
            <div style="border:1px dashed rgba(201,169,110,0.3);border-radius:16px;
                        padding:4rem 2rem;text-align:center;color:rgba(201,169,110,0.4);">
                <div style="font-size:3rem;margin-bottom:1rem;">✦</div>
                <div style="font-family:'Cinzel',serif;letter-spacing:0.2em;font-size:0.85rem;">
                    الصورة ستظهر هنا
                </div>
            </div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# TAB 2 – ANIMATION
# ════════════════════════════════════════════════════════════════
with tab2:
    if "generated_img" not in st.session_state:
        st.info("🎨 ولّد صورة أولاً من التبويب الأول")
    else:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">🎬 اختر نوع التحريك</p>', unsafe_allow_html=True)

        anim_type = st.selectbox(
            "",
            options=[
                ("float",  "🌊 طفو – Float Up & Down"),
                ("pulse",  "💫 توهج – Pulse Glow"),
                ("zoom",   "🔍 تكبير تدريجي – Slow Zoom"),
                ("pan",    "👁 مسح جانبي – Pan"),
            ],
            format_func=lambda x: x[1],
            index=0
        )
        anim_key = anim_type[0]

        speed = st.slider("سرعة التحريك (ثواني)", 2, 15, 6)

        st.markdown('</div>', unsafe_allow_html=True)

        # Show animated image
        img_b64 = img_to_base64(st.session_state["generated_img"])

        anim_css_map = {
            "float": f"animation: floatY {speed}s ease-in-out infinite;",
            "pulse": f"animation: pulseGlow {speed}s ease-in-out infinite;",
            "zoom":  f"animation: slowZoom {speed}s ease-in-out infinite alternate;",
            "pan":   f"animation: panX {speed}s ease-in-out infinite alternate;",
        }
        anim_style = anim_css_map[anim_key]

        st.markdown(f"""
        <style>
        @keyframes floatY  {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-20px)}} }}
        @keyframes pulseGlow {{ 0%,100%{{filter:brightness(1) saturate(1);box-shadow:0 0 20px rgba(201,169,110,.2)}} 50%{{filter:brightness(1.15) saturate(1.3);box-shadow:0 0 60px rgba(201,169,110,.6)}} }}
        @keyframes slowZoom {{ from{{transform:scale(1)}} to{{transform:scale(1.1)}} }}
        @keyframes panX {{ from{{object-position:0% center}} to{{object-position:100% center}} }}
        .anim-preview {{ border-radius:16px; overflow:hidden; border:1px solid rgba(201,169,110,.25);
                          box-shadow:0 20px 60px rgba(0,0,0,.6); }}
        .anim-preview img {{ width:100%; display:block; {anim_style} }}
        </style>
        <div class="anim-preview">
            <img src="data:image/png;base64,{img_b64}" />
        </div>
        <p style="text-align:center;color:rgba(201,169,110,.5);margin-top:.8rem;
                  font-size:.8rem;letter-spacing:.2em;font-family:'Cinzel',serif;">
            ✦ LIVE ANIMATION PREVIEW ✦
        </p>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# TAB 3 – TEXT TO SPEECH
# ════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">🎙 النص المراد نطقه</p>', unsafe_allow_html=True)

    tts_text = st.text_area(
        "",
        placeholder="اكتب السيناريو أو أي نص تريد سماعه...\nمثال: مرحباً بكم في استوديو الأحلام الذكي، حيث تتحول كلماتك إلى صور حية ومتحركة.",
        height=180
    )

    lang_map = {
        "العربية":   "ar-SA",
        "الإنجليزية": "en-US",
        "الفرنسية":  "fr-FR",
        "الإسبانية": "es-ES",
    }
    lang_choice = st.selectbox("اللغة", list(lang_map.keys()))
    lang_code = lang_map[lang_choice]

    voice_speed = st.slider("سرعة النطق", 0.5, 2.0, 1.0, 0.1)
    voice_pitch = st.slider("حدة الصوت", 0.5, 2.0, 1.0, 0.1)

    speak_btn = st.button("🔊 تشغيل النطق", key="speak_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    # Web Speech API (runs in browser, no API key needed)
    if speak_btn and tts_text.strip():
        escaped = tts_text.replace("'", "\\'").replace("\n", " ")
        st.markdown(f"""
        <script>
        (function() {{
            window.speechSynthesis.cancel();
            const utter = new SpeechSynthesisUtterance('{escaped}');
            utter.lang  = '{lang_code}';
            utter.rate  = {voice_speed};
            utter.pitch = {voice_pitch};
            // Try to pick a matching voice
            const voices = window.speechSynthesis.getVoices();
            const match  = voices.find(v => v.lang.startsWith('{lang_code[:2]}'));
            if (match) utter.voice = match;
            window.speechSynthesis.speak(utter);
        }})();
        </script>
        <div class="glass-card" style="text-align:center;padding:1.2rem;">
            <span class="status-badge status-success">🔊 يتم النطق الآن...</span>
        </div>
        """, unsafe_allow_html=True)

    elif speak_btn:
        st.warning("⚠️ اكتب نصاً أولاً")

    # Combined showcase: animated image + speech
    if "generated_img" in st.session_state and tts_text.strip():
        st.markdown("---")
        st.markdown('<p class="section-label">✨ العرض الكامل – صورة متحركة + نطق</p>', unsafe_allow_html=True)
        img_b64 = img_to_base64(st.session_state["generated_img"])
        escaped2 = tts_text.replace("'", "\\'").replace("\n", " ")

        st.markdown(f"""
        <style>
        @keyframes floatFull {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-15px)}} }}
        @keyframes glowFull  {{ 0%,100%{{box-shadow:0 0 30px rgba(201,169,110,.3)}} 50%{{box-shadow:0 0 70px rgba(201,169,110,.7)}} }}
        .full-frame {{ border-radius:20px;overflow:hidden;border:1px solid rgba(201,169,110,.35);
                       animation:glowFull 4s ease-in-out infinite; max-width:500px; margin:0 auto; }}
        .full-frame img {{ width:100%;display:block;animation:floatFull 7s ease-in-out infinite; }}
        </style>
        <div class="full-frame">
            <img src="data:image/png;base64,{img_b64}" />
        </div>
        <div style="text-align:center;margin-top:1.5rem;">
            <button onclick="(function(){{
                window.speechSynthesis.cancel();
                const u=new SpeechSynthesisUtterance('{escaped2}');
                u.lang='{lang_code}'; u.rate={voice_speed}; u.pitch={voice_pitch};
                window.speechSynthesis.speak(u);
            }})()"
            style="background:linear-gradient(135deg,#c9a96e,#a67c52);color:#0a0a0f;
                   border:none;padding:0.9rem 2.5rem;border-radius:50px;cursor:pointer;
                   font-family:'Cinzel',serif;font-weight:700;font-size:0.9rem;
                   letter-spacing:0.2em;box-shadow:0 4px 20px rgba(201,169,110,.4);">
                ▶ تشغيل الكامل
            </button>
        </div>
        """, unsafe_allow_html=True)


# ─── Footer ──────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center;color:rgba(201,169,110,0.3);font-size:0.75rem;
           letter-spacing:0.3em;font-family:'Cinzel',serif;">
    ✦ AI DREAM STUDIO ✦ BUILT WITH STREAMLIT & HUGGING FACE
</p>
""", unsafe_allow_html=True)
