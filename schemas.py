from pydantic import BaseModel
from typing import List

# Article inside UserDisplay
class Article(BaseModel):
    title: str
    content: str
    published: bool

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Article] = []
        
# User inside ArticleDisplay
class User(BaseModel):
    id: int
    username: str
        
class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int
    
class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User