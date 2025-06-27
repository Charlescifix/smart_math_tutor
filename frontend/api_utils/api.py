import requests
import os
import streamlit as st
from dotenv import load_dotenv

# ✅ Load environment variables from .env file
load_dotenv()

API_URL = os.getenv("API_URL")

if not API_URL:
    st.error("🔧 CONFIGURATION ERROR: API_URL environment variable is not set!")
    st.info("Please set API_URL in your .env file or deployment secrets")
    st.stop()

def create_user(name, age, grade_level):
    """Create a new user in the system"""
    try:
        payload = {
            "name": name,
            "age": age,
            "grade_level": grade_level
        }
        res = requests.post(f"{API_URL}/create_user", json=payload, timeout=10)
        res.raise_for_status()
        return res.json()["user_id"]
    except requests.exceptions.ConnectionError:
        st.error("🌐 CONNECTION_ERROR: Unable to connect to backend server")
        st.info(f"Backend URL: {API_URL}")
        st.stop()
    except requests.exceptions.Timeout:
        st.error("⏱️ TIMEOUT_ERROR: Backend server is not responding")
        st.stop()
    except requests.exceptions.HTTPError as e:
        st.error(f"🚨 SERVER_ERROR: {e.response.status_code} - {e.response.text}")
        st.stop()
    except KeyError:
        st.error("📝 RESPONSE_ERROR: Invalid response format from server")
        st.stop()
    except Exception as e:
        st.error(f"❌ UNEXPECTED_ERROR: {str(e)}")
        st.stop()

def start_session(user_id):
    """Start a new learning session"""
    try:
        payload = {"user_id": user_id}
        res = requests.post(f"{API_URL}/start_session", json=payload, timeout=10)
        res.raise_for_status()
        return res.json()["session_id"]
    except requests.exceptions.ConnectionError:
        st.error("🌐 CONNECTION_ERROR: Unable to connect to backend server")
        st.stop()
    except requests.exceptions.Timeout:
        st.error("⏱️ TIMEOUT_ERROR: Backend server is not responding")
        st.stop()
    except requests.exceptions.HTTPError as e:
        st.error(f"🚨 SERVER_ERROR: {e.response.status_code} - {e.response.text}")
        st.stop()
    except KeyError:
        st.error("📝 RESPONSE_ERROR: Invalid response format from server")
        st.stop()
    except Exception as e:
        st.error(f"❌ UNEXPECTED_ERROR: {str(e)}")
        st.stop()

def get_next_question(session_id):
    """Get the next question for the session"""
    try:
        res = requests.get(f"{API_URL}/next_question/{session_id}", timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.ConnectionError:
        st.error("🌐 CONNECTION_ERROR: Unable to connect to backend server")
        return {"question_text": "ERROR: Connection failed"}
    except requests.exceptions.Timeout:
        st.error("⏱️ TIMEOUT_ERROR: Backend server is not responding")
        return {"question_text": "ERROR: Server timeout"}
    except requests.exceptions.HTTPError as e:
        st.error(f"🚨 SERVER_ERROR: {e.response.status_code} - {e.response.text}")
        return {"question_text": "ERROR: Server error"}
    except Exception as e:
        st.error(f"❌ UNEXPECTED_ERROR: {str(e)}")
        return {"question_text": "ERROR: Unknown error"}

def submit_answer(session_id, student_answer):
    """Submit student answer and get feedback"""
    try:
        payload = {
            "session_id": session_id,
            "student_answer": student_answer
        }
        res = requests.post(f"{API_URL}/submit_answer", json=payload, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.ConnectionError:
        st.error("🌐 CONNECTION_ERROR: Unable to connect to backend server")
        return {
            "feedback": "ERROR: Connection failed",
            "score": 0,
            "streak": 0,
            "badge": "❌"
        }
    except requests.exceptions.Timeout:
        st.error("⏱️ TIMEOUT_ERROR: Backend server is not responding")
        return {
            "feedback": "ERROR: Server timeout",
            "score": 0,
            "streak": 0,
            "badge": "⏱️"
        }
    except requests.exceptions.HTTPError as e:
        st.error(f"🚨 SERVER_ERROR: {e.response.status_code} - {e.response.text}")
        return {
            "feedback": f"ERROR: Server error {e.response.status_code}",
            "score": 0,
            "streak": 0,
            "badge": "🚨"
        }
    except Exception as e:
        st.error(f"❌ UNEXPECTED_ERROR: {str(e)}")
        return {
            "feedback": f"ERROR: {str(e)}",
            "score": 0,
            "streak": 0,
            "badge": "❌"
        }

# ✅ Health check function for debugging
def check_backend_health():
    """Check if backend is accessible"""
    try:
        res = requests.get(f"{API_URL}/docs", timeout=5)
        if res.status_code == 200:
            st.success(f"✅ Backend is healthy: {API_URL}")
            return True
        else:
            st.warning(f"⚠️ Backend responded with status: {res.status_code}")
            return False
    except Exception as e:
        st.error(f"❌ Backend health check failed: {str(e)}")
        return False

# ✅ Display current configuration (for debugging)
def show_config():
    """Display current API configuration"""
    st.sidebar.write("🔧 **API Configuration**")
    st.sidebar.write(f"Backend URL: `{API_URL}`")
    if st.sidebar.button("🔍 Test Connection"):
        check_backend_health()