from fastapi import FastAPI
from backend.api import router as api_router

# load messages in global message generator
from backend.system.message_generator import message_generator
from backend.system.crud.crud_messages import crud_messages, crud_default_vocabulary
message_generator.load(messages=crud_messages, vocabulary=crud_default_vocabulary)

app = FastAPI()

app.include_router(
    router=api_router,
    prefix='/api',
)

