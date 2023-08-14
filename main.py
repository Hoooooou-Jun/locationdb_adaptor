import pymysql
import base64
import hashlib
from Crypto.Cipher import AES

hostI = input("데이터베이스 호스트를 입력해주세요. : ")
userI = input("아이디를 입력해주세요. : ")
passwordI = input("비밀번호를 입력해주세요. : ")
schemaI = input("접근할 스키마를 입력해주세요. : ")

connect = pymysql.connect(host=hostI, user=userI, password=passwordI, db=schemaI)
cursor = connect.cursor()

key = 'easternsky'

BS = 16
pad = (lambda s: s+ (BS - len(s) % BS) * chr(BS - len(s) % BS).encode())
unpad = (lambda s: s[:-ord(s[len(s)-1:])])

class AESCipher(object):
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, message):
        message = message.encode()
        raw = pad(message)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf8'))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')

    def __iv(self):
        return chr(0) * 16

aes = AESCipher(key)

def locationEncrypt(rows):
    for  row in rows:
        if row[1] == "0" or row[2] == "0":
            print(f'id {row[0]} 데이터 위도 및 경도 없음')
            continue
        encrypted_lat, encrypted_lon = aes.encrypt(row[1]), aes.encrypt(row[2])
        cursor.execute(update_query, (encrypted_lat, encrypted_lon, row[0]))
        connect.commit()
        print(f'id {row[0]} 데이터 암호화 완료')

selectI = int(input("모든 테이블 대상의 암호화는 0, 하나의 테이블 대상의 암호화는 1을 입력해주세요. : "))

if selectI:
    tableI = input("암호화할 대상 테이블을 입력해주세요. : ")

    select_query = f"SELECT id, longitude, latitude FROM {tableI}"
    update_query = f"UPDATE {tableI} SET latitude = %s, longitude = %s WHERE id = %s"
    cursor.execute(select_query)

    rows = cursor.fetchall()
    locationEncrypt(rows)
else:
    show_query = 'SHOW TABLES'
    cursor.execute(show_query)
    tables = cursor.fetchall()

    for table in tables:
        try:
            select_query = f"SELECT id, longitude, latitude FROM {table[0]}"
            update_query = f"UPDATE {table[0]} SET latitude = %s, longitude = %s WHERE id = %s"

            cursor.execute(select_query)
            rows = cursor.fetchall()

            print(f"{table[0]} 테이블 대상 위치 정보 암호화 진행")
            locationEncrypt(rows)
            print(f"{table[0]} 테이블 대상 암호화 완료")
        except:
            print(f"{table[0]} 테이블은 위치 정보가 없습니다.")
            continue

connect.commit()
connect.close()

print("프로그램이 종료됩니다.")