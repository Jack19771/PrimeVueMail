from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Funkcja do odszyfrowania wiadomości
def decrypt_message(encrypted_message_base64, private_key_path):
    # Dekodowanie Base64
    encrypted_message = base64.b64decode(encrypted_message_base64)
    
    # Wczytanie klucza prywatnego
    with open(private_key_path, 'rb') as priv_file:
        private_key = RSA.import_key(priv_file.read())
    
    # Odszyfrowanie wiadomości
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher_rsa.decrypt(encrypted_message)
    
    return decrypted_message.decode('utf-8')

# Wczytanie zaszyfrowanej wiadomości z pliku .txt
with open('messages\encrypted_Jacek_Jacek.txt', 'r') as enc_file:
    encrypted_message_base64 = enc_file.read()

# Ścieżka do pliku z kluczem prywatnym
private_key_path = 'keys/private_key.pem'

# Odszyfrowanie wiadomości
try:
    decrypted_message = decrypt_message(encrypted_message_base64, private_key_path)
    print("Odszyfrowana wiadomość:")
    print(decrypted_message)
except Exception as e:
    print(f"Błąd podczas odszyfrowywania wiadomości: {e}")
