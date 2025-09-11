import streamlit as st
import base64
import secrets
import string
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# Page configuration
st.set_page_config(
    page_title="ZTE ID 2561 Generator",
    page_icon="🔑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS styling inspired by the HTML design
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        color: #f5f5f5;
        font-family: 'Courier Prime', 'Courier New', monospace;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stAppHeader {display: none;}
    
    /* Main header */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
    }
    
    .logo {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #ffffff;
        text-shadow: 0 0 20px #ffffff;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px #ffffff; }
        to { text-shadow: 0 0 30px #aaaaaa, 0 0 40px #ffffff; }
    }
    
    .tagline {
        font-size: 1.1rem;
        color: #aaaaaa;
        margin-bottom: 1rem;
    }
    
    /* Tool cards */
    .tool-card {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 2rem;
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .tool-card:hover {
        background: rgba(255,255,255,0.1);
        border-color: #ffffff;
        box-shadow: 0 0 20px rgba(255,255,255,0.3);
        transform: translateY(-2px);
    }
    
    .tool-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .tool-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #ffffff;
    }
    
    .tool-description {
        color: #cccccc;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 4px;
        color: #ffffff;
        font-family: 'Courier Prime', 'Courier New', monospace;
        font-size: 1.1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffffff;
        box-shadow: 0 0 10px rgba(255,255,255,0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #ffd700, #ffed4e);
        border: 2px solid #ffd700;
        border-radius: 8px;
        color: #000000;
        font-family: 'Courier Prime', 'Courier New', monospace;
        font-size: 1rem;
        font-weight: 700;
        padding: 0.8rem 2rem;
        text-transform: uppercase;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #ffed4e, #fff700);
        box-shadow: 0 0 15px rgba(255,215,0,0.5);
        transform: translateY(-1px);
    }

    .stButton > button:active {
        background: linear-gradient(45deg, #ffed4e, #fff700);
        box-shadow: 0 0 15px rgba(255,215,0,0.5);
        transform: translateY(-1px);
    }
    
    /* Success/Error messages */
    .success-box {
        background: rgba(76, 175, 80, 0.1);
        border: 1px solid #4caf50;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ffffff;
    }
    
    .error-box {
        background: rgba(244, 67, 54, 0.1);
        border: 1px solid #f44336;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ffffff;
    }
    
    /* Certificate output */
    .certificate-output {
        background: rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.3);
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        color: #32cd32;
        font-family: 'Courier Prime', 'Courier New', monospace;
        font-size: 0.9rem;
        word-break: break-all;
        position: relative;
    }
    
    /* Section styling */
    .section-header {
        font-size: 1.5rem;
        color: #ffffff;
        margin-bottom: 1.5rem;
        border-left: 4px solid #ffffff;
        padding-left: 1rem;
    }
    
    /* Info box */
    .info-box {
        background: rgba(255,255,255,0.1);
        border-left: 4px solid #ffffff;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border-radius: 0 8px 8px 0;
        backdrop-filter: blur(10px);
        text-align: center;
    }
    
    /* Details styling */
    .details-box {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #cccccc;
    }
    
    /* Override Streamlit's default dark theme for better contrast */
    .stSelectbox > div > div {
        background: rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.3);
        color: #ffffff;
        font-family: 'Courier Prime', 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Certificate generation functions (from original script)
def generate_random_string(length):
    """Generate random string for prefix/suffix"""
    return ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def format_mac_address(mac_input):
    mac_clean = mac_input.replace(":", "").replace("-", "")
    mac_formatted = mac_clean.upper()
    
    if len(mac_formatted) != 12:
        raise ValueError(f"Invalid MAC address: {mac_input}. Must have 12 hex characters.")
    
    try:
        int(mac_formatted, 16)
    except ValueError:
        raise ValueError(f"MAC address contains invalid characters: {mac_input}")
    
    return mac_formatted

def create_certificate_payload(mac1, mac2, board_type, prefix_length=16, suffix_length=16):
    mac1_formatted = format_mac_address(mac1)
    mac2_formatted = format_mac_address(mac2)
    
    # Validate board type
    board_type = board_type.upper().strip()
    if len(board_type) > 20:
        raise ValueError(f"Board type too long: {board_type} (maximum 20 chars)")
    
    # Generate random prefix and suffix
    prefix = generate_random_string(prefix_length)
    suffix = generate_random_string(suffix_length)
    # Fix: Removed the trailing space from the separator
    separator = "N"
    
    certificate_data = mac1_formatted + mac2_formatted + separator + board_type
    
    # Add prefix and suffix
    full_certificate = prefix + certificate_data + suffix
    
    return {
        'payload': full_certificate,
        'mac1_formatted': mac1_formatted,
        'mac2_formatted': mac2_formatted,
        'board_type': board_type,
        'prefix': prefix,
        'suffix': suffix,
        'data_section': certificate_data
    }

def encrypt_certificate(payload, public_key_pem=None):
    """Encrypt the certificate using RSA"""
    # Default ZTE public key
    default_public_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDO+5w8SZFD6opwK4tWOeH7f+yT
RKy6dXvmRtUwiIjrgb/Djnl85S0/kSYgpgQpolSGjbijiyBDj41aSFGrOEz7z3wO
K4pRByHk0+O82vf7y7qceJAIX0OocSluks4oBgnwVFyo4Qis9xwwssqC1aubsQYy
xKNa0c/WodUSouWK0wIDAQAB
-----END PUBLIC KEY-----"""
    
    # Use provided key or default
    key_pem = public_key_pem or default_public_key
    
    # Load public key
    public_key = serialization.load_pem_public_key(key_pem.encode())
    
    # Encrypt payload
    payload_bytes = payload.encode('utf-8')
    
    encrypted = public_key.encrypt(
        payload_bytes,
        padding.PKCS1v15()
    )
    
    encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
    
    return encrypted_b64

def generate_certificate(mac1, mac2, board_type, prefix_length=16, suffix_length=16):
    try:
        # Create payload
        cert_info = create_certificate_payload(mac1, mac2, board_type, prefix_length, suffix_length)
        
        # Encrypt
        encrypted_cert = encrypt_certificate(cert_info['payload'])
        
        return {
            'encrypted_certificate': encrypted_cert,
            'certificate_info': cert_info,
            'success': True
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'success': False
        }

# Main application
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="logo">ZTE ID 2561 Generator</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Info section
    st.markdown("""
    <div class="info-box">
        <strong>ZTE Certificate Generator</strong> - Generate Certificate ID 2561 for fixing 10-minute reboot after Anti_Infringement_judge function is triggered.<br/>
        <strong>GitHub:</strong> <a href="https://github.com/ldamasceno38" target="_blank" style="color:#ffd700;text-decoration:none">https://github.com/ldamasceno38</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">🔑 Certificate Generator</h2>', unsafe_allow_html=True)
    
    # Input form
    st.markdown("### Device Information")
    
    mac1 = st.text_input(
        "MAC Address 1 (setmac show id 256)",
        placeholder="48:96:D9:A2:47:01",
        help="Enter the first MAC address from your device"
    )
    
    mac2 = st.text_input(
        "MAC Address 2 (setmac show id 257)",
        placeholder="48:96:D9:A2:47:02",
        help="Enter the second MAC address from your device"
    )
    
    board_type = st.text_input(
        "Board Type",
        placeholder="F6600P",
        help="Enter your device board type (e.g., F6600P, F6645P)"
    )
    
    # Generate button
    if st.button("🔐 Generate Certificate", type="primary"):
        if not mac1 or not mac2 or not board_type:
            st.markdown("""
            <div class="error-box">
                ❌ <strong>Error:</strong> Please fill in all required fields.
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.spinner("Generating certificate..."):
                result = generate_certificate(mac1, mac2, board_type, 16, 16)
            
            if result['success']:
                info = result['certificate_info']
                
                # Success message
                st.markdown("""
                <div class="success-box">
                    ✅ <strong>Certificate generated successfully!</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Certificate output with a unique ID for copy button
                st.markdown("### Generated Certificate")
                
                # Strip any potential leading/trailing whitespace
                certificate_text = result['encrypted_certificate'].strip()
                
                # Wrap the certificate in a div with an ID
                st.markdown(f"""
                <div class="certificate-output" id="certificateText">
                    {certificate_text}
                </div>
                """, unsafe_allow_html=True)
                
                # Add copy button functionality using JavaScript
                st.markdown("""
                <button 
                    onclick="navigator.clipboard.writeText(document.getElementById('certificateText').innerText.trim());"
                    style="
                        background: linear-gradient(45deg, #ffd700, #ffed4e);
                        border: 2px solid #ffd700;
                        border-radius: 8px;
                        color: #000000;
                        font-family: 'Courier Prime', 'Courier New', monospace;
                        font-size: 1rem;
                        font-weight: 700;
                        padding: 0.8rem 2rem;
                        text-transform: uppercase;
                        transition: all 0.3s ease;
                        width: 100%;
                        margin-top: 1rem;
                    "
                >
                📋 Copy to Clipboard
                </button>
                """, unsafe_allow_html=True)
        
                
                # Certificate details
                st.markdown("### Certificate Details")
                st.markdown(f"""
                <div class="details-box">
                    <strong>MAC Address 1:</strong> {info['mac1_formatted']}<br/>
                    <strong>MAC Address 2:</strong> {info['mac2_formatted']}<br/>
                    <strong>Board Type:</strong> {info['board_type']}<br/>
                    <strong>Payload Structure:</strong> [Random16]{info['data_section']}[Random16]<br/>
                    <strong>Total Payload Length:</strong> {len(info['payload'])} characters
                </div>
                """, unsafe_allow_html=True)
                
                # Installation instructions
                st.markdown("### Installation Instructions")
                st.markdown(f"""
                <div class="details-box">
                    <strong>1. Set the certificate:</strong><br/>
                    <code>setmac 1 2561 {certificate_text}</code><br/><br/>
                    <strong>2. Reboot the device:</strong><br/>
                    <code>reboot</code><br/><br/>
                    <strong>3. Verify installation (via telnet):</strong><br/>
                    <code>upgradetest devicecheck</code><br/>
                    <em>Should return SUCCESS</em>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown(f"""
                <div class="error-box">
                    ❌ <strong>Error:</strong> {result['error']}
                </div>
                """, unsafe_allow_html=True)

def show_documentation():
    st.markdown('<h2 class="section-header">📚 Documentation</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### About ZTE Certificate Generator
    
    This tool generates Certificate ID 2561 for ZTE modems to fix the 10-minute reboot issue that occurs after the Anti_Infringement_judge function is triggered.
    
    ### How it works
    
    ZTE Modems call `Anti_Infringement_judge()` to check if the certificate (base64) after RSA decryption contains in a specific order:
    
    1. **Random Prefix** (16 bytes)
    2. **MAC 1** (setmac show id 256) 
    3. **MAC 2** (setmac show id 257)
    4. **Separator** ("N ")
    5. **BoardType** (checked via DB directly)
    6. **Random Suffix** (16 bytes)
    
    ### Prerequisites
    
    Before using this tool, you need to obtain:
    - MAC Address 1: `setmac show id 256`
    - MAC Address 2: `setmac show id 257`  
    - Board Type: Your device model (e.g., F6600P, F6645P)
    
    ### Supported Models
    
    - ZTE F6600P
    - ZTE F6645P
    - Other ZTE models with similar certificate requirements
    
    ### Installation Process
    
    1. Generate the certificate using this tool
    2. Connect to your device via telnet/SSH
    3. Set the certificate: `setmac 1 2561 [generated_certificate]`
    4. Reboot the device: `reboot`
    5. Verify: `upgradetest devicecheck` (should return SUCCESS)
    
    ### Troubleshooting
    
    - **Invalid MAC address**: Ensure MAC addresses are in correct format (12 hex characters)
    - **Board type too long**: Keep board type under 20 characters
    - **Certificate not working**: Verify MAC addresses match your device exactly
    - **Verification fails**: Double-check the certificate was set correctly
    
    ### Security Note
    
    This tool uses the default ZTE public key for encryption. The generated certificates are specific to your device's MAC addresses and board type.
    """)
    
    # Technical details
    with st.expander("Technical Details"):
        st.markdown("""
        ### RSA Encryption Details
        
        - **Key Size**: 1024-bit RSA
        - **Padding**: PKCS1v15
        - **Encoding**: Base64
        
        ### Certificate Structure
        
        ```
        [Random Prefix 16 bytes][MAC1 12 chars][MAC2 12 chars][N ][Board Type][Random Suffix 16 bytes]
        ```
        
        ### Default ZTE Public Key
        
        ```
        -----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDO+5w8SZFD6opwK4tWOeH7f+yT
        RKy6dXvmRtUwiIjrgb/Djnl85S0/kSYgpgQpolSGjbijiyBDj41aSFGrOEz7z3wO
        K4pRByHk0+O82vf7y7qceJAIX0OocSluks4oBgnwVFyo4Qis9xwwssqC1aubsQYy
        xKNa0c/WodUSouWK0wIDAQAB
        -----END PUBLIC KEY-----
        ```
        """)

if __name__ == "__main__":
    main()
