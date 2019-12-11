from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as cipher_PKCS1_v1_5
from Crypto.Signature import PKCS1_v1_5 as signature_PKCS1_v1_5
import base64


def get_key():
    rsa = RSA.generate(1024, Random.new().read)
    private_pem = rsa.exportKey()
    public_pem = rsa.publickey().exportKey()
    return {
        "public_key": public_pem.decode(),
        "private_key": private_pem.decode()
    }

# 公钥加密
def rsa_encode(message, public_key):
    rsakey = RSA.importKey(public_key)
    cipher = cipher_PKCS1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(
        cipher.encrypt(message.encode(encoding="utf-8"))
    )
    return cipher_text.decode()

# 私钥解密
def rsa_decode(cipher_text, private_key):
    rsakey = RSA.importKey(private_key)
    cipher = cipher_PKCS1_v1_5.new(rsakey)
    text = cipher.decrypt(base64.b64decode(cipher_text), "ERROR")
    if text == "ERROR":
        return text
    return text.decode()


def rsa_sinature_encode(message, private_key):
    rsakey = RSA.importKey(private_key)
    signer = signature_PKCS1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(message.encode("utf8"))
    sign = signer.sign(digest)
    signature = base64.b64encode(sign)
    return signature


def rsa_signature_decode(message, public_key, signature):
    rsakey = RSA.importKey(public_key)
    signer = signature_PKCS1_v1_5.new(rsakey)
    digest = SHA.new()
    digest.update(message.encode("utf8"))
    is_verify = signer.verify(digest, base64.b64decode(signature))
    return is_verify


# if __name__ == '__main__':
#     keys = get_key()
#     public_key = keys["public_key"]
#     private_key = keys["private_key"]
#     # 加密解密
#     message = "hello world!"
#     encode_msg = rsa_encode(message, public_key)
#     print("encode_msg ==== ", encode_msg)
#     message = rsa_decode(encode_msg, private_key)
#     print("message ==== ", message)
#     # 签名验证
#     message = "it's me"
#     signature = rsa_sinature_encode(message, private_key)
#     print("signature ==== ", signature)
#     verify = rsa_signature_decode(message, public_key, signature)
#     print("verify ==== ", verify)
