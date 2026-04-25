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

# Custom CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp {
        background: #0d0d0d;
        color: #ffffff;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stAppHeader {display: none;}

    /* Loading Spinner */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 0;
        gap: 1.5rem;
    }

    .spinner-ring {
        width: 48px;
        height: 48px;
        border: 3px solid rgba(255,255,255,0.1);
        border-top-color: #ffffff;
        border-radius: 50%;
        animation: spin 1.2s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .loading-text {
        color: #a1a1a1;
        font-size: 0.95rem;
        font-weight: 400;
        letter-spacing: 0.02em;
    }

    /* Success State */
    .success-ring {
        width: 48px;
        height: 48px;
        border: 3px solid #22c55e;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: success-pop 0.3s ease-out forwards;
    }

    @keyframes success-pop {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    .checkmark {
        width: 20px;
        height: 20px;
        stroke: #22c55e;
        stroke-width: 3;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
        stroke-dasharray: 24;
        stroke-dashoffset: 24;
        animation: checkmark-draw 0.3s ease-out 0.1s forwards;
    }

    @keyframes checkmark-draw {
        to { stroke-dashoffset: 0; }
    }

    /* Certificate Card */
    .certificate-card {
        background: #171717;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        animation: fade-in-up 0.4s ease-out 0.2s both;
    }

    @keyframes fade-in-up {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .certificate-output {
        background: rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        padding: 1rem;
        color: #22c55e;
        font-family: 'Inter', monospace;
        font-size: 0.85rem;
        word-break: break-all;
        margin: 1rem 0;
    }

    /* Info & Details boxes */
    .info-box {
        background: rgba(255,255,255,0.05);
        border-left: 3px solid #ffffff;
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 2rem;
        font-size: 0.9rem;
        color: #a1a1a1;
    }

    .details-box {
        background: #171717;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1rem 0;
        font-size: 0.85rem;
        color: #a1a1a1;
        line-height: 1.6;
    }

    .details-box code {
        background: rgba(0,0,0,0.3);
        padding: 0.15rem 0.4rem;
        border-radius: 4px;
        font-family: 'Inter', monospace;
        color: #ffffff;
    }

    /* Section header */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #ffffff;
        margin: 2rem 0 1rem;
        border-left: 3px solid #ffffff;
        padding-left: 0.75rem;
    }

    /* Success/Error boxes */
    .success-box {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid #22c55e;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        color: #ffffff;
        font-weight: 500;
        margin: 1rem 0;
    }

    .error-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        color: #ffffff;
        font-weight: 500;
        margin: 1rem 0;
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background: #171717;
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 8px;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        padding: 0.6rem 0.75rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: #ffffff;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.1);
    }

    .stTextInput > div > div > input::placeholder {
        color: #555555;
    }

    /* Button */
    .stButton > button {
        background: #ffffff;
        color: #0d0d0d;
        border: none;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 600;
        padding: 0.7rem 1.5rem;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #e5e5e5;
        transform: translateY(-1px);
    }

    /* Links */
    a { color: #ffffff; }
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
    separator = "N "
    
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
    
    encrypted_b64 = base64.b64encode(encrypted).decode('utf-8').strip()
    
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

def render_loading_spinner():
    """Render the custom minimalista loading spinner"""
    st.markdown("""
    <div class="loading-container">
        <div class="spinner-ring"></div>
        <div class="loading-text">Gerando certificado...</div>
    </div>
    """, unsafe_allow_html=True)


def render_success_checkmark():
    """Render success state with checkmark animation"""
    st.markdown("""
    <div class="loading-container">
        <div class="success-ring">
            <svg class="checkmark" viewBox="0 0 24 24">
                <polyline points="4,12 10,18 20,6"></polyline>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)


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
            render_loading_spinner()
            import time
            time.sleep(1.5)
            result = generate_certificate(mac1, mac2, board_type, 16, 16)
            
            if result['success']:
                info = result['certificate_info']

                # Show success checkmark first
                render_success_checkmark()
                st.markdown('<div class="loading-container" style="padding-top:0;padding-bottom:1rem;"><div class="loading-text" style="color:#22c55e;">Certificado gerado!</div></div>', unsafe_allow_html=True)

                # Certificate output
                st.markdown("### Generated Certificate")
                certificate_text = result['encrypted_certificate']
                
                st.markdown(f"""
                <div class="certificate-output">
                    {certificate_text}
                </div>
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
