from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def healthcheck():
    return {"Hello": "World"}


@app.get("/query")
def modelquery():
    return {"Hello": "World"}
