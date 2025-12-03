import streamlit as st
import requests
import base64

# --- CONFIGURATION ---
API_URL = "http://localhost:8000/api/chat"
PAGE_TITLE = "DevFlow | AI Squad"
PAGE_ICON = "⚡"

# Update this path to your local image
LOCAL_IMAGE_PATH = r"D:\Generative AI\Google_Agentic_AI\UI\Background.png" 

# --- PAGE SETUP ---
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# --- FUNCTION TO LOAD LOCAL IMAGE ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

img_base64 = get_base64_of_bin_file(LOCAL_IMAGE_PATH)

# --- CSS STYLING ---
# 1. BACKGROUND HANDLING
if img_base64:
    bg_style = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(5, 5, 10, 0.85), rgba(5, 5, 10, 0.85)), 
                          url("data:image/png;base64,{img_base64}");
        background-size: cover; 
        background-position: center top; 
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
else:
    bg_style = "<style>.stApp {background-color: #0E1117;}</style>"

st.markdown(bg_style, unsafe_allow_html=True)

# --- CUSTOM UI CSS ---
st.markdown("""
<style>
    /* 2. TEXT COLORS */
    h1 {
        color: #00FF88 !important; 
        font-family: 'Courier New', monospace;
        font-weight: 800;
        text-shadow: 0px 0px 15px rgba(0, 255, 136, 0.6);
        letter-spacing: 1.5px;
    }
    h2, h3 { color: #E0E0E0 !important; }
    p, .stMarkdown { color: #CDCDCD !important; font-size: 1.05rem; }

    /* 3. RESET BUTTON STYLING */
    div.stButton > button {
        background-color: transparent;
        border: 1px solid #00FF88;
        color: #00FF88;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #00FF88;
        color: #000000;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.6);
    }

    /* 4. CHAT MESSAGES */
    .stChatMessage {
        background-color: rgba(25, 30, 40, 0.95);
        border: 1px solid #444;
        border-radius: 12px;
    }
    
    /* 5. INFO BOX */
    .info-box {
        background-color: rgba(20, 20, 20, 0.7);
        border-left: 5px solid #00FF88;
        padding: 25px;
        border-radius: 8px;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }

    /* 6. SIDEBAR STYLING (The Fix for Scrolling) */
    section[data-testid="stSidebar"] {
        background-color: #020202; 
        border-right: 1px solid #222;
    }
    
    /* REMOVE TOP PADDING IN SIDEBAR TO SAVE SPACE */
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* 7. INPUT BOX */
    .stTextInput > div > div > input {
        background-color: #0F0F0F;
        color: #fff;
        border: 1px solid #333;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00FF88;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTENT ---
with st.sidebar:
    # A. TOP ICON
    st.image("https://cdn-icons-png.flaticon.com/512/10464/10464673.png", width=80) 
    
    # B. BACKGROUND PREVIEW (Compact Version)
    if img_base64:
        st.markdown(f"""
        <div style="margin-top: 10px; margin-bottom: 20px; text-align: left;">
            <div style="font-size: 10px; color: #555; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;">Active Env</div>
            <div style="
                width: 100%; 
                height: 60px; 
                background-image: url('data:image/png;base64,{img_base64}'); 
                background-size: cover; 
                background-position: center; 
                border-radius: 6px; 
                border: 1px solid #333; 
                opacity: 0.7;">
            </div>
        </div>
        """, unsafe_allow_html=True)

    # C. SYSTEM STATUS
    st.markdown("### System Status")
    # st.markdown("---") # Removed to save space
    
    # Compact Status Rows
    def status_row(color, label, status):
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(f"<div style='margin-top:5px; width:10px; height:10px; background-color:{color}; border-radius:50%; box-shadow: 0 0 5px {color};'></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<span style='color:white; font-weight:bold;'>{label}</span> <span style='color:{color}; font-size:0.8rem; margin-left:5px'>[{status}]</span>", unsafe_allow_html=True)

    status_row("#00FF88", "DevFlow Core", "ONLINE") 
    status_row("#00CCFF", "Sprint Lead", "READY")   
    status_row("#D000FF", "Dev Expert", "STANDBY")  
        
    st.write("") 
    st.write("") 
    
    # Spacer to push reset button down slightly (optional)
    if st.button("RESET OPERATIONS", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CONTENT ---

# TITLE
st.title("DevFlow - AI Engineering Squad")

# DESCRIPTION
st.markdown("""
<div class="info-box">
    <h3 style="margin-top:0; color:white;">⚡ Squad Operations Center</h3>
    <p>
        System Online. Your autonomous team is standing by.
        <br><br>
        The <strong>Orchestrator</strong> delegates tasks in real-time:
        <br>
        🔹 <span style="color:#00CCFF; font-weight:bold;">Sprint Lead</span> manages <strong>Jira</strong> tickets.
        <br>
        🟣 <span style="color:#D000FF; font-weight:bold;">Dev Expert</span> handles <strong>GitHub</strong> code.
    </p>
</div>
""", unsafe_allow_html=True)

# --- CHAT LOGIC ---

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
if prompt := st.chat_input("Command the squad (e.g., 'Check Jira bugs and assign them to the repo')"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Orchestrating Agents..."):
            try:
                payload = {"query": prompt, "session_id": "hackathon-demo-1"}
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    agent_reply = data.get("response", "No response received.")
                    message_placeholder.markdown(agent_reply)
                    st.session_state.messages.append({"role": "assistant", "content": agent_reply})
                else:
                    message_placeholder.error(f"Backend Error: {response.status_code}")
                    
            except Exception as e:
                message_placeholder.error(f"⚠️ Connection Failed. Ensure 'app.py' is running.")