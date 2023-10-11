import uvicorn
from fastapi import FastAPI, Request,  Response
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, SessionLocal
from app.apis import user, user_profile
from app.models import user as user_model
from app.auth import auth

user_model.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Fast API USER AUTH",
    description="A simple API for user authentication",
    version="0.0.1",
    contact={
        "name": "Jordy Orel KONDA",
        "email": "jordyorel@protonmail.com",
    },
    license_info={
        "name": "MIT",
    },
)
 
@app.middleware("http")
async def db_session_middleware(request: Request , call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Dependency
def get_db(request: Request): 
    return request.state.db

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(user_profile.router)


@app.get("/")
def root():
    return {"message": "Welcome to the API"}


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

