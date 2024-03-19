from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from router import blog_get, blog_post, user, article, product, file
from db import models
from db.database import engine
from exceptions import StoryException
from auth import authentication
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import time
from client import html
from fastapi.websockets import WebSocket, WebSocketDisconnect

app = FastAPI()
app.include_router(authentication.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(file.router)

@app.get('/hello')
def index():
    return {"message": "Hello World"}

@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"detail": exc.name}
    )
    
@app.get("/")
async def get():
    return HTMLResponse(html)

clients = []

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                await client.send_text(data)
    except WebSocketDisconnect:
        print("Client disconnected.")
    except Exception as e:
        print(f"WebSocket error: {e}")

# @app.exception_handler(HTTPException)
# def custom_handler(Request: Request, exc: StoryException):
#     return PlainTextResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)

models.Base.metadata.create_all(engine)

origins = ["http://localhost/3000"]

@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response


app.add_middleware(
    CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)

app.mount("/files", StaticFiles(directory="files"), name="files")