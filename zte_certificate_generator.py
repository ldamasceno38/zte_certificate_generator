# My gift to the community.
#
# https://github.com/ldamasceno38/zte_certificate_generator
#
# Generates Certificate ID 2561 for Fixing 10-minute-reboot after Anti_Infringement_judge function is triggered.
#
# Anti_Infringement_judge() if the certificate (base64) after RSA decryption CONTAINS:
#  - MAC 1 (setmac show id 256)
#  - MAC 2 (setmac show id 257)
#  - BoardType (not setmac, this is checked via DB directly)
#
#  You can check if your certificate is valid via telnet:
#             upgradetest devicecheck
#  This should returns a SUCCESS message.

import base64
import secrets
import string
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

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

def create_certificate_payload(mac1, mac2, board_type, 
                             prefix_length=16, suffix_length=16):

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
    """
    Encrypt the certificate using RSA
    """
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
        cert_info = create_certificate_payload(mac1, mac2, board_type, 
                                             prefix_length, suffix_length)
        
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

def main():
    """Main interactive function"""
    print("=== ANTI-INFRINGEMENT CERTIFICATE GENERATOR ===")
    print()
    
    # Request inputs
    print("Enter device data:")
    mac1 = input("MAC Address 1 (ex: 48:96:D9:A2:47:01): ").strip()
    mac2 = input("MAC Address 2 (ex: 48:96:D9:A2:47:02): ").strip()
    board_type = input("Board Type (ex: F6600P): ").strip()
    
    print("\nGenerating certificate...")
    
    # Generate certificate
    result = generate_certificate(mac1, mac2, board_type)
    
    if result['success']:
        info = result['certificate_info']
        
        print("\n=== CERTIFICATE GENERATED SUCCESSFULLY ===")
        print(f"\033[92m{result['encrypted_certificate']}\033[0m")
        print()
       
    else:
        print(f"\n❌ Error: {result['error']}")

if __name__ == "__main__":
    main()
