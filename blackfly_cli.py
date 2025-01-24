from cryptography.fernet import Fernet
import cryptography
import os , json, random, string, pyfiglet, requests, time, base64

# 1. Generate or load the encryption key
def retrieve_key(file_path='key.key'):
    print('Scanning for key file..')
    if not os.path.exists(file_path):
        print('Key file not found!\nDo you have a key?(yes/no)')
        option = input('> ')
        if option == 'yes':
            key = input('Enter your key:').encode()
            try:
                fernet = Fernet(key)
                return key
            except ValueError as e:
                print('Key error.\nThe key you provided in incorrect.\nExiting...')
                exit() 
        else:
            print('Generating a new key for you..')
            key = Fernet.generate_key()
        with open(file_path, 'wb') as key_file:
            key_file.write(key)
        print(f"New key generated\nEncryption key:{key.decode()}\nEncryption key saved to {file_path}")
        print('\nFor hardended Security, you can save the key somewhere safe & delete the generated key file.\nYou can enter your key every time this script is run, to access all your secure passwords.')
        time.sleep(2)
        return key
    else:
        print(f"Encryption key found at {file_path}")
        with open(file_path, 'rb') as key_file:
            return key_file.read()


# 2. Encrypt a password
def encrypt_password(password, key):
    try:
        fernet = Fernet(key)
        encrypted_password = fernet.encrypt(password.encode())
    except ValueError as e:
        print('Key error.\nThe key you provided in incorrect.\nExiting...')
        exit()    
    return encrypted_password

# 3. Decrypt a password
def decrypt_password(encrypted_password, key):
    try:
        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(encrypted_password).decode()
    except ValueError as e:
        print('Key error.\nThe key you provided in incorrect.\nExiting...')
        exit()      
    return decrypted_password

# generate welcome
def welcome():
    print(pyfiglet.figlet_format("Blackfly", font="slant"))

# generate password
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(16))
    return password

# generating new identity
def new_identity():
    response = requests.get('https://randomuser.me/api/')
    if response.status_code == 200:
        info = json.loads(response.text)['results'][0]

    data = f"""\t\t\tMy Identity
    First Name: {info['name']['first']}
    Last Name: {info['name']['last']}
    Gender: {info['gender']}

    Address: {info['location']['street']['number']} {info['location']['street']['name']}
    City: {info['location']['city']}
    State: {info['location']['state']}
    Country: {info['location']['country']}
    Post Code: {info['location']['postcode']}

    Date of Birth: {info['dob']['date']}
    Age: {info['dob']['age']}

    Nationality: {info['nat']}"""
    with open('Identity.txt','w') as file:
        file.write(data)
    print(data)

if __name__ == "__main__":
    # Generate or load the encryption key
    welcome()
    key = retrieve_key()
    # print(key)
    while True:
        option = int(input('\nChoose from the options below: (enter only index numbers)\n1.Generate pasword for new account\n2.View saved passwords\n3.Generate new identity\n4.Exit\n>'))
        if option == 1:
            platform = input("Platform:").strip()
            account_name = input("Username:").strip()
            password = generate_password()
            encoded_password = base64.b64encode(encrypt_password(password,key)).decode('utf-8')
            try:
                with open('Data.json','r') as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                data = {}

            data[platform+"-"+account_name] = [platform,account_name,encoded_password]
            # print(data)
            with open('Data.json','w') as file:
                json.dump(data,file)
            print(f'Password: {password}\nPassword encrypted & saved.')
        elif option == 2:
            print('Fetching Your stored passwords..')
            try:
                with open('Data.json','r') as file:
                    data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print('No Saved passwords found!')
                continue
            print('\t\tYour Stored Accounts are:')
            for id,val in data.items():
                print(f'ID:{id}\nPlatform:{val[0]}\nUsername:{val[1]}',end='\n')
            select = input('\nenter the ID to select an account > ').strip()
            try:
                account = data[select]
                print('Decrypting your password..\n')
                decrypted_password = decrypt_password(base64.b64decode(account[-1]),key)
                print(f'Account Credentials\nUsername:{account[1]}\nPlatform:{account[0]}\nPassword:{decrypted_password}')
            except KeyError as e:
                print('Invalid key')
                continue
        elif option  == 3:
            print('Generating new identity for you..')
            new_identity()
            print('Identity saved to file : Identity.txt')
        elif option == 4:
            print('Exiting..')
            break
        else:
            print('Invalid Selection..\n')
            continue
