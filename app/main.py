from fastapi import FastAPI
from .routers import ops, client, download

app = FastAPI()

app.include_router(ops.router)
app.include_router(client.router)
app.include_router(download.router)

@app.get('/')
def root():
    return {"message": "Secure File Sharing System API"}

# Placeholder for ops and client routers
# from .routers import ops, client
# app.include_router(ops.router)
# app.include_router(client.router) 