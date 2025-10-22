from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import text
from sqlalchemy.orm import Session

from controllers.router import api_router
from db.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-form")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


@app.get("/test_db", tags=["Test DB"])
def teste_conexao_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return {
            "message": "Database connection established!",
            "result": result,
        }
    except Exception as e:
        return {"error": str(e)}


app.include_router(api_router, prefix="/api")
