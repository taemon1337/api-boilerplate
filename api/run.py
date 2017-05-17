from eve import Eve
from os import getenv

MONGO_HOST = getenv("MONGO_HOST","mongo")
MONGO_PORT = int(getenv("MONGO_PORT", "27017"))
MONGO_DBNAME = getenv("MONGO_DBNAME","default-db")

users_schema = {
  'username': {
    'type': 'string',
    'required': True,
    'regex': '[\w]+',
    'unique': True
  },
  'displayname': {
    'type': 'string',
    'required': True,
    'unique': True
  },
  'role': {
    'type': 'list',
    'default': ['user'],
    'allowed': ['user','admin','guest']
  },
  'favorites': {
    'type': 'list',
    'default': [],
    'schema': {
      'type': 'objectid',
      'data_relation': {
        'resource': 'posts',
        'field': '_id',
        'embeddable': True
      }
    }
  }
}

posts_schema = {
  'title': {
    'type': 'string',
    'required': True,
    'unique': True
  },
  'content': {
    'type': 'string',
    'default': '{}'
  },
  'author': {
    'type': 'objectid',
    'data_relation': {
      'resource': 'users',
      'field': '_id',
      'embeddable': True
    }
  }
}

settings = {
  'URL_PREFIX': 'api',
  'MONGO_HOST': MONGO_HOST,
  'MONGO_PORT': MONGO_PORT,
  'MONGO_DBNAME': MONGO_DBNAME,
  'RESOURCE_METHODS': ['GET','POST'],
  'ITEM_METHODS': ['GET','PUT','PATCH','DELETE'],
#  'MULTIPART_FORM_FIELDS_AS_JSON': True,
  'XML': False,
  'RETURN_MEDIA_AS_URL': True,
  'RETURN_MEDIA_AS_BASE64_STRING': False,
  'EXTENDED_MEDIA_INFO': ['name','length','content_type'],
  'MEDIA_ENDPOINT': 'raw',
  'CACHE_CONTROL': 'max-age:0,must-revalidate',
  'DATE_FORMAT': '%Y-%m-%d %H:%M:%S',
  'DOMAIN': {
    'users': {
      'schema': users_schema,
      'embedded_fields': ['favorites']
    },
    'posts': {
      'schema': posts_schema,
      'embedded_fields': ['author']
    }
  }
}

app = Eve(settings=settings)

if __name__ == "__main__":
  host = getenv("HOST","0.0.0.0")
  port = int(getenv("PORT","8080"))
  debug = getenv("DEBUG",True)
  app.run(host=host, port=port, debug=debug)

