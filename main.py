import pymysql
import base64
import hashlib
from Crypto.Cipher import AES

connect = pymysql.connect(host='127.0.0.1', user='root', password='12341234', db='Project_info')
cursor = connect.cursor()

key = "input_key"
data = "input_data"

BS = 16
pad = (lambda s: s+ (BS - len(s) % BS) * chr(BS - len(s) % BS).encode())
unpad = (lambda s: s[:-ord(s[len(s)-1:])])

class AESCipher(object):
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()
        print("AES Key", key)
        print("AES Key 암호화 결과:", self.key)

    def encrypt(self, message):
        message = message.encode()
        raw = pad(message)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf8'))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')

    def __iv(self):
        return chr(0) * 16

aes = AESCipher(key)
encrypt = aes.encrypt(data)

print("암호화 전 데이터:", data)
print("암호화 후 데이터:", encrypt)


cursor.execute("SELECT * FROM users")


connect.commit()
connect.close()





# hostI = input("데이터베이스 호스트를 입력해주세요. : ")
# userI = input("아이디를 입력해주세요. : ")
# passwordI = input("비밀번호를 입력해주세요. : ")
#

# connect = pymysql.connect(host=hostI, user=userI, password=passwordI, db='Project_info')