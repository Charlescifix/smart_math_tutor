# Fix import path for pages/ subfolder
import sys
import os
from pathlib import Path

# Add the frontend directory to Python path (go up one level from pages/)
frontend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(frontend_dir))

import streamlit as st

# Now import your local api_utils
try:
    from api_utils import api
except ImportError:
    # Fallback: try direct import
    import api_utils.api as api

# 🎨 Page Config
st.set_page_config(
    page_title="Binary Math Compiler - Learning Interface",
    page_icon="🔢",
    layout="wide"
)

# 🎯 Validate session - Complete check
if "session_id" not in st.session_state or st.session_state.get("session_id") is None:
    st.markdown(
        '''
        <div style="
            background: linear-gradient(135deg, rgba(255, 0, 0, 0.1), rgba(200, 0, 0, 0.1));
            border: 2px solid #ff4444;
            padding: 2rem;
            text-align: center;
            margin: 2rem;
            color: #ff4444;
            font-family: 'Courier New', monospace;
            font-size: 1.4rem;
            font-weight: 700;
        ">
            ERROR 404: SESSION_NOT_FOUND<br>
            >> RETURN TO HOME TO INITIALIZE BINARY PROTOCOL
        </div>
        ''',
        unsafe_allow_html=True
    )
    st.stop()

# 🎯 Initialize state if needed - Only after confirming session exists
if "question" not in st.session_state:
    try:
        st.session_state["question"] = api.get_next_question(st.session_state["session_id"])
        st.session_state["feedback"] = None
        st.session_state["score"] = 0
        st.session_state["streak"] = 0
        st.session_state["badge"] = "🌟"
    except Exception as e:
        st.error(f"RUNTIME_ERROR: {str(e)}")
        st.stop()

