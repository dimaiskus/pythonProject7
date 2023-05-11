import uvicorn
from fastapi import FastAPI

app = FastAPI()
def sum_two_args(x,y):
 return x+y
# Hello World route
@app.get("/")
def read_root():
 return {"Hello": "World"}
if __name__ == "__main__":
 uvicorn.run(app, host="127.0.0.1", port=5000)