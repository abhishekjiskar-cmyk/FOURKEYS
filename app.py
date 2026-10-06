"""
Streamlit Web Interface for Multi-Agent Gemma System
"""
import streamlit as st
import time
from agents import MultiAgentSystem, SingleAgentBaseline
from reconciliation import Reconciler, analyze_disagreements
from test_dataset import TEST_CASES, get_all_domains
import json

# Page config
st.set_page_config(
    page_title="Multi-Agent Gemma System",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'system_initialized' not in st.session_state:
    st.session_state.system_initialized = False
    st.session_state.use_api = True
    st.session_state.multi_agent = None
    st.session_state.single_agent = None
    st.session_state.reconciler = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def initialize_system(use_api: bool, local_model_name: str = "google/gemma-2b-it"):
    """Initialize the multi-agent system"""
    with st.spinner("🔄 Initializing AI models..."):
        try:
            st.session_state.multi_agent = MultiAgentSystem(use_api=use_api, model_name=local_model_name)
            st.session_state.single_agent = SingleAgentBaseline(use_api=use_api, model_name=local_model_name)
            st.session_state.reconciler = Reconciler()
            st.session_state.system_initialized = True
            st.session_state.use_api = use_api
            st.session_state.current_model = "Gemini API" if use_api else local_model_name
            st.success(f"✅ System initialized with {st.session_state.current_model}!")
        except Exception as e:
            st.error(f"Failed to load {local_model_name}")
            error_str = str(e).lower()
            if "gated repo" in error_str or "401" in error_str or "unauthorized" in error_str:
                st.error("🔒 **Authentication Error:** This model is restricted. You must accept the terms on HuggingFace and add a valid `HF_TOKEN` to your `.env` file. \n\n*Alternatively, please select an open, non-gated model like **Qwen** or **Phi-3** from the dropdown!*")
            else:
                st.error(f"Error: {e}")

def main():
    import streamlit.components.v1 as components
    
    INJECTED_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:wght@300;400;600;700&family=JetBrains+Mono:wght@400&display=swap');

    /* Global overrides */
    .stApp { background: transparent !important; background-color: transparent !important; cursor: none !important; }
    .stApp > header { background-color: transparent !important; }

    /* Base text (excluding spans to prevent breaking Material Icons) */
    body, .stApp, p, h1, h2, h3, h4, h5, h6, label, button, input, textarea, .stMarkdown { font-family: 'Space Grotesk', sans-serif !important; }
    p, span, div, h1, h2, h3, h4, h5, h6, label { color: #F0F4F8 !important; font-weight: 400; }
    strong, b { font-weight: 600 !important; color: #FFFFFF !important; }

    /* Centered Chat-like Layout */
    .block-container { max-width: 100% !important; padding: 2rem 4rem !important; }

    /* Sidebar styling - Lighter glass */
    [data-testid="stSidebar"] { background-color: rgba(20, 25, 40, 0.5) !important; backdrop-filter: blur(25px) !important; border-right: 1px solid rgba(0, 229, 255, 0.15) !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { font-family: 'JetBrains Mono', monospace !important; font-size: 13px !important; letter-spacing: 0.05em; }

    /* Inputs - Bright Glowing Chatbox */
    .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 229, 255, 0.3) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 1.1rem !important;
        line-height: 1.5 !important;
        box-shadow: inset 0 0 10px rgba(0, 229, 255, 0.05), 0 4px 20px rgba(0,0,0,0.5) !important;
        transition: all 0.3s ease !important;
    }
    .stTextArea>div>div>textarea:focus { border-color: #00E5FF !important; box-shadow: inset 0 0 15px rgba(0, 229, 255, 0.1), 0 0 30px rgba(0, 229, 255, 0.3) !important; }

    /* Fix Selectbox Arrow Overlap & Match Styling */
    [data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    [data-baseweb="select"] div {
        color: #F0F4F8 !important;
    }
    /* Force long text to truncate instead of overlapping the arrow */
    [data-baseweb="select"] div[class*="singleValue"] {
        padding-right: 40px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: rgba(255,255,255,0.08) !important; 
        color: #F0F4F8 !important; 
        border: 1px solid rgba(255, 255, 255, 0.15) !important; 
        border-radius: 30px !important; 
        height: auto !important;
        min-height: 42px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; 
    }
    .stButton > button[data-testid="baseButton-primary"] { 
        background: linear-gradient(135deg, #7C6CFF 0%, #00E5FF 100%) !important;
        color: #050506 !important; 
        border: none !important; 
        font-weight: 700 !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.4) !important;
        animation: pulseGlow 2s infinite alternate !important;
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 15px rgba(124, 108, 255, 0.4); }
        100% { box-shadow: 0 0 35px rgba(0, 229, 255, 0.8); }
    }
    .stButton > button:hover { transform: translateY(-2px) scale(1.02); background-color: rgba(255,255,255,0.15) !important; }
    .stButton > button[data-testid="baseButton-primary"]:hover { 
        background: linear-gradient(135deg, #8b7dff 0%, #33edff 100%) !important;
        box-shadow: 0 0 40px rgba(0, 229, 255, 0.9) !important; 
    }
    
    /* Force text inside buttons to inherit the button color */
    .stButton > button p, .stButton > button span, .stButton > button div { color: inherit !important; }

    /* Expanders & Cards (AI Responses) - Lighter Glass */
    [data-testid="stExpander"] { 
        background: rgba(255, 255, 255, 0.04) !important; 
        backdrop-filter: blur(30px) !important; 
        border: 1px solid rgba(0, 229, 255, 0.15) !important; 
        border-radius: 16px !important; 
        margin-bottom: 12px !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stExpander"]:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(0, 229, 255, 0.4) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3), 0 0 20px rgba(0, 229, 255, 0.15) !important;
        transform: translateY(-2px);
    }
    .streamlit-expanderHeader p { font-family: 'JetBrains Mono', monospace !important; color: #00E5FF !important; font-size: 14px !important; }

    /* File Uploader - Bright Futuristic Dropzone */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 2px dashed rgba(0, 229, 255, 0.4) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        padding: 10px !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #00E5FF !important;
        background: rgba(0, 229, 255, 0.05) !important;
        box-shadow: inset 0 0 20px rgba(0, 229, 255, 0.2) !important;
    }

    /* Hide default cursor on interactables */
    a, button, input, textarea, select, [data-testid="stFileUploader"] { cursor: none !important; }

    /* Hide Tabs for a cleaner look, but keep them clickable */
    [data-testid="stTabs"] button { font-family: 'Space Grotesk', sans-serif !important; font-size: 13px !important; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600 !important; opacity: 0.6; transition: all 0.3s ease; }
    [data-testid="stTabs"] button[aria-selected="true"] { opacity: 1; color: #00E5FF !important; border-bottom-color: #00E5FF !important; text-shadow: 0 0 15px rgba(0, 229, 255, 0.5); }
    [data-testid="stTabs"] button:hover { opacity: 1; color: #7C6CFF !important; }
    </style>
    """

    INJECTED_JS = """
    <script>
    (function() {
        const parentDoc = window.parent.document;
        if (parentDoc.getElementById('custom-bg-injected')) return;

        const flag = parentDoc.createElement('div');
        flag.id = 'custom-bg-injected';
        flag.style.display = 'none';
        parentDoc.body.appendChild(flag);

        const script = parentDoc.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
        script.onload = () => {
            const THREE = window.parent.THREE;
            
            const canvasContainer = parentDoc.createElement('div');
            canvasContainer.style.position = 'fixed';
            canvasContainer.style.top = '0'; canvasContainer.style.left = '0';
            canvasContainer.style.width = '100vw';
            canvasContainer.style.height = '100vh';
            canvasContainer.style.zIndex = '-1';
            canvasContainer.style.pointerEvents = 'none';
            // Ambient dark space gradient
            canvasContainer.style.background = 'radial-gradient(circle at 50% 50%, rgba(30, 20, 60, 0.7) 0%, #050506 60%)';
            parentDoc.body.appendChild(canvasContainer);

            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x050506, 0.003);
            
            const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
            camera.position.set(0, 0, 15);
            camera.lookAt(0,0,0);
            
            const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
            renderer.setPixelRatio(Math.min(window.parent.devicePixelRatio, 2));
            renderer.setSize(window.innerWidth, window.innerHeight);
            canvasContainer.appendChild(renderer.domElement);

            const starsGeo = new THREE.BufferGeometry();
            const starPos = [];
            for(let i=0; i<3000; i++) {
                starPos.push((Math.random()-0.5)*120, (Math.random()-0.5)*120, (Math.random()-0.5)*120);
            }
            starsGeo.setAttribute('position', new THREE.Float32BufferAttribute(starPos, 3));
            const starMat = new THREE.PointsMaterial({color: 0xEFE9E1, size: 0.1, transparent: true, opacity: 0.6});
            const starMesh = new THREE.Points(starsGeo, starMat);
            scene.add(starMesh);

            // 3D Wireframe Particle Globe (Earth/Network)
            const globeGeo = new THREE.IcosahedronGeometry(5.5, 4);
            const coreMat = new THREE.MeshBasicMaterial({ color: 0x050508 });
            const coreMesh = new THREE.Mesh(globeGeo, coreMat);
            scene.add(coreMesh);
            
            const wireMat = new THREE.LineBasicMaterial({ color: 0x00E5FF, transparent: true, opacity: 0.25 });
            const wireMesh = new THREE.LineSegments(new THREE.WireframeGeometry(globeGeo), wireMat);
            scene.add(wireMesh);

            const nodeMat = new THREE.PointsMaterial({ color: 0xFFFFFF, size: 0.08, transparent: true, opacity: 0.9 });
            const nodeMesh = new THREE.Points(globeGeo, nodeMat);
            scene.add(nodeMesh);

            const ringGeo1 = new THREE.RingGeometry(6.5, 6.55, 100);
            const ringMat1 = new THREE.MeshBasicMaterial({ color: 0x7C6CFF, side: THREE.DoubleSide, transparent: true, opacity: 0.6 });
            const ringMesh1 = new THREE.Mesh(ringGeo1, ringMat1);
            ringMesh1.rotation.x = Math.PI / 2;
            scene.add(ringMesh1);
            
            const ringGeo2 = new THREE.RingGeometry(7.2, 7.23, 100);
            const ringMat2 = new THREE.MeshBasicMaterial({ color: 0x00E5FF, side: THREE.DoubleSide, transparent: true, opacity: 0.4 });
            const ringMesh2 = new THREE.Mesh(ringGeo2, ringMat2);
            ringMesh2.rotation.y = Math.PI / 3;
            ringMesh2.rotation.x = Math.PI / 4;
            scene.add(ringMesh2);

            const warpGeo = new THREE.BufferGeometry();
            const warpPos = [];
            for(let i=0; i<600; i++) {
                warpPos.push((Math.random()-0.5)*40, (Math.random()-0.5)*40, (Math.random()-0.5)*100);
            }
            warpGeo.setAttribute('position', new THREE.Float32BufferAttribute(warpPos, 3));
            const warpMat = new THREE.PointsMaterial({color: 0x00E5FF, size: 0.15, transparent: true, opacity: 0.6});
            const warpMesh = new THREE.Points(warpGeo, warpMat);
            scene.add(warpMesh);

            let time = 0;
            function animate() {
                requestAnimationFrame(animate);
                time += 0.01;
                
                wireMesh.rotation.y += 0.002;
                wireMesh.rotation.x += 0.001;
                nodeMesh.rotation.y += 0.002;
                nodeMesh.rotation.x += 0.001;
                coreMesh.rotation.y += 0.002;
                coreMesh.rotation.x += 0.001;
                
                ringMesh1.rotation.z -= 0.005;
                ringMesh2.rotation.z += 0.003;
                
                starMesh.rotation.y += 0.0005;
                
                const positions = warpMesh.geometry.attributes.position.array;
                for(let i=2; i<positions.length; i+=3) {
                    positions[i] += 0.5;
                    if(positions[i] > 20) positions[i] = -60;
                }
                warpMesh.geometry.attributes.position.needsUpdate = true;
                
                camera.position.x += (mouseX/window.innerWidth - 0.5) * 0.4;
                camera.position.y += -(mouseY/window.innerHeight - 0.5) * 0.4 - 0.01;
                camera.position.x *= 0.95; 
                camera.position.y = camera.position.y * 0.95 + 5 * 0.05;
                camera.lookAt(0,0,0);

                renderer.render(scene, camera);
            }
            
            let mouseX = window.innerWidth/2, mouseY = window.innerHeight/2;
            parentDoc.addEventListener('mousemove', e => { mouseX = e.clientX; mouseY = e.clientY; });
            animate();

            window.parent.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });
        };
        parentDoc.head.appendChild(script);

        const dot = parentDoc.createElement('div');
        
        // Solid bold white cursor dot with brand glow
        dot.style = 'position:fixed; width:8px; height:8px; background:#FFFFFF; border-radius:50%; pointer-events:none; z-index:99999; transform:translate(-50%, -50%); box-shadow: 0 0 15px #ff7a00, 0 0 30px #ff007a;';
        
        parentDoc.body.appendChild(dot);

        let mX = window.innerWidth/2, mY = window.innerHeight/2;
        parentDoc.addEventListener('mousemove', e => { mX = e.clientX; mY = e.clientY; });
        
        function renderCursor() {
            dot.style.left = mX + 'px'; dot.style.top = mY + 'px';
            requestAnimationFrame(renderCursor);
        }
        renderCursor();
    })();
    </script>
    """
    st.markdown(INJECTED_CSS, unsafe_allow_html=True)
    components.html(INJECTED_JS, height=0, width=0)

    # --- LANDING PAGE LOGIC ---
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        st.markdown("""
        <style>
        /* Hide sidebar and reset padding for home page */
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        .block-container { max-width: 100% !important; padding: 0 !important; }
        
        .hero { margin-top: 15vh; display: flex; flex-direction: column; align-items: center; text-align: center; position: relative; z-index: 10; width: 100%; }
        
        .badge {
            display: inline-block;
            padding: 8px 24px;
            border-radius: 50px;
            border: 1px solid rgba(255, 122, 0, 0.5);
            background: rgba(255, 122, 0, 0.05);
            color: #fff;
            font-size: 0.8rem;
            letter-spacing: 2px;
            margin-bottom: 1.5rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .title { 
            font-size: 11rem; 
            line-height: 0.95; 
            font-weight: 400 !important; 
            color: #fff; 
            margin-bottom: 0.5rem; 
            letter-spacing: 2px; 
            text-transform: uppercase; 
            font-family: 'Anton', 'Space Grotesk', sans-serif !important; 
            width: 100%;
        }
        
        .glow-text {
            background: linear-gradient(90deg, #ff7a00, #ff007a, #e2e2fd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
            filter: drop-shadow(0 0 25px rgba(255, 50, 100, 0.6)) drop-shadow(0 0 60px rgba(255, 0, 122, 0.4));
        }

        .subtitle { font-size: 1.5rem; line-height: 1.6; color: #ccc; margin-bottom: 2rem; max-width: 850px; font-weight: 400; text-align: center; }
        
        /* Custom start button */
        div[data-testid="stButton"] > button {
            background: linear-gradient(90deg, #ff7a00, #ff007a) !important;
            color: #fff !important;
            border-radius: 50px !important;
            padding: 16px 36px !important;
            font-size: 1rem !important;
            font-weight: 700 !important;
            letter-spacing: 3px !important;
            text-transform: uppercase !important;
            box-shadow: 0 0 20px rgba(255, 122, 0, 0.4) !important;
            animation: none !important;
            border: none !important;
        }
        div[data-testid="stButton"] > button:hover {
            background: linear-gradient(90deg, #ff9533, #ff3399) !important;
            color: #fff !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 40px rgba(255, 122, 0, 0.6) !important;
        }
        
        /* Nav button overrides */
        .nav-col div[data-testid="stButton"] > button {
            background: transparent !important;
            color: #888 !important;
            padding: 5px 10px !important;
            font-size: 0.8rem !important;
            letter-spacing: 2px !important;
            margin: 0 !important;
            box-shadow: none !important;
        }
        .nav-col div[data-testid="stButton"] > button:hover {
            background: transparent !important;
            color: #ff7a00 !important;
            transform: none !important;
            box-shadow: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Navigation Bar
        nav_cols = st.columns([2, 1, 1, 1, 1, 2])
        with nav_cols[0]:
            st.markdown("<div style='font-size: 1.4rem; font-weight: 700; color: #fff; letter-spacing: 4px; padding-left: 2rem; padding-top: 1rem;'>⚿ FOURKEYS</div>", unsafe_allow_html=True)
        with nav_cols[1]:
            st.markdown("<div class='nav-col' style='padding-top: 1rem;'>", unsafe_allow_html=True)
            if st.button("PLATFORM"): st.session_state.page = "chat"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with nav_cols[2]:
            st.markdown("<div class='nav-col' style='padding-top: 1rem;'>", unsafe_allow_html=True)
            if st.button("AGENTS"): st.session_state.page = "chat"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with nav_cols[3]:
            st.markdown("<div class='nav-col' style='padding-top: 1rem;'>", unsafe_allow_html=True)
            if st.button("EVALUATION"): st.session_state.page = "chat"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with nav_cols[4]:
            st.markdown("<div class='nav-col' style='padding-top: 1rem;'>", unsafe_allow_html=True)
            if st.button("LAUNCH LOG"): st.session_state.page = "chat"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Hero Section
        st.markdown("""
        <style>
        /* Force center alignment for the main start button container */
        div.stButton {
            display: flex;
            justify-content: center;
            margin-top: 1rem;
        }
        </style>
        <div class="hero">
            <div class="badge">FOURKEYS ORCHESTRATION</div>
            <h1 class="title">UNLOCK YOUR AI<br><span class="glow-text">SUPERPOWERS</span></h1>
            <p class="subtitle">Deploy four distinct AI agents—Domain Expert, Critical Skeptic, Curious Beginner, and Fact Verifier—to synthesize flawless solutions. Just prompt, orchestrate, and launch.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Center the button using Streamlit columns
        _, center_col, _ = st.columns([1, 1, 1])
        with center_col:
            if st.button("START DEMO ➔", key="main_start", use_container_width=True):
                st.session_state.page = "chat"
                st.rerun()
            
        return
    # --- END LANDING PAGE LOGIC ---
    
    with st.sidebar:
        # Add Logo to Sidebar for Chat Page
        st.markdown("<div style='font-size: 1.8rem; font-weight: 800; color: #fff; letter-spacing: 4px; margin-bottom: 2rem; font-family: \"Space Grotesk\", sans-serif;'>⚿ FOURKEYS</div>", unsafe_allow_html=True)
        
        if st.button("⬅️ Back to Home", key="back_btn"):
            st.session_state.page = "home"
            st.rerun()
            
        st.header("⚙️ Configuration")

        use_api = st.radio(
            "Model Source:",
            options=[True, False],
            format_func=lambda x: "Google Gemini API" if x else "Local HuggingFace Model",
            index=0
        )
        
        local_model = "Qwen/Qwen2.5-1.5B-Instruct"
        if not use_api:
            local_model = st.selectbox(
                "Select Local Model:",
                options=[
                    "Qwen/Qwen2.5-1.5B-Instruct",
                    "Qwen/Qwen2.5-3B-Instruct",
                    "microsoft/Phi-3-mini-4k-instruct",
                    "google/gemma-2b-it",
                    "google/gemma-7b-it",
                    "google/gemma-2-2b-it",
                    "meta-llama/Llama-3.2-1B-Instruct",
                    "meta-llama/Llama-3.2-3B-Instruct"
                ],
                index=0
            )

        if st.button("Initialize System", type="primary"):
            initialize_system(use_api, local_model)

        st.markdown("---")
        st.markdown("**System Status:**")
        if st.session_state.system_initialized:
            st.success("✅ Ready")
            st.info(f"Using: {st.session_state.get('current_model', 'API' if st.session_state.use_api else 'Local')}")
        else:
            st.warning("⚠️ Not initialized")

        st.markdown("---")
        st.markdown("**About:**")
        st.markdown("""
        This system uses **4 different AI agents** with specialized roles:
        - 🎓 **Domain Expert**: Deep technical analysis
        - 🔍 **Critical Skeptic**: Questions & challenges
        - 🌱 **Curious Beginner**: Clarity checks
        - ✅ **Fact Verifier**: Validates consistency
        """)

        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("### 📜 Chat History")
            for i, item in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q: {item['problem'][:30]}...", expanded=False):
                    st.markdown(f"**Query:** {item['problem']}")
                    st.success(f"**Answer:** {item['multi_response']}")

    # Main tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Live Demo", "📊 Run Evaluation", "📈 View Results"])

    # TAB 1: Live Demo
    with tab1:
        st.header("Try it Live")

        if not st.session_state.system_initialized:
            st.warning("⚠️ Please initialize the system first (see sidebar)")
            return

        # Input options
        col1, col2 = st.columns([3, 1])

        with col1:
            input_method = st.radio(
                "Input method:",
                ["Enter your own question", "Choose from test cases"],
                horizontal=True
            )

        image_obj = None
        if input_method == "Enter your own question":
            problem = st.text_area(
                "Enter your question or problem:",
                height=100,
                placeholder="E.g., What is the treatment for bacterial pneumonia?"
            )
            uploaded_image = st.file_uploader("🖼️ Upload an image to analyze (Optional):", type=["png", "jpg", "jpeg", "webp"])
            if uploaded_image is not None:
                from PIL import Image
                image_obj = Image.open(uploaded_image)
                st.image(image_obj, width=200)
        else:
            test_ids = [tc["id"] for tc in TEST_CASES]
            selected_id = st.selectbox("Choose a test case:", test_ids)
            selected_case = next(tc for tc in TEST_CASES if tc["id"] == selected_id)

            st.markdown(f"**Domain:** {selected_case['domain']} | **Difficulty:** {selected_case['difficulty']}")
            problem = st.text_area("Problem:", value=selected_case["problem"], height=100)

            with st.expander("Show expected answer"):
                st.info(selected_case["ground_truth"])

        if st.button("🚀 Analyze", type="primary", disabled=not problem):

            # Single Agent Analysis
            st.markdown("---")
            st.subheader("1️⃣ Single Agent Response")

            with st.spinner("Analyzing..."):
                single_start = time.time()
                single_result = st.session_state.single_agent.analyze(problem, image=image_obj)
                single_time = time.time() - single_start

            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(single_result["response"])
            with col2:
                st.metric("Time", f"{single_time:.2f}s")

            # Multi-Agent Analysis
            st.markdown("---")
            st.subheader("2️⃣ Multi-Agent System")

            with st.spinner("Getting perspectives from all agents..."):
                multi_start = time.time()
                perspectives = st.session_state.multi_agent.get_perspectives(problem, parallel=True, image=image_obj)
                reconciled = st.session_state.reconciler.reconcile(perspectives)
                multi_time = time.time() - multi_start

            # Show individual perspectives
            st.markdown("#### Individual Agent Perspectives:")

            cols = st.columns(2)
            for idx, perspective in enumerate(perspectives):
                with cols[idx % 2]:
                    with st.expander(f"{perspective['role_name']} ({perspective['weight']:.0%} weight)"):
                        st.markdown(perspective["response"])
                        st.caption(f"Time: {perspective['inference_time']:.2f}s | Temp: {perspective['temperature']}")

            # Show reconciled answer
            st.markdown("---")
            st.markdown("#### 🎯 Final Reconciled Answer:")

            col1, col2 = st.columns([3, 1])
            with col1:
                st.success(reconciled["final_answer"])
            with col2:
                st.metric("Time", f"{multi_time:.2f}s")
                st.metric("Confidence", f"{reconciled['confidence']:.0%}")
                st.metric("Agreement", f"{reconciled['agreement_level']:.0%}")
            
            # Save to history
            st.session_state.chat_history.append({
                "problem": problem,
                "single_response": single_result["response"],
                "multi_response": reconciled["final_answer"],
                "confidence": reconciled['confidence']
            })

            # Analysis
            disagreements = analyze_disagreements(perspectives)

            if disagreements["has_major_disagreement"]:
                with st.expander("⚠️ Agent Disagreements Detected"):
                    for d in disagreements["disagreements"]:
                        st.markdown(f"**{d['role1']} vs {d['role2']}** (similarity: {d['similarity']:.0%})")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.caption(d["response1"])
                        with col2:
                            st.caption(d["response2"])
                        st.markdown("---")

            # Comparison
            st.markdown("---")
            st.subheader("📊 Comparison")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Single Agent Time", f"{single_time:.2f}s")
            with col2:
                st.metric("Multi-Agent Time", f"{multi_time:.2f}s",
                         f"+{multi_time - single_time:.2f}s")
            with col3:
                st.metric("Speedup Factor", f"{multi_time/single_time:.1f}x")

    # TAB 2: Run Evaluation
    with tab2:
        st.header("Run Full Evaluation")

        if not st.session_state.system_initialized:
            st.warning("⚠️ Please initialize the system first (see sidebar)")
            return

        st.markdown("""
        This will run the multi-agent system on all test cases and compare performance
        against a single-agent baseline.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📝 Total test cases: {len(TEST_CASES)}")
        with col2:
            st.info(f"🏷️ Domains: {', '.join(get_all_domains())}")

        if st.button("▶️ Run Evaluation", type="primary"):
            from evaluation import Evaluator

            progress_bar = st.progress(0)
            status_text = st.empty()

            evaluator = Evaluator(use_api=st.session_state.use_api)

            results = []
            for idx, test_case in enumerate(TEST_CASES):
                status_text.text(f"Running test {idx+1}/{len(TEST_CASES)}: {test_case['id']}")
                progress_bar.progress((idx + 1) / len(TEST_CASES))

                try:
                    result = evaluator.run_single_test(test_case)
                    results.append(result)
                except Exception as e:
                    st.error(f"Error on {test_case['id']}: {e}")

            # Calculate stats
            stats = evaluator.calculate_statistics(results)

            # Save to session
            st.session_state.evaluation_results = {
                "results": results,
                "statistics": stats
            }

            status_text.success("✅ Evaluation complete!")

            # Show summary
            st.markdown("---")
            st.subheader("📊 Results Summary")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Single Agent Avg", f"{stats['overall']['single_agent_avg']:.3f}")
            with col2:
                st.metric("Multi-Agent Avg", f"{stats['overall']['multi_agent_avg']:.3f}")
            with col3:
                improvement = stats['overall']['avg_improvement']
                st.metric("Improvement", f"{improvement:+.3f}",
                         f"{stats['overall']['improvement_percentage']:.1f}%")
            with col4:
                st.metric("Multi-Agent Wins",
                         f"{stats['overall']['multi_agent_wins']}/{len(results)}")

            # Generate visualizations
            st.markdown("---")
            evaluator.generate_visualizations(st.session_state.evaluation_results, output_dir="./results")
            evaluator.save_results(st.session_state.evaluation_results)

            st.success("📁 Results saved to ./results/")

    # TAB 3: View Results
    with tab3:
        st.header("View Previous Results")

        if 'evaluation_results' in st.session_state:
            results = st.session_state.evaluation_results
            stats = results["statistics"]

            # Overall metrics
            st.subheader("Overall Performance")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tests Run", stats['overall']['total_tests'])
            with col2:
                st.metric("Multi-Agent Wins", stats['overall']['multi_agent_wins'])
            with col3:
                st.metric("Avg Improvement",
                         f"{stats['overall']['improvement_percentage']:.1f}%")

            # Domain breakdown
            st.markdown("---")
            st.subheader("Performance by Domain")

            domain_data = []
            for domain, dstats in stats['by_domain'].items():
                domain_data.append({
                    "Domain": domain,
                    "Single Agent": f"{dstats['single_avg']:.3f}",
                    "Multi-Agent": f"{dstats['multi_avg']:.3f}",
                    "Improvement": f"{dstats['improvement']:+.3f}",
                    "Tests": dstats['count']
                })

            st.table(domain_data)

            # Show images if they exist
            st.markdown("---")
            st.subheader("Visualizations")

            try:
                col1, col2 = st.columns(2)
                with col1:
                    st.image("./results/overall_comparison.png", caption="Overall Comparison")
                with col2:
                    st.image("./results/win_rate.png", caption="Win Rate")

                st.image("./results/domain_comparison.png", caption="Domain-wise Performance")
                st.image("./results/improvement_distribution.png", caption="Improvement Distribution")
            except:
                st.info("Run evaluation first to generate visualizations")

        else:
            st.info("No evaluation results yet. Run evaluation in the previous tab.")

if __name__ == "__main__":
    main()
