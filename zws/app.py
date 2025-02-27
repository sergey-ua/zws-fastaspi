from fastapi import FastAPI

from zws.database.models.url_model import Base, BlockedHostname
from zws.dependencies import engine, get_db
from zws.routes.api import api_router

app = FastAPI(
    title="Link shortener",
    description="FastAPI application providing a link shortener service",
    version="1.0.0"
)

# This is for Dev purposes only.
def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with get_db() as db:
        try:
            # Add a sample row to URLModel
            sample_url = BlockedHostname(hostname="example.com")
            db.add(sample_url)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

@app.on_event("startup")
def on_startup():
    init_db()

# Include Routers
app.include_router(
    api_router,
    prefix="/api",
    tags=["API"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="", port=9997)