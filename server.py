from flask import Flask, render_template, render_template_string, make_response, redirect
from flask.ext.restful import Api, Resource, reqparse, abort

import json
import string
import random
from datetime import datetime

# Load data from disk
with open('data.jsonld') as data:
    data = json.load(data)


# Generate a unique ID for a new notebook, note, or reference.
# By default this will consist of six lowercase numbers and letters.
def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Respond with 404 Not Found if no notebooks with the specified ID exists.
def error_if_notebookid_not_found(notebook_id):
    if notebook_id not in data['notebooks']:
        message = "No notebook with ID: {}".format(notebook_id)
        abort(404, message=message)

# Respond with 404 Not Found if no note with specified ID exists.
def error_if_noteid_not_found(note_id):
    if note_id not in data['notes']:
        message = "No note with ID: {}".format(note_id)
        abort(404, message=message)

# Respond with 404 Not Found if no reference with specified ID exists.
def error_if_referenceid_not_found(reference_id):
    if reference_id not in data['references']:
        message = "No reference with ID: {}".format(reference_id)
        abort(404, message=message)

# Given the data for a notebook and the notes in it, generate an HTML representation
# of that notebook.
def render_notebook_as_html(notebook, notes):
    return render_template(
        'notebook.html',
        notebook=notebook,
        notes=notes
        )


# Given the data for a list of notebooks, generate an HTML representation
# of that list.
def render_notebook_list_as_html(notebooks):
    return render_template(
        'notebooks.html',
        notebooks=notebooks
        )
    
# Given the data for a note, generate an HTML representation of that note.
def render_note_as_html(note, references):
    return render_template(
        'note.html',
        note=note,
        references=references
        )

# Given the data for a reference, generate an HTML representation of that reference.
def render_reference_as_html(reference, notes):
    return render_template(
        'reference.html',
        reference=reference,
        notes=notes
        )

# Given the data for a list of notebooks, generate an HTML representation
# of that list.
def render_reference_list_as_html(references):
    return render_template(
        'references.html',
        references=references
        )

# Raises an error if the string x is empty (has zero length).
def nonempty_string(x):
    s = str(x)
    if len(x) == 0:
        raise ValueError('string is empty')
    return s


# Specify the data necessary to create a new notebook (title is required)
new_notebook_parser = reqparse.RequestParser()
new_notebook_parser.add_argument(
    'notebook-title', 
    type=nonempty_string, 
    required=True, 
    help="Title is a required value")

# Specify the data necessary to create a new note (title and text are required)
new_note_parser = reqparse.RequestParser()
for arg in ['title', 'text']:
    new_note_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))

# Specify the data necessary to update an existing note.
# Only the reference citations can be updated
update_note_parser = reqparse.RequestParser()
update_note_parser.add_argument(
    'citation', 
    type=str)

new_reference_parser = reqparse.RequestParser()
for arg in ['author', 'time', 'title', 'publisher', 'place']:
    new_reference_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))

# Define reference resource.
class Reference(Resource):

 # If a reference with the specified ID does not exist,
    # respond with a 404, otherwise respond with an HTML representation.
    def get(self, reference_id):
        error_if_referenceid_not_found(reference_id)
        notes = data['notes'].items()
        return make_response(
            render_reference_as_html(
                (data['references'][reference_id]), notes), 200)


# Define a resource for getting a JSON representation of a reference.
class ReferenceAsJSON(Resource):

    # If a reference with the specified ID does not exist,
    # respond with a 404, otherwise respond with a JSON representation.
    def get(self, reference_id):
        error_if_referenceid_not_found(reference_id)
        reference = data['references'][reference_id]
        reference['@context'] = data['@context']
        return reference

# Define our reference list resource.
class ReferenceList(Resource):

    # Respond with an HTML representation of the notebook list
    def get(self):
        references = data['references'].items()
        return make_response(
            render_reference_list_as_html(references), 200)

    # Add a new notebook to the list, and respond with an HTML
    # representation of the updated list.
    def post(self):
        reference = new_reference_parser.parse_args()
        reference_id = generate_id()
        reference['@type'] = "http://schema.org/CreativeWork"
        reference['@id'] = 'reference/' + reference_id
        data['references'][reference_id] = reference
        references = data['references'].items()
        return make_response(
            render_reference_list_as_html(references), 201)


# Define our note resource.
class Note(Resource):

    # If a note with the specified ID does not exist,
    # respond with a 404, otherwise respond with an HTML representation.
    def get(self, note_id):
        error_if_noteid_not_found(note_id)
        references = data['references'].items()
        return make_response(
            render_note_as_html(
                (data['notes'][note_id]), references), 200)

    def patch(self, note_id):
        error_if_noteid_not_found(note_id)
        note = data['notes'][note_id]
        update = update_note_parser.parse_args()
        note.setdefault('citation', []).append(update['citation'])
        references = data['references'].items()
        reference = data['references'][update['citation']]
        reference.setdefault('related', []).append(note_id)
        return make_response(
            render_note_as_html(
                (data['notes'][note_id]), references), 200)

# Define a resource for getting a JSON representation of a notebook.
class NoteAsJSON(Resource):

    # If a note with the specified ID does not exist,
    # respond with a 404, otherwise respond with a JSON representation.
    def get(self, note_id):
        error_if_noteid_not_found(note_id)
        note = data['notes'][note_id]
        note['@context'] = data['@context']
        return note


# Define our notebook resource.
class Notebook(Resource):

    # If a notebook with the specified ID does not exist,
    # respond with a 404, otherwise respond with an HTML representation.
    def get(self, notebook_id):
        print notebook_id
        notebook = data['notebooks'][notebook_id]
        print notebook
        child_notes = []
        notes = data['notes'].items()
        for note in notes:
            note_id = note[0]
            if data['notes'][note_id]['parent'] == notebook_id:
                child_notes.append(note)
        error_if_notebookid_not_found(notebook_id)
        return make_response(
            render_notebook_as_html(notebook, child_notes), 200)
    
    # Add a new note to the notebook, and respond with an HTML
    # representation of the updated list of notes.
    def post(self, notebook_id):
        notebook = data['notebooks'][notebook_id]
        note = new_note_parser.parse_args()
        note_id = generate_id()
        note['@type'] = "http://schema.org/CreativeWork"
        note['@id'] = 'note/' + note_id
        note['time'] = datetime.isoformat(datetime.now())
        note['parent']= notebook_id
        notebook.setdefault('children', []).append(note_id)
        data['notes'][note_id] = note
        notes = data['notes'].items()
        child_notes = []
        for note in notes:
            note_id = note[0]
            if data['notes'][note_id]['parent'] == notebook_id:
                child_notes.append(note)
        return make_response(
            render_notebook_as_html(notebook, child_notes), 201)


# Define a resource for getting a JSON representation of a notebook.
class NotebookAsJSON(Resource):

    # If a notebook with the specified ID does not exist,
    # respond with a 404, otherwise respond with a JSON representation.
    def get(self, notebook_id):
        error_if_notebookid_not_found(notebook_id)
        notebook = data['notebooks'][notebook_id]
        notebook['@context'] = data['@context']
        return notebook


# Define our notebook list resource.
class NotebookList(Resource):

    # Respond with an HTML representation of the notebook list
    def get(self):
        notebooks = data['notebooks'].items()
        return make_response(
            render_notebook_list_as_html(notebooks), 200)

    # Add a new notebook to the list, and respond with an HTML
    # representation of the updated list.
    def post(self):
        notebook = new_notebook_parser.parse_args()
        notebook_id = generate_id()
        notebook['@type'] = "http://schema.org/CreativeWork"
        notebook['@id'] = 'notebook/' + notebook_id
        notebook['title'] = notebook['notebook-title']
        notebook['time'] = datetime.isoformat(datetime.now())
        data['notebooks'][notebook_id] = notebook
        notebooks = data['notebooks'].items()
        return make_response(
            render_notebook_list_as_html(notebooks), 201)


# Define a resource for getting a JSON representation of the notebook list.
class NotebookListAsJSON(Resource):
    def get(self):
        return data


# Assign URL paths to our resources.
app = Flask(__name__)
api = Api(app)
api.add_resource(NotebookList, '/notebooks')
api.add_resource(NotebookListAsJSON, '/notebooks.json')
api.add_resource(Notebook, '/notebook/<string:notebook_id>')
api.add_resource(NotebookAsJSON, '/notebook/<string:notebook_id>.json')
api.add_resource(Note, '/note/<string:note_id>')
api.add_resource(NoteAsJSON, '/note/<string:note_id>.json')
api.add_resource(ReferenceList, '/references')
api.add_resource(Reference, '/reference/<string:reference_id>')
api.add_resource(ReferenceAsJSON, '/reference/<string:reference_id>.json')

# Redirect from the index to the list of notebooks.
@app.route('/')
def index():
    return redirect(api.url_for(NotebookList), code=303)


# This is needed to load JSON from Javascript running in the browser.
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

# Start the server.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
