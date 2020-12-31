from fastapi import FastAPI
from utils import paper_check
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import jieba

app = FastAPI()

origins = ["http://127.0.0.1:5500"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,  #设置允许的origins来源
    allow_credentials=True,
    allow_methods=["*"],  # 设置允许跨域的http方法，比如 get、post、put等。
    allow_headers=["*"])  #允许跨域的headers，可以用来鉴别来源等作用。


class Data(BaseModel):
    content: str

@app.post("/check")
async def root(request: Data):
    similarity_rates = paper_check(request.content)
    return similarity_rates

if __name__ == "__main__":
    import uvicorn
    jieba.initialize()
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)