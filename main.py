import __init__ # noqa

from app import init_app, run

app = init_app()


if __name__ == '__main__':
    # pass
    # uvicorn main:app --host 0.0.0.0 --port 8061
    run("0.0.0.0", 8088)
