from transformers import MBartForConditionalGeneration, MBart50Tokenizer
from PIL import Image
import streamlit as st
import base64
from languages import languages

# Page configuration
st.set_page_config(
    page_title='Multilingual Translator', 
    layout='wide', 
    page_icon='🌐',
    initial_sidebar_state='expanded'
)

# Function to convert image to base64 for CSS background
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Custom CSS with background image
def apply_custom_css():
    banner_base64 = get_base64_image('banner.png')
    
    css = """
    <style>
    /* Main background styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Background image overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        opacity: 0.1;
    """
    
    if banner_base64:
        css += f"""
        background-image: url('data:image/png;base64,{banner_base64}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        """
    
    css += """
    }
    
    /* Header styling */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    }
    
    .main-title {
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        color: #555;
        font-size: 1.3rem;
        margin-bottom: 0;
    }
    
    /* Card styling */
    .translator-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 2rem;
    }
    
    /* Input area styling */
    .stTextArea textarea {
        border-radius: 15px;
        border: 2px solid #e0e6ed;
        font-size: 1.1rem;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Result box styling */
    .result-box {
        background: linear-gradient(135deg, #e6f7ff, #f0f9ff);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin-top: 1rem;
        font-size: 1.1rem;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Language selection styling */
    .language-section {
        background: rgba(102, 126, 234, 0.1);
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
    }
    
    /* Info box styling */
    .info-box {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Footer styling */
    .footer {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 3rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .translator-card {
        animation: fadeIn 0.6s ease-out;
    }
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

# Apply custom CSS
apply_custom_css()

# Header Section
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🌐 Multilingual Translator</h1>
    <p class="subtitle">Translate text between 50+ languages using mBART-50 AI model</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for language selection
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem;">
    <h2 style="color: #667eea;">🌟 Language Settings</h2>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="language-section">', unsafe_allow_html=True)
st.sidebar.markdown("**🔤 Source Language**")
src_lang = st.sidebar.selectbox('', list(languages.keys()), key='source_lang', label_visibility='collapsed')

st.sidebar.markdown("**🎯 Target Language**")
trans_lang = st.sidebar.selectbox('', list(languages.keys()), key='target_lang', label_visibility='collapsed')
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Language swap button
if st.sidebar.button('🔄 Swap Languages', use_container_width=True):
    # This would require session state to properly swap languages
    st.sidebar.info("💡 Tip: Manually change the languages above to swap them")

# Get language codes
src_lang_code = [value for key, value in languages.items() if key == src_lang][0]
trans_lang_code = [value for key, value in languages.items() if key == trans_lang][0]

# Cache the model loading
@st.cache_resource
def download_model():
    with st.spinner('Loading AI model... This may take a moment on first run.'):
        model_name = "facebook/mbart-large-50-many-to-many-mmt"
        model = MBartForConditionalGeneration.from_pretrained(model_name)
        tokenizer = MBart50Tokenizer.from_pretrained(model_name)
    return model, tokenizer

# Load model
try:
    model, tokenizer = download_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error(f"Error loading model: {str(e)}")

# Main translation interface
# st.markdown('<div class="translator-card">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"### 📝 Enter Text ({src_lang})")
    text = st.text_area(
        "",
        value='',
        height=200,
        max_chars=2000,
        placeholder=f"Type your text in {src_lang} here...",
        key="input_text",
        label_visibility='collapsed'
    )
    
    # Character counter
    char_count = len(text)
    st.markdown(f"<small>Characters: {char_count}/2000</small>", unsafe_allow_html=True)

with col2:
    st.markdown(f"### 🎯 Translation ({trans_lang})")
    
    # Translation button
    if st.button('🚀 Translate Now', use_container_width=True, type='primary'):
        if not model_loaded:
            st.error('❌ AI model not loaded. Please refresh the page and try again.')
        elif text.strip() == '':
            st.warning('⚠️ Please enter some text to translate!')
        elif src_lang == trans_lang:
            st.warning('⚠️ Source and target languages are the same!')
        else:
            try:
                with st.spinner('🔮 Translating... Please wait'):
                    # Set source language
                    tokenizer.src_lang = str(src_lang_code)
                    
                    # Encode input text
                    encoded_text = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
                    
                    # Generate translation
                    generated_tokens = model.generate(
                        **encoded_text,
                        forced_bos_token_id=tokenizer.lang_code_to_id[str(trans_lang_code)],
                        max_length=512,
                        num_beams=5,
                        early_stopping=True
                    )
                    
                    # Decode translation
                    translation = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
                    
                    st.success('✅ Translation completed successfully!')
                    
                    # Display result in a nice box
                    st.markdown(f"""
                    <div class="result-box">
                        <strong>📄 Translated Text:</strong><br>
                        <span style="font-size: 1.1rem;">{translation}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f'❌ Translation error: {str(e)}')
    
    # Copy to clipboard button (if translation exists)
    # if 'translation' in locals():
        # if st.button('📋 Copy Translation', use_container_width=True):
        #     st.info('💡 Translation is displayed above. Use Ctrl+C to copy.')

st.markdown('</div>', unsafe_allow_html=True)

# Information section
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("""
    <div class="info-box">
        <h4 style="color: #667eea;">🌍 50+ Languages</h4>
        <p>Support for major world languages including English, Spanish, French, German, Chinese, Arabic, and many more.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h4 style="color: #667eea;">🤖 AI-Powered</h4>
        <p>Uses Facebook's mBART-50 model, trained on billions of text examples for accurate translations.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-box">
        <h4 style="color: #667eea;">⚡ Fast & Reliable</h4>
        <p>Get instant translations with high accuracy. Perfect for documents, messages, and learning.</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar additional info
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="padding: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 10px;">
    <h4>💡 Usage Tips</h4>
    <ul style="font-size: 0.9rem;">
        <li>Keep text under 2000 characters for best results</li>
        <li>Check spelling for better accuracy</li>
        <li>Try shorter sentences for complex languages</li>
        <li>Model works best with formal text</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem;">
    <p style="font-size: 0.9rem; color: #666;">
        <strong>Supported Languages:</strong><br>
        🇺🇸 🇪🇸 🇫🇷 🇩🇪 🇨🇳 🇯🇵 🇰🇷 🇷🇺 🇮🇹 🇵🇹<br>
        🇳🇱 🇸🇪 🇳🇴 🇩🇰 🇫🇮 🇵🇱 🇹🇷 🇸🇦 🇮🇳 🇹🇭<br>
        <em>And many more...</em>
    </p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p style="margin-bottom: 1rem; color: #1f2937;">Made with ❤️ by <strong>B Sai Teja Goud</strong></p>
    <p style="font-size: 0.9rem; color: #6b7280;">
        Questions or issues? <a href="mailto:saitej0045@gmail.com?subject=Multilingual Translator WebApp!&body=Please specify the issue you are facing with the app." style="color: #3b82f6; text-decoration: none;">Contact me</a>
    </p>
</div>
""", unsafe_allow_html=True)