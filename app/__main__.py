from fastapi import FastAPI
from app.api import router


app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    from unicorn import run

    run(
        app=app,
        loop="uvloop",
        http="httptools",
        interface="asgi3",
    )