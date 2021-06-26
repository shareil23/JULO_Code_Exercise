from src import app
from meinheld import server # mainheld server

if __name__ == '__main__':
    # app.run(debug=True)
    server.listen("0.0.0.0")
    server.run(app)