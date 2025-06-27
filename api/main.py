from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")

db = client["sistema_escolar"]
maestros_collection = db["maestro"]
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Maestro(BaseModel):
    id: int
    nombre: str
    apellidos: str
    email: str
    password: str
    telefono: str
    area_investigacion: str
    materias: list[str] = []

@app.get("/maestros/")
def obtener_maestros():
    maestros = list(maestros_collection.find({}, {"_id": 0}))
    return maestros

@app.post("/maestros/")
def insertar_maestro(maestro: Maestro):
    maestro_dict = maestro.dict()
    maestro_dict["password"] = crypt.hash(maestro_dict["password"])

    maestros_collection.insert_one(maestro_dict)
    return {"mensaje": "Maestro insertado correctamente"}

