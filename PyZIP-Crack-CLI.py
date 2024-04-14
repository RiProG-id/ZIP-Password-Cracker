import itertools
import zipfile
import signal
import sys
import threading
import os

stop_event = threading.Event()

def signal_handler(sig, frame):
    global stop_event
    print('\nExited')
    stop_event.set()
    sys.exit()

def extract_zip(zip_file, start_length, max_length, charset):
    filler = " " * (max_length // 2)

    passwords = (''.join(password) for length in range(start_length, max_length+1) for password in itertools.product(charset, repeat=length))

    print("\nStarting brute-force attack...")

    for i, password in enumerate(passwords, start=1):
        if len(password) > max_length:
            break
        
        if stop_event.is_set():
            return None
        
        progress = f"Trying password: {password} (on iteration: {i} of cycle: {len(password)})"
        print("\r" + progress, end="", flush=True)

        try:
            zip_file.extractall(pwd=password.encode())
            print('\n\nPassword found:', password)
            print('Total attempts:', i)
            return password
        except:
            global count
            count = i
            pass

    print('\n\nPassword not found.')
    print('Total attempts:', count)
    return None


if __name__ == '__main__':
    lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
    uppercase_letters = lowercase_letters.upper()
    digits = '0123456789'
    special_chars = r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

    all_chars = lowercase_letters + uppercase_letters + digits + special_chars
    
    zip_file_path = input("Enter the path to the ZIP file: ")

    if not os.path.exists(zip_file_path):
        print("The specified ZIP file does not exist.")
        sys.exit()

    print("Choose a method:")
    print("1. Lowercase letters")
    print("2. Uppercase letters")
    print("3. Lowercase and Uppercase letters")
    print("4. Digits")
    print("5. Special characters")
    print("6. Lowercase, Uppercase, and Digits")
    print("7. All possible combinations")

    method_choice = input("Enter your choice (1/2/3/4/5/6/7): ")

    charsets = []

    if method_choice == "1":
        charsets.append(lowercase_letters)
    elif method_choice == "2":
        charsets.append(uppercase_letters)
    elif method_choice == "3":
        charsets.append(lowercase_letters + uppercase_letters)
    elif method_choice == "4":
        charsets.append(digits)
    elif method_choice == "5":
        charsets.append(special_chars)
    elif method_choice == "6":
        charsets.append(lowercase_letters + uppercase_letters + digits)
    elif method_choice == "7":
        charsets = [all_chars]
    else:
        print("Invalid choice.")
        sys.exit()

    min_length = int(input("Enter the minimum length of the password to try: "))
    max_length = int(input("Enter the maximum length of the password to try: "))

    try:
        zip_file = zipfile.ZipFile(zip_file_path)
    except Exception as e:
        print('Failed to open ZIP file: ' + str(e))
        sys.exit()

    for charset in charsets:
        password = extract_zip(zip_file, min_length, max_length, ''.join(charset))
        if password:
            break
