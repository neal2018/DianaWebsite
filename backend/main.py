from logging import DEBUG
from fastapi import FastAPI, BackgroundTasks
from utils import Checker, write_log
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import jieba

DEBUG = False

app = FastAPI()
check = Checker()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


class Data(BaseModel):
    content: str


@app.post("/check")
async def root(request: Data, background_tasks: BackgroundTasks):
    similarity_rates = await check.paper_check(request.content)
    background_tasks.add_task(write_log, request.content)
    return similarity_rates

if __name__ == "__main__":
    import uvicorn
    jieba.initialize()
    if not DEBUG:
        key = "../../ssl/key.key"
        crt = "../../ssl/crt.crt"
        uvicorn.run(app='main:app', host="0.0.0.0", port=8888,
                    ssl_keyfile=key, ssl_certfile=crt, reload=True, debug=False)
    else:
        uvicorn.run(app='main:app', host="0.0.0.0",
                    port=8888, reload=True, debug=True)
