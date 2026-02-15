from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.database import engine, Base
from .api import auth, projects, generation, advanced

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoDev API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(generation.router)
app.include_router(advanced.router)

@app.get("/")
def root():
    return {"message": "AutoDev API is running"}
