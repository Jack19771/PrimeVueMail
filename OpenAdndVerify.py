from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

# Funkcja do odszyfrowania wiadomości
def decrypt_message(encrypted_message_base64, private_key_path):
    # Dekodowanie Base64 (zakładając, że plik .txt zawiera zaszyfrowaną wiadomość w Base64)
    encrypted_message = base64.b64decode(encrypted_message_base64)
    
    # Wczytanie klucza prywatnego
    with open(private_key_path, 'rb') as priv_file:
        private_key = RSA.import_key(priv_file.read())
    
    # Odszyfrowanie wiadomości
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_message = cipher_rsa.decrypt(encrypted_message)
    
    return decrypted_message.decode('utf-8')

# Funkcja do weryfikacji podpisu
def verify_signature(message, signature_base64, public_key_path):
    # Dekodowanie Base64 podpisu
    signature = base64.b64decode(signature_base64)

    # Wczytanie klucza publicznego
    with open(public_key_path, 'rb') as pub_file:
        public_key = RSA.import_key(pub_file.read())

    # Obliczanie hasha wiadomości
    h = SHA256.new(message.encode('utf-8'))

    # Weryfikacja podpisu
    verifier = pkcs1_15.new(public_key)
    try:
        verifier.verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

# Funkcja główna do wczytania plików, odszyfrowania wiadomości i weryfikacji podpisu
def process_encrypted_email(encrypted_filename, signature_filename, private_key_path, public_key_path):
    try:
        # Wczytanie zaszyfrowanej wiadomości z pliku .txt (w formacie Base64)
        with open(encrypted_filename, 'r') as enc_file:
            encrypted_message_base64 = enc_file.read().strip()

        # Wczytanie podpisu z pliku .sig (w Base64)
        with open(signature_filename, 'r') as sig_file:
            signature_base64 = sig_file.read().strip()

        # Odszyfrowanie wiadomości
        decrypted_message = decrypt_message(encrypted_message_base64, private_key_path)
        print("Odszyfrowana wiadomość:")
        print(decrypted_message)

        # Weryfikacja podpisu
        if verify_signature(decrypted_message, signature_base64, public_key_path):
            print("Podpis jest prawidłowy!")
        else:
            print("Podpis jest nieprawidłowy!")
    except Exception as e:
        print(f"Błąd: {e}")

# Przykładowe ścieżki plików
encrypted_filename = r'messages\encrypted_siema_marzenmka.txt'  # Plik .txt z zaszyfrowaną wiadomością
signature_filename = r'messages\signed_siema_marzenmka.sig'   # Plik .sig z podpisem
private_key_path = r'keys/private_key.pem'  # Ścieżka do klucza prywatnego
public_key_path = r'keys/public_key.pem'   # Ścieżka do klucza publicznego

# Procesowanie plików
process_encrypted_email(encrypted_filename, signature_filename, private_key_path, public_key_path)
