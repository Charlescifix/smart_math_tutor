import streamlit as st
from api_utils import api

# 🎨 Page Config
st.set_page_config(
    page_title="Binary Math Compiler - Initialize Session",
    page_icon="🔢",
    layout="wide"
)

# 🎨 Binary Mathematical Computing Interface
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=Fira+Code:wght@400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(145deg, #0d1117 0%, #161b22 30%, #21262d 70%, #0d1117 100%);
        font-family: 'JetBrains Mono', monospace;
        color: #58a6ff;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(90deg, rgba(88, 166, 255, 0.02) 1px, transparent 1px),
            linear-gradient(0deg, rgba(88, 166, 255, 0.02) 1px, transparent 1px);
        background-size: 30px 30px;
        pointer-events: none;
        z-index: 0;
    }

    .main-container {
        background: rgba(13, 17, 23, 0.95);
        border: 1px solid #30363d;
        border-radius: 6px;
        margin: 1rem auto;
        max-width: 1400px;
        position: relative;
        z-index: 1;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        min-height: 90vh;
    }

    .terminal-header {
        background: #21262d;
        border-bottom: 1px solid #30363d;
        padding: 0.75rem 1.5rem;
        font-family: 'Fira Code', monospace;
        font-size: 0.9rem;
        color: #7d8590;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .terminal-dots {
        display: flex;
        gap: 0.5rem;
    }

    .dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }

    .dot.red { background: #ff6b6b; }
    .dot.yellow { background: #ffd93d; }
    .dot.green { background: #6bcf7f; }

    .application-header {
        text-align: center;
        padding: 3rem 2rem 2rem 2rem;
        background: #161b22;
        border-bottom: 1px solid #30363d;
    }

    .app-title {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: #58a6ff !important;
        margin: 0 !important;
        text-shadow: 0 0 20px rgba(88, 166, 255, 0.3);
        letter-spacing: 3px;
    }

    .app-subtitle {
        font-family: 'Fira Code', monospace;
        font-size: 1.2rem;
        color: #6bcf7f;
        margin-top: 0.5rem;
        font-weight: 600;
        letter-spacing: 1px;
    }

    .code-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: auto auto;
        gap: 1.5rem;
        padding: 2rem;
    }

    .code-block {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 6px;
        overflow: hidden;
        transition: all 0.2s ease;
    }

    .code-block:hover {
        border-color: #58a6ff;
        box-shadow: 0 4px 12px rgba(88, 166, 255, 0.1);
    }

    .code-header {
        background: #21262d;
        border-bottom: 1px solid #30363d;
        padding: 0.75rem 1rem;
        font-family: 'Fira Code', monospace;
        font-size: 0.85rem;
        color: #7d8590;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .function-signature {
        color: #ffa657;
        font-weight: 600;
    }

    .welcome-block {
        grid-column: 1 / -1;
    }

    .welcome-content {
        padding: 2rem;
        text-align: center;
        background: #0d1117;
    }

    .welcome-message {
        font-family: 'Fira Code', monospace;
        font-size: 1.4rem;
        color: #6bcf7f;
        font-weight: 600;
        margin: 0;
        letter-spacing: 1px;
    }

    .form-block {
        background: #0d1117;
    }

    .form-content {
        padding: 2rem;
    }

    .input-group {
        margin-bottom: 1.5rem;
    }

    .input-label {
        font-family: 'Fira Code', monospace;
        font-size: 0.9rem;
        color: #ffa657;
        margin-bottom: 0.5rem;
        font-weight: 600;
        display: block;
    }

    .stTextInput > div > div > input {
        background: #161b22 !important;
        border: 2px solid #30363d !important;
        border-radius: 6px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        font-family: 'JetBrains Mono', monospace !important;
        color: #58a6ff !important;
        transition: all 0.2s ease !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }

    .stTextInput > div > div > input:focus {
        border: 2px solid #58a6ff !important;
        box-shadow: 
            inset 0 2px 4px rgba(0, 0, 0, 0.2),
            0 0 0 3px rgba(88, 166, 255, 0.1) !important;
        background: #0d1117 !important;
        color: #ffffff !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #6e7681 !important;
        font-family: 'Fira Code', monospace !important;
    }

    .stNumberInput > div > div > input {
        background: #161b22 !important;
        border: 2px solid #30363d !important;
        border-radius: 6px !important;
        padding: 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        font-family: 'JetBrains Mono', monospace !important;
        color: #6bcf7f !important;
        text-align: center !important;
        transition: all 0.2s ease !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }

    .stNumberInput > div > div > input:focus {
        border: 2px solid #6bcf7f !important;
        box-shadow: 
            inset 0 2px 4px rgba(0, 0, 0, 0.2),
            0 0 0 3px rgba(107, 207, 127, 0.1) !important;
        background: #0d1117 !important;
        color: #ffffff !important;
    }

    .stSelectbox > div > div {
        background: #161b22 !important;
        border: 2px solid #30363d !important;
        border-radius: 6px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        font-family: 'JetBrains Mono', monospace !important;
        color: #ffa657 !important;
        transition: all 0.2s ease !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }

    .stSelectbox > div > div:hover {
        border: 2px solid #ffa657 !important;
        box-shadow: 
            inset 0 2px 4px rgba(0, 0, 0, 0.2),
            0 0 0 3px rgba(255, 166, 87, 0.1) !important;
    }

    .features-block {
        background: #0d1117;
    }

    .features-content {
        padding: 2rem;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }

    .feature-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 4px;
        padding: 1rem;
        text-align: center;
        transition: all 0.2s ease;
    }

    .feature-card:hover {
        border-color: #58a6ff;
        box-shadow: 0 2px 8px rgba(88, 166, 255, 0.1);
        transform: translateY(-2px);
    }

    .feature-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        display: block;
    }

    .feature-text {
        font-family: 'Fira Code', monospace;
        font-weight: 600;
        font-size: 0.85rem;
        color: #7d8590;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .execute-block {
        background: #0d1117;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .execute-content {
        padding: 2rem;
        width: 100%;
    }

    .binary-execute-button {
        background: linear-gradient(135deg, #238636, #2ea043) !important;
        border: 1px solid #2ea043 !important;
        border-radius: 6px !important;
        padding: 2rem 3rem !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        font-family: 'JetBrains Mono', monospace !important;
        color: #ffffff !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        width: 100% !important;
        box-shadow: 0 6px 20px rgba(46, 160, 67, 0.3) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }

    .binary-execute-button:hover {
        background: linear-gradient(135deg, #2ea043, #46954a) !important;
        border-color: #46954a !important;
        box-shadow: 0 8px 24px rgba(46, 160, 67, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    .binary-stream {
        position: fixed;
        font-family: 'JetBrains Mono', monospace;
        color: rgba(88, 166, 255, 0.04);
        font-size: 0.7rem;
        pointer-events: none;
        z-index: 0;
        animation: binaryFloat 15s linear infinite;
    }

    .stream-1 { top: 8%; left: 3%; animation-delay: 0s; }
    .stream-2 { top: 25%; right: 5%; animation-delay: 5s; }
    .stream-3 { bottom: 30%; left: 7%; animation-delay: 10s; }
    .stream-4 { bottom: 15%; right: 10%; animation-delay: 12s; }
    .stream-5 { top: 50%; left: 2%; animation-delay: 3s; }
    .stream-6 { top: 70%; right: 3%; animation-delay: 8s; }

    @keyframes binaryFloat {
        0% { 
            transform: translateY(0px);
            opacity: 0.04;
        }
        50% { 
            transform: translateY(-8px);
            opacity: 0.06;
        }
        100% { 
            transform: translateY(0px);
            opacity: 0.04;
        }
    }

    .stAlert > div {
        background: #161b22 !important;
        border: 1px solid #6bcf7f !important;
        border-radius: 6px !important;
        color: #6bcf7f !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        font-family: 'Fira Code', monospace !important;
        box-shadow: 0 4px 12px rgba(107, 207, 127, 0.1) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🎨 Subtle Binary Background Streams
st.markdown(
    '''
    <div class="binary-stream stream-1">01001000 01100101 01101100 01101100 01101111</div>
    <div class="binary-stream stream-2">01001101 01100001 01110100 01101000</div>
    <div class="binary-stream stream-3">01000011 01101111 01100100 01100101</div>
    <div class="binary-stream stream-4">01000001 01001001 00100000 01001100</div>
    <div class="binary-stream stream-5">01100101 01100001 01110010 01101110</div>
    <div class="binary-stream stream-6">01010000 01111001 01110100 01101000 01101111 01101110</div>
    ''',
    unsafe_allow_html=True
)

# 🎨 Main Container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# 🎯 Terminal Header
st.markdown(
    '''
    <div class="terminal-header">
        <div class="terminal-dots">
            <div class="dot red"></div>
            <div class="dot yellow"></div>
            <div class="dot green"></div>
        </div>
        <div>binary_math_compiler.py</div>
        <div>SESSION: INITIALIZATION</div>
    </div>
    ''',
    unsafe_allow_html=True
)

# 🎯 Application Header
st.markdown(
    '''
    <div class="application-header">
        <div class="app-title">🔢 BINARY MATH COMPILER</div>
        <div class="app-subtitle">// Initialize Learning Protocol</div>
    </div>
    ''',
    unsafe_allow_html=True
)

# 🎯 Code Grid Layout
st.markdown('<div class="code-grid">', unsafe_allow_html=True)

# Grid Item 1: Welcome Block (spans both columns)
st.markdown('<div class="code-block welcome-block">', unsafe_allow_html=True)
st.markdown(
    '''
    <div class="code-header">
        <span class="function-signature">function</span> initializeLearningSession()
        <span>🚀 READY</span>
    </div>
    ''',
    unsafe_allow_html=True
)
st.markdown('<div class="welcome-content">', unsafe_allow_html=True)
st.markdown(
    '<div class="welcome-message">// Initialize user parameters for mathematical computing engine</div>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Grid Item 2: Form Block
st.markdown('<div class="code-block form-block">', unsafe_allow_html=True)
st.markdown(
    '''
    <div class="code-header">
        <span class="function-signature">class</span> UserProfile
        <span>📝 INPUT</span>
    </div>
    ''',
    unsafe_allow_html=True
)

st.markdown('<div class="form-content">', unsafe_allow_html=True)

# 🎯 Collect user info
st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<label class="input-label">username = string</label>', unsafe_allow_html=True)
name = st.text_input("", placeholder="Enter your username...", key="name_input")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<label class="input-label">age = integer</label>', unsafe_allow_html=True)
age = st.number_input("", min_value=4, max_value=18, step=1, value=8, key="age_input")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="input-group">', unsafe_allow_html=True)
st.markdown('<label class="input-label">grade_level = enum</label>', unsafe_allow_html=True)
grade_level = st.selectbox(
    "",
    ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6"],
    index=1,
    key="grade_input"
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Grid Item 3: Features Block
st.markdown('<div class="code-block features-block">', unsafe_allow_html=True)
st.markdown(
    '''
    <div class="code-header">
        <span class="function-signature">array</span> systemCapabilities
        <span>⚡ MODULES</span>
    </div>
    ''',
    unsafe_allow_html=True
)

st.markdown('<div class="features-content">', unsafe_allow_html=True)
st.markdown(
    '''
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🔄</div>
            <div class="feature-text">Adaptive Engine</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-text">Analytics Core</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🏆</div>
            <div class="feature-text">Achievement Sys</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-text">Real-time Proc</div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Grid Item 4: Execute Block
st.markdown('<div class="code-block execute-block">', unsafe_allow_html=True)
st.markdown(
    '''
    <div class="code-header">
        <span class="function-signature">main</span> executeLearningProtocol()
        <span>🔥 COMPILE</span>
    </div>
    ''',
    unsafe_allow_html=True
)

st.markdown('<div class="execute-content">', unsafe_allow_html=True)

# 🎯 Binary Execute Button
if st.button("🔢 COMPILE & EXECUTE", key="binary_launch", help="Initialize binary math learning protocol"):
    if not name:
        st.error("COMPILE_ERROR: Username parameter required for session initialization")
    else:
        # ✅ Create user in backend
        user_id = api.create_user(name, age, grade_level)
        # ✅ Start session
        session_id = api.start_session(user_id)

        # ✅ Store in session_state
        st.session_state["session_id"] = session_id
        st.session_state["student_name"] = name

        st.success(
            f"✅ SESSION_INITIALIZED | User: {name.upper()} | Navigate to **Learn** to execute mathematical algorithms")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close code-grid
st.markdown('</div>', unsafe_allow_html=True)  # Close main-container