question = st.session_state.get("question", {"question_text": "ERROR: No question loaded"})

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
        background-size: 25px 25px;
        pointer-events: none;
        z-index: 0;
    }

    .main-container {
        background: rgba(13, 17, 23, 0.95);
        border: 1px solid #30363d;
        border-radius: 6px;
        margin: 1rem auto;
        max-width: 1200px;
        position: relative;
        z-index: 1;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
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

    .user-status {
        background: linear-gradient(90deg, #1f2937, #374151);
        border: 1px solid #4b5563;
        padding: 1rem 2rem;
        margin: 1.5rem;
        border-radius: 4px;
        text-align: center;
    }

    .user-info {
        font-family: 'Fira Code', monospace;
        color: #6bcf7f;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: 1px;
    }

    .code-block {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 6px;
        margin: 2rem 1.5rem;
        overflow: hidden;
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

    .question-algorithm {
        padding: 3rem 2rem;
        text-align: center;
        background: #0d1117;
    }

    .mathematical-expression {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 4rem !important;
        font-weight: 800 !important;
        color: #58a6ff !important;
        margin: 0 !important;
        line-height: 1.2;
        text-shadow: 0 0 20px rgba(88, 166, 255, 0.3);
        letter-spacing: 2px;
    }

    .input-function {
        padding: 2rem 1.5rem;
        background: #161b22;
    }

    .input-label {
        font-family: 'Fira Code', monospace;
        font-size: 1rem;
        color: #ffa657;
        margin-bottom: 1rem;
        font-weight: 600;
    }

    .stTextInput > div > div > input {
        background: #0d1117 !important;
        border: 2px solid #30363d !important;
        border-radius: 6px !important;
        padding: 1.5rem !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        font-family: 'JetBrains Mono', monospace !important;
        color: #6bcf7f !important;
        text-align: center !important;
        transition: all 0.2s ease !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }

    .stTextInput > div > div > input:focus {
        border: 2px solid #58a6ff !important;
        box-shadow: 
            inset 0 2px 4px rgba(0, 0, 0, 0.2),
            0 0 0 3px rgba(88, 166, 255, 0.1) !important;
        background: #161b22 !important;
        color: #ffffff !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #6e7681 !important;
        font-family: 'Fira Code', monospace !important;
        font-size: 1rem !important;
    }

    .execute-button {
        background: linear-gradient(135deg, #238636, #2ea043) !important;
        border: 1px solid #2ea043 !important;
        border-radius: 6px !important;
        padding: 1rem 2rem !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        font-family: 'Fira Code', monospace !important;
        color: #ffffff !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        width: 100% !important;
        margin-top: 1rem !important;
        box-shadow: 0 4px 12px rgba(46, 160, 67, 0.2) !important;
    }

    .execute-button:hover {
        background: linear-gradient(135deg, #2ea043, #46954a) !important;
        border-color: #46954a !important;
        box-shadow: 0 6px 16px rgba(46, 160, 67, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    .output-terminal {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 6px;
        margin: 2rem 1.5rem;
        overflow: hidden;
    }

    .output-header {
        background: #21262d;
        border-bottom: 1px solid #30363d;
        padding: 0.75rem 1rem;
        font-family: 'Fira Code', monospace;
        font-size: 0.85rem;
        color: #7d8590;
    }

    .output-content {
        padding: 1.5rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.3rem;
        font-weight: 600;
        color: #6bcf7f;
        text-align: center;
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .analytics-dashboard {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        margin: 2rem 1.5rem 1.5rem 1.5rem;
        overflow: hidden;
    }

    .dashboard-header {
        background: #21262d;
        border-bottom: 1px solid #30363d;
        padding: 1rem;
        font-family: 'Fira Code', monospace;
        font-size: 1rem;
        color: #ffa657;
        font-weight: 600;
        text-align: center;
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        padding: 1.5rem;
        gap: 1.5rem;
    }

    .metric-card {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        border-color: #58a6ff;
        box-shadow: 0 4px 12px rgba(88, 166, 255, 0.1);
        transform: translateY(-2px);
    }

    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }

    .metric-label {
        font-family: 'Fira Code', monospace;
        font-size: 0.85rem;
        color: #7d8590;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 800;
        color: #58a6ff;
    }

    .binary-stream {
        position: fixed;
        font-family: 'JetBrains Mono', monospace;
        color: rgba(88, 166, 255, 0.05);
        font-size: 0.8rem;
        pointer-events: none;
        z-index: 0;
        animation: binaryFloat 12s linear infinite;
    }

    .stream-1 { top: 10%; left: 5%; animation-delay: 0s; }
    .stream-2 { top: 30%; right: 8%; animation-delay: 3s; }
    .stream-3 { bottom: 20%; left: 10%; animation-delay: 6s; }
    .stream-4 { bottom: 40%; right: 15%; animation-delay: 9s; }

    @keyframes binaryFloat {
        0% { 
            transform: translateY(0px);
            opacity: 0.05;
        }
        50% { 
            transform: translateY(-10px);
            opacity: 0.08;
        }
        100% { 
            transform: translateY(0px);
            opacity: 0.05;
        }
    }

    .stAlert > div {
        background: #161b22 !important;
        border: 1px solid #da3633 !important;
        border-radius: 6px !important;
        color: #ff6b6b !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        font-family: 'Fira Code', monospace !important;
        box-shadow: 0 4px 12px rgba(218, 54, 51, 0.1) !important;
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
    <div class="binary-stream stream-4">01000001 01001001 00100000 01001100 01100101 01100001 01110010 01101110</div>
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
        <div>RUNTIME: ACTIVE</div>
    </div>
    ''',
    unsafe_allow_html=True
)

# 🎯 User Status
if "student_name" in st.session_state:
    st.markdown(
        f'''
        <div class="user-status">
            <div class="user-info">USER: {st.session_state["student_name"].upper()} | STATUS: CONNECTED</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

# 🎯 Mathematical Expression Algorithm Block
st.markdown(
    f'''
    <div class="code-block">
        <div class="code-header">
            <span class="function-signature">function</span> calculateExpression()
            <span>⚡ EXECUTE</span>
        </div>
        <div class="question-algorithm">
            <div class="mathematical-expression">{question["question_text"]}</div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# 🎯 Input Function Block
st.markdown('<div class="code-block">', unsafe_allow_html=True)
st.markdown(
    '''
    <div class="code-header">
        <span class="function-signature">input</span> submitSolution()
        <span>📝 COMPILE</span>
    </div>
    ''',
    unsafe_allow_html=True
)

st.markdown('<div class="input-function">', unsafe_allow_html=True)
st.markdown('<div class="input-label">>> Enter solution value:</div>', unsafe_allow_html=True)

answer = st.text_input("", key="answer_input", placeholder="Type answer...")

if st.button("⚡ EXECUTE CALCULATION", key="execute_btn", help="Compile and execute solution"):
    if not answer.strip():
        st.warning("COMPILE_ERROR: Input buffer empty. Solution required.")
    else:
        # Submit to backend
        feedback_data = api.submit_answer(st.session_state["session_id"], answer.strip())

        # Update state
        st.session_state["feedback"] = feedback_data["feedback"]
        st.session_state["score"] = feedback_data["score"]
        st.session_state["streak"] = feedback_data["streak"]
        st.session_state["badge"] = feedback_data["badge"]

        # Load next question
        st.session_state["question"] = api.get_next_question(st.session_state["session_id"])

        # Clear answer input
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 🎯 Output Terminal
if st.session_state.get("feedback"):
    st.markdown(
        f'''
        <div class="output-terminal">
            <div class="output-header">console.log() - Algorithm Output</div>
            <div class="output-content">{st.session_state["feedback"]}</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

# 🎯 Analytics Dashboard
st.markdown(
    f'''
    <div class="analytics-dashboard">
        <div class="dashboard-header">PERFORMANCE ANALYTICS</div>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-icon">🎯</div>
                <div class="metric-label">Score</div>
                <div class="metric-value">{st.session_state.get("score", 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">🔥</div>
                <div class="metric-label">Streak</div>
                <div class="metric-value">{st.session_state.get("streak", 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">{st.session_state.get("badge", "🌟")}</div>
                <div class="metric-label">Badge</div>
                <div class="metric-value">EARNED</div>
            </div>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)