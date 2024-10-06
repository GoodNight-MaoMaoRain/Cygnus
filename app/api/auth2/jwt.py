from datetime import datetime, timedelta
from typing import Dict
import jwt
import bcrypt
from fastapi import HTTPException,Request
from jose import JWTError
from passlib.context import CryptContext
from starlette import status

from app.core.settings.ini import CygnusConfig
from app.schemas.schemas_jwt import JWTMeta, JWTUser

jwt_al, jwt_exp, jwt_subject = CygnusConfig.get_auth_cfg()


class UserJwt:

    @staticmethod
    def create_jwt_token(
            *,
            jwt_content: Dict[str, str],
            secret_key: str,
            expires_delta: timedelta,
    ) -> str:
        to_encode = jwt_content.copy()
        expire = datetime.now() + expires_delta
        to_encode.update(JWTMeta(exp=expire, sub=jwt_subject).model_dump())
        return jwt.encode(to_encode, secret_key, algorithm=jwt_al)

    def create_access_token_for_user(self, user_id: int, user_name: str, secret_key: str) -> str:
        return self.create_jwt_token(
            jwt_content=JWTUser(user_name=user_name, user_id=user_id).model_dump(),
            secret_key=secret_key,
            expires_delta=timedelta(minutes=jwt_exp),
        )

    # 验证 token 的函数
    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, jwt_subject, jwt_al)
            # 从 payload 中提取用户信息
            user_id = payload.get("user_id")
            user_name = payload.get("user_name")
            user_role = payload.get("user_role")
            # 返回用户信息字典
            return {"user_id": user_id, "user_name": user_name, "user_role": user_role}
        except jwt.exceptions.InvalidTokenError:
            return {}


class UserPasswd:
    """
    用户密码
    """

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # 获取加密salt
    @staticmethod
    def generate_salt() -> str:
        return bcrypt.gensalt().decode()

    # 密码校验
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    # 获取用户加密密码
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)



SECRET_KEY = "fe0c8b9f5375ba0f0ee4f657c12c2a22a239fc97f7c74c23bcfccdb42b35106b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 生成一个 32 字节的随机密钥
# secret_key = secrets.token_hex(32)
# print("Generated Secret Key:", secret_key)




def create_access_token(data: dict, expires_delta: timedelta = None):
    """生成 JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """验证 JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


def get_current_user(request: Request) -> Dict:
    auth_header = request.headers.get("Authorization")
    print("Authorization Header:", auth_header)
    if auth_header is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")

    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded Payload:", payload)
        return {"username": payload.get("sub"), "role": payload.get("role")}

    except JWTError as e:
        print("JWT Error:", str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的Token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token已过期")



