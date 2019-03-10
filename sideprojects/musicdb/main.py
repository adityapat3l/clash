# http://www.blog.pythonlibrary.org/2017/12/12/flask-101-getting-started/

from app import app
from db_setup import init_db

init_db()


@app.route('/')
def test():
    return "Welcome to Flask!"

if __name__ == '__main__':
    app.run()