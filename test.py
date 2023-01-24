import hashlib
pwd2=input()
pwd2=hashlib.sha256(pwd2.encode('utf-8')).hexdigest()
print(pwd2)