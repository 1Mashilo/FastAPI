# utils.py
def sqlalchemy_model_to_dict(model):
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}
