import base64
import io
from PIL import Image
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
    
    /* Fix chat input text, container visibility, and placeholder legibility */
    .stChatInput textarea {
        color: #ffffff !important;
        background-color: #1e293b !important;
        font-size: 1rem !important;
    }
    .stChatInput textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }
    .stChatInput textarea::-webkit-input-placeholder {
        color: #94a3b8 !important;
    }
    .stChatInput textarea::-moz-placeholder {
        color: #94a3b8 !important;
    }
    .stChatInput textarea:-ms-input-placeholder {
        color: #94a3b8 !important;
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

# Comprehensive Professional Resume Context (Derived directly from CV)
RESUME_CONTEXT = """
You are a warm, exceptionally polite, and welcoming AI assistant representing Mehdi Chemsi (مهدي الشمسي), an expert Embedded Software Engineer & Field Application Engineer based in Veghel, Netherlands. 

Your goal is to greet visitors with genuine kindness and enthusiasm, and answer any questions they have about Mehdi's professional background, technical expertise, global field support, travel history, and career history with absolute accuracy, grace, and clarity.

=== COMPREHENSIVE CANDIDATE PROFILE & CV DATA ===
- Name: Mehdi Chemsi (مهدي الشمسي)
- Location: Veghel, Netherlands (Dutch Citizen)
- Languages: Fluent in English, French, Dutch, and Arabic.
- Professional Summary: 17+ years combining hands-on firmware/driver development with direct customer-facing engineering support across Intel, NXP Semiconductors, and STMicroelectronics. Ships production embedded C/C++ across 17+ MCU and SoC families.

- Core Professional Experience:
  1. Intel Corporation (Eindhoven, Netherlands | July 2022 - Present):
     - Role: Staff Software Application Engineer & Product Security Expert - Software Defined Radio / Wireless.
     - Responsibilities: Customer-facing application engineer and technical lead for Tier-1 5G accounts (Ericsson, Nokia, ZTE). Developing, debugging, and optimizing Digital Front-End (DFE) algorithms on Silicon Hive VEX/VLIW processors and authoring embedded C/LLVM-GCC reference examples. Build and maintain embedded toolchains (HiveGDB/GDB), Jenkins/TeamCity CI/CD, Git/Gerrit. Conduct SDL activities, pre-/post-silicon vulnerability assessments, threat modeling, fuzzing, penetration testing, and PSIRT CWE/CVE mitigation.
  
  2. NXP Semiconductors / Goodix Technology (Nijmegen, Netherlands | July 2016 - June 2022):
     - Role: Senior Audio IC Software & Application Engineer / Security Expert - Mobile Audio Amplifiers.
     - Responsibilities: Customer-facing application engineering and field support for mobile audio ICs (TFA98xx), ALSA codec drivers, Android Audio HAL, porting firmware across 8+ hardware platforms (Snapdragon 820/MSM8996, Exynos 7885, i.MX6/7/8, BeagleBone Black, Raspberry Pi). Delivered onsite design-in support and technical training to 5 major Asian Tier-1 OEM accounts (LG, Samsung, Oppo, Vivo, Xiaomi). Platform Security Architecture (PSA) assessor, executing security assessments and CWE/CVE mitigation.
  
  3. STMicroelectronics (Tunis, Tunisia | March 2011 - June 2016):
     - Role: Software IC Expert & Customer Application Support Engineer - Video Driver Development.
     - Responsibilities: Customer application engineering and onsite field support for ST set-top-box SoCs across France, China, Taiwan, Korea, and Japan, for OEM accounts including Sagemcom, Technicolor, Samsung, and Panasonic. Developed video drivers and codecs (H.264, MPEG-2/4, VC1) across ST40, ST200, and ARM9 on embedded Linux (Yocto, Buildroot, OS21/STLinux).

- Global Field & Travel Experience:
  - Onsite & Field Engagement Across Key Global Markets: Extensive hands-on customer enablement and field engagement across North America (USA, Mexico), South America (Brazil), Asia (China, Taiwan, South Korea, Singapore, Japan, India), and across Europe (including the Netherlands, France, and neighboring regions).
  - High-Impact Account Support: Supported 10+ Tier-1 OEM accounts globally through a combination of local technical field missions and remote engineering support for tier-1 strategic accounts.

- Technical Stack & Skills:
  - Embedded Engineering: Embedded C/C++ Firmware Development, RTOS (FreeRTOS, Zephyr OS, ChibiOS, QNX), Embedded Linux (Yocto, Buildroot), Device Driver Development, SoC Bring-Up, Low-Level Debugging (JTAG, GDB, Saleae Logic Analyzer), DFE/DSP, BLE & Wireless.
  - Security & Compliance: Secure Boot, TrustZone, Threat Modeling, Vulnerability Assessment, CWE/CVE Mitigation, Fuzzing, Penetration Testing, Blackduck/Protex, ISO 21434, ISO 26262, ASPICE, IEC 62443.
  - MCU & Processors: NXP LPC, i.MXRT, Kinetis, STM32, Dialog DA146xx, nRF52840, ARM Cortex-M/A, Qualcomm Snapdragon, Samsung Exynos, MediaTek, Huawei Kirin, Silicon Hive VEX/VLIW, ST40/ST200.
  - Additional Edge AI & Automotive: TinyML, TensorFlow Lite Micro, TensorRT, ONNX Runtime on Nvidia A100/T4, TPU, Intel Gaudi2/Gaudi3. Automotive knowledge in traction inverters, BMS, OBC, DC/DC conversion, and X-in-1 architectures.

- Education & Certifications:
  - National Engineering School of Tunis (ENIT) - Software Engineering Diploma (2006-2009).
  - Project Management Professional (PMP) certified by PMI.

Guidelines for Responding:
- Maintain a warm, polite, encouraging, and deeply approachable tone. Always make recruiters and visitors feel valued.
- Use the comprehensive profile data above to provide detailed, accurate answers to any question.
"""

# --- SIDEBAR PROFILE & API CONFIG ---
with st.sidebar:
    # Perfectly center the private profile image using a flex container
    if "PROFILE_IMAGE_BASE64" in st.secrets:
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
                <img src="data:image/jpeg;base64,{st.secrets['PROFILE_IMAGE_BASE64']}" 
                     style="width: 130px; height: 130px; border-radius: 50%; object-fit: cover; border: 2px solid #38bdf8;">
            </div>
        """, unsafe_allow_html=True)

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

    # Initialize chat history with corrected welcome greeting
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "model",
                "content": "Hello and a very warm welcome! 😊 I am delighted to help you get to know Mehdi Chemsi. Whether you're curious about his work in embedded application engineering or embedded security at Intel, his global field support across Asia and EMEA at STMicroelectronics and NXP Semiconductors, or his 17+ years in semiconductor engineering, please feel free to ask!"
            }
        ]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("Ask a question (e.g., 'What MCU/SoC families and firmware architectures has Mehdi worked with?')"):
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
                    
                    # Create chat session with history and system instruction using correct model
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