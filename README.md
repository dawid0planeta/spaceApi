# spaceApi
API to access rocket engine testing data

## Endpoints
* `GET /api/getIds` - get ids of every file currently in database
* `GET /api/getAll` - get contents of every file
* `GET /api/getOne/id` - get contents of file with specified id
* `POST /api/addOne` - add one file to database
* `DELETE /api/delete/id` - delete file with specified id 

## Instalation
```bash
git clone https://github.com/dawid0planeta/spaceApi.git
cd spaceApi
python3 -m venv venv
. venv/bin/activate
pip3 install Flask

export FLASK_APP=rocket_api
export FLASK_ENV=development
flask db-init
flask run
```