from requests import request
from typing import List
from uuid import uuid4

import requests

class Strapi:

    def __init__(self, url: str = "http://127.0.0.1:1337") -> None:
        self.token = None
        self.url = url
    
    def call(self, method: str, path: str, data=None, files=None, headers=None) -> dict or List[dict]:
        if (self.token != None):
            headers = {"Authorization": f"Bearer {self.token}"}
        return request(method=method, url=f"{self.url}{path}", files=files, headers=headers, json=data).json()

    def auth(self, username: str, password: str) -> None:
        if (self.token == None):
            auth = self.call("POST", "/auth/local", data={"identifier": username, "password": password})
            self.token = auth.get("jwt")
            if (self.token == None):
                raise Exception(auth)

    def query(self, query: dict) -> dict:
        return self.call("POST", "/graphql", data={"query": query}).get("data")
    
    def create_entity(self, colletion: str, data: dict) -> dict:
        return self.call("POST", f"/{colletion}", data=data)

    def get_entity(self, colletion: str, id: str = None) -> dict:
        path = f"/{colletion}"
        if (id != None):
            path += f"/{id}"
        return self.call("GET", path)

    def list_entities(self, colletion: str) -> List[dict]:
        return self.call("GET", f"/{colletion}")
    
    def update_entity(self, colletion: str, id: str = None, data: dict = {}) -> dict:
        path = f"/{colletion}"
        if (id != None):
            path += f"/{id}"
        return self.call("PUT", path, data=data)
    
    def upload_image(self, file: object, filename: str = None) -> dict:
        if (filename == None):
            filename = f'{str(uuid4())}.png'
        return self.call("POST", "/upload", files={'files': (filename, file, 'image', {'uri': ''})})
