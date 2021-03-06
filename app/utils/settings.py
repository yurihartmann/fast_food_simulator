import os
from typing import Any

from app.core.singleton_model import SingletonModel


class SETTINGS(metaclass=SingletonModel):

    MONGO_URI: str = os.getenv('MONGO_URL', None)
    ITEMS_PER_PAGE: int = 2
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.validate_mongo_uri()

    def validate_mongo_uri(self):
        if not self.MONGO_URI:
            raise ValueError('MONGO_URI should be not empty')

    def serialize(self):
        return {
            "MONGO_URI": self.MONGO_URI,
            "ITEMS_PER_PAGE": self.ITEMS_PER_PAGE,
            "SECRET_KEY": self.SECRET_KEY,
            "ALGORITHM": self.ALGORITHM,
            "ACCESS_TOKEN_EXPIRE_MINUTES": self.ACCESS_TOKEN_EXPIRE_MINUTES,
        }
