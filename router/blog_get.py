from fastapi import APIRouter, status, Response, Depends
from enum import Enum
from typing import Optional
from router.blog_post import required_functionality


router = APIRouter(
    prefix="/blog",
    tags=["blog"],
)

@router.get('/all',
         summary="Retrive all Blogs",
         description="This API Call simulates fetching all blogs from the database",
         response_description="List of available blogs",
         )
def get_all_blogs(page: int = 1, page_size: Optional[int] = None, req_parameter: dict = Depends(required_functionality)):
    return {"message": f"All {page_size} blogs on page: {page}", "req": req_parameter}

@router.get('/{id}/comments/{comment_id}', tags=["comments"])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    """
    Simulates retrieving a comment from a blog.
    
    - **id**: Mandatory path parameter.
    - **comment_id**: Mandatory path parameter.
    - **valid**: Optional query parameter.
    - **username**: Optional query parameter.
    """
    return {"message": f"blog_id: {id}, comment_id: {comment_id}, valid: {valid}, username: {username}"}

class BlogType(str, Enum):
    short = "short"
    story = "story"
    howto = "howto"

@router.get('/type/{type}')
def get_blog_type(type: BlogType):
    return {"message": f"Blogs of type: {type.value}"}

@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Blog {id} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f"Blog with id: {id}"}