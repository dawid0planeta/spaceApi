import functools

from flask import (
    Response, Blueprint, flash, jsonify, g, redirect, render_template, request, session, url_for
)

from rocket_api.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.before_app_request
def load_db():
    g.db = get_db()


def constructDataList(file_id):
    """Creates formated list of data from database"""
    data_obj = g.db.execute("SELECT * FROM readouts WHERE file_id = ?", (file_id, )).fetchall()

    return [{"timestamp": str(row['timestamp']),
                    "value": str(row['value'])} for row in data_obj]


def constructFileJson(file_obj):
    """Creates dict object of file from database"""
    data = constructDataList(file_obj['id'])

    return {"filename": file_obj['filename'], "description": file_obj['description'], "data": data, "version": file_obj['version']}

@bp.route('/getIds', methods=('GET', ))
def info():
    """Prints populated ids"""
    files = g.db.execute("SELECT * FROM files").fetchall()

    return jsonify([each['id'] for each in files])

@bp.route('/getAll', methods=('GET',))
def getAll():
    files_db = g.db.execute("SELECT * FROM files").fetchall()
    files = [constructFileJson(each) for each in files_db]

    return jsonify(files)



@bp.route('/getOne/<id>', methods=('GET',))
def getOne(id):
    file_obj = g.db.execute("SELECT * FROM files WHERE id = ?", (id, )).fetchone()
    if file_obj is None:
        return Response(status=404)

    return jsonify(constructFileJson(file_obj))

@bp.route('/addOne', methods=('POST',))
def addOne():
    req_data = request.get_json()

    #Check if file already exists
    file_check = g.db.execute("SELECT * FROM files WHERE filename=?", (req_data['filename'], )).fetchone()

    if file_check is None:
        #TODO: handle multiple adding of same file
        #Add file to files table
        g.db.execute("INSERT INTO files (filename, description, version) VALUES (?, ?, ?)", (req_data['filename'], req_data['description'], req_data['version']))

        #Get file id from database
        file_id = g.db.execute("SELECT * FROM files WHERE filename=?", (req_data['filename'], )).fetchone()["id"]
    
        #Add filedata to readouts table
        for readout in req_data['data']:
            #Timestamp and value stored as int. Allows filtering independently of file 
            g.db.execute("INSERT INTO readouts (file_id, timestamp, value) VALUES (?, ?, ?)", (file_id, readout['timestamp'], readout['value']))

        g.db.commit()

    return Response(status=201)

@bp.route('/delete/<id>', methods=('DELETE',))
def delete(id):
    g.db.execute("DELETE FROM files WHERE id=?", (id, )) 
    g.db.execute("DELETE FROM readouts where file_id=?", (id, ))
    g.db.commit()

    return Response(status=200)