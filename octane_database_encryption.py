from cryptography.fernet import Fernet


# function that generates new key
def generate_filekey():
    key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)

# uncomment the line below to generate new key
# generate_filekey()


# read key from file
with open('filekey.key', 'rb') as filekey:
    key = filekey.read()
fernet = Fernet(key)

# update the variables to generate new encrypted database network connection
db_username = ""
db_password = ""
db_network_alias = ""

# concatenate and print database network connection
db_network_connection = db_username + "/" + db_password + "@" + db_network_alias
print("Database Network Connection:\n" + db_network_connection)

# encrypt and print encrypted database network connection
encrypted_db_network_connection = fernet.encrypt(db_network_connection.encode('utf-8')).decode()
print("\nEncrypted Database Network Connection:\n" + encrypted_db_network_connection + "\n(Copy the string above)")
