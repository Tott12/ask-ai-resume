import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="Mehdi Chemsi - Ask AI Resume",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for high contrast, dark sidebar, and crystal clear readability
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Force sidebar to dark mode with bright white text */
    [data-testid="stSidebar"] {
        background-color: #0b1329 !important;
        color: #f8fafc !important;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] li, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #f8fafc !important;
        font-size: 0.95rem !important;
    }
    
    /* Force crystal-clear high-contrast bright white text for all chat messages and bullet points */
    .stChatMessage p, .stChatMessage li, .stChatMessage span, .stMarkdown p, .stMarkdown li {
        color: #ffffff !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }
    
    /* Fix chat input text and container visibility */
    .stChatInput textarea {
        color: #ffffff !important;
        background-color: #1e293b !important;
        font-size: 1rem !important;
    }
    .stChatInputContainer {
        background-color: #1e293b !important;
        border: 1px solid #475569 !important;
        border-radius: 12px !important;
    }
    
    .profile-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Kinder, Warmer Professional Resume Context / System Instructions
RESUME_CONTEXT = """
You are a warm, exceptionally polite, and welcoming AI assistant representing Mehdi Chemsi (مهدي الشمسي), a Senior Software Product Application and Embedded Security Engineer based in Veghel, Netherlands. 

Your goal is to greet anyone visiting this page with genuine kindness and enthusiasm, and to answer any questions they have about Mehdi's professional background, technical expertise, firmware debugging, customer support, and field engineering experience with grace and clarity.

Candidate Profile Summary:
- Name: Mehdi Chemsi (مهدي الشمسي)
- Location: Veghel, Netherlands
- Current Role: Senior Software Product Application and Embedded Security Engineer at Intel Corporation.
- Career Background: Extensive semiconductor industry experience spanning software development, System-on-Chip (SoC) architecture, firmware engineering, hardware security, customer support, and field engineering across companies including STMicroelectronics, NXP Semiconductors, and Intel Corporation.
- Core Technical Expertise:
  * Embedded Systems & Processors: VLIW core architectures, Cadence Tensilica Vision 341 DSPs, microcontrollers (STM32, Raspberry Pi), RTOS (FreeRTOS, Zephyr).
  * Firmware & Debugging: Low-level firmware development, advanced debugging, compiler toolchains (GCC, LLVM, GDB, CMake, Xtensa Xplorer IDE).
  * Hardware Security & Compliance: Root of Trust, Secure Boot, Trusted Execution Environments, ARM TrustZone, TPM, Hardware Security Modules (HSMs), FIPS 140-3 certifiability, and EU Cyber Resilience Act compliance.
  * Customer Enablement & Field Engineering: Technical customer support, product application engineering, guiding tier-1 clients through hardware/software integration and troubleshooting.
  * Software & Development Tooling: Linux environments, WSL2, Ubuntu, Bash, Zsh, Git, OpenSSL, Python, C/C++, and static analysis tools.
- Languages: Fluent in English, French, and Arabic.

Guidelines for Responding:
- Maintain a warm, polite, encouraging, and deeply approachable tone. Always make recruiters and visitors feel valued.
- Highlight his strengths in bridging deep engineering (firmware debugging, SoC security) with customer success and field engineering enablement.
- Base your answers strictly on the profile details provided above. If asked about something outside this scope, politely and warmly clarify or pivot to related engineering strengths.
"""

# --- SIDEBAR PROFILE & API CONFIG ---
with st.sidebar:
    st.markdown("""
        <div class="profile-card">
            <h2 style="margin:0; font-size: 1.25rem; color: #f8fafc;">Mehdi Chemsi</h2>
            <p style="margin:5px 0 0 0; font-size: 0.85rem; color: #94a3b8;">Senior Field Application and Support Engineer</p>
            <p style="margin:5px 0 0 0; font-size: 0.85rem; color: #94a3b8;">Senior Embedded Software Engineer</p>
            <p style="margin:5px 0 0 0; font-size: 0.85rem; color: #94a3b8;">Senior Embedded Security Engineer</p>
            <p style="margin:5px 0 0 0; font-size: 0.75rem; color: #38bdf8;">📍 Veghel, The Netherlands • Intel Corporation</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Quick Background")
    st.markdown(
        "- **Current:** Intel Corporation\n"
        "- **Specialty:** SoC Architecture & Hardware Security\n"
        "- **Engineering:** Firmware Development & Advanced Debugging\n"
        "- **Field Role:** Product Application & Customer Engineering\n"
        "- **Stack:** C/C++, Python, Linux, VLIW, FreeRTOS"
    )
    
    st.markdown("---")
    
    api_key = None
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = st.text_input("Gemini API Key (Local Testing)", type="password", help="Enter your Google AI Studio key for local testing.")

# --- MAIN CHAT INTERFACE ---
st.markdown("<h1 style='text-align: center; font-size: 2rem; margin-bottom: 0;'>💬 Ask AI Resume</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 30px;'>It is a pleasure to welcome you! Feel free to explore Mehdi's engineering background below.</p>", unsafe_allow_html=True)

if not api_key:
    st.warning("⚠️ Please provide a Gemini API Key in the sidebar to start the chat for local testing.")
else:
    client = genai.Client(api_key=api_key)

    # Initialize chat history with a kinder greeting
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "model",
                "content": "Hello and a very warm welcome! 😊 I am delighted to help you get to know Mehdi Chemsi. Whether you're curious about his embedded security work at Intel, firmware development and debugging, or his customer support and field engineering experience, please feel free to ask!"
            }
        ]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("Ask a question (e.g., 'What is Mehdi's experience with firmware debugging and customer support?')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("model"):
            with st.spinner("Thinking..."):
                try:
                    # Format past messages correctly for the SDK chat API
                    formatted_history = [
                        {
                            "role": "user" if m["role"] == "user" else "model",
                            "parts": [{"text": m["content"]}]
                        }
                        for m in st.session_state.messages[:-1]
                    ]
                    
                    # Create chat session with history and system instruction
                    chat = client.chats.create(
                        model='gemini-3.6-flash',
                        history=formatted_history,
                        config={
                            'system_instruction': RESUME_CONTEXT,
                            'temperature': 0.3,
                        }
                    )
                    
                    response = chat.send_message(prompt)
                    reply = response.text
                    st.markdown(reply)
                except Exception as e:
                    reply = f"An error occurred: {e}"
                    st.error(reply)

        st.session_state.messages.append({"role": "model", "content": reply})