from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

# ⚙️ Paramètres du token
SECRET_KEY = "une_cle_ultra_secrete_a_changer"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# Déclare le schéma d'authentification utilisé (Bearer token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from service.user_service import UserService

user_service = UserService()

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
       
        user = user_service.trouver_par_username(username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user  # renvoie l'objet User complet
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def verify_admin(user = Depends(verify_token)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user