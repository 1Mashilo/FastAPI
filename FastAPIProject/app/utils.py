from passlib.context import CryptContext

pwd_contract = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_contract.hash(password)

def verify(plain_password, hash_password):
    return pwd_contract.verify(plain_password, hash_password)

def sqlalchemy_model_to_dict(model):
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}
