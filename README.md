## Example Api built with Python Eve and running with Docker

This project is an example of how I build microservice APIs quickly.

### Steps to run
*Assuming you have git, docker, and docker-compose
```
git clone git@github.com:taemon1337/api-boilerplate.git
cd api-boilerplate/
docker-compose up
```

### ./docker-compose.yml
```
version: '2'
services:
  api:
    build: ./api
    volumes:
      - ./api:/api
    working_dir: /api
    command: python -u run.py
    environment:
      - MONGO_HOST=mongo
      - MONGO_PORT=27017
      - MONGO_DB=apidb
    ports:
      - 8080:8080
  mongo:
    image: mongo
    volumes:
      - ./data/mongo:/data/db
```

### ./api/Dockerfile
The API docker image is python with eve installed.
```
FROM: python:slim
RUN pip install eve
```

### ./api/run.py
The API is basically the Python Eve schema definition and runtime config.

```
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
  'XML': False,
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
```
