from werkzeug.wsgi import DispatcherMiddleware
from run import app
from app1 import app as app1

app = DispatcherMiddleware(app, {
    '/app1': app1.server,
    })


if __name__ == "__main__":
    app.run()
