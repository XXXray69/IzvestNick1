from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.chats import router as chats_router
from app.api.messages import router as messages_router
from app.api.ws import router as ws_router
from app.core.config import settings
from app.core.db import Base, engine

# Import models so SQLAlchemy registers them.
from app.models import chat as _chat  # noqa: F401
from app.models import device_session as _device_session  # noqa: F401
from app.models import message as _message  # noqa: F401
from app.models import user as _user  # noqa: F401

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(users_router, prefix=settings.API_V1_PREFIX)
app.include_router(chats_router, prefix=settings.API_V1_PREFIX)
app.include_router(messages_router, prefix=settings.API_V1_PREFIX)
app.include_router(ws_router)


@app.get('/')
def root():
    return {'name': settings.APP_NAME, 'status': 'ok', 'web_app': '/app'}


@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)


app.mount("/app", StaticFiles(directory="app/static", html=True), name="static_app")
