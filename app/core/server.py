from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Request, Form
from auth.security import get_current_user, authenticate_user
from core.manager import manager
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from auth.jwt import create_access_token
from db.user_repository import user_repository

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request
    })

@app.post("/token")
async def login_for_access_token(request: Request, username: str = Form(...), password: str = Form(...)):
    if not authenticate_user(username, password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ცუდი მონაცემები")
    access_token = create_access_token(data = {
        "sub": username
    })
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.websocket("/server/{token}")
async def endpoint(websocket: WebSocket, token: str):
    user = get_current_user(token)
    username = user.username
    await manager.connect(websocket, token)
    try:
        while True:
            data = await websocket.receive_text()
            message = f"{username}: {data}"
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} left the chat.")

@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    result = user_repository.register_user(username, password)
    if result:
        return templates.TemplateResponse("register_success.html", {"request": request, "username": username})
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration failed")  
    
@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})