from .Main import app

from flask_restful import Api
from flask_cors import CORS
from flask_caching import Cache
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

Compress(app)
api    = Api(app)
cors   = CORS(app)
caches = Cache(app)
db     = SQLAlchemy(app)
ma     = Marshmallow(app)
bcrypt = Bcrypt(app)