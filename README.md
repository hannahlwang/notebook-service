# notebook-service
This is a scholarly notebook service, a simple web API implemented using [Flask](http://flask.pocoo.org/) and [Flask-RESTful](http://flask-restful.readthedocs.org/en/latest/).

To run it:

1. Install required dependencies:
   ```
   $ pip install -r requirements.txt
   ``` 
   [Flask](http://flask.pocoo.org/docs/0.10/installation/#installation)
   and
   [Flask-RESTful](http://flask-restful.readthedocs.org/en/latest/installation.html) to run `server.py` 
   and [RDFLib](http://rdflib.readthedocs.org/en/latest/) and [JSONLD for RDFLib](https://github.com/RDFLib/rdflib-jsonld) to run the `extractdata.py` script or the `another-server.py` service.

2. Run the notebook service server:
   ```
   $ python server.py
   ```
   
   Service can be accessed at `localhost:8080`.

## Application flow
These are the attribute values used to describe the application flow.

### class
- `notebooks`
	Indicates parent tag of a notebooks document.
- `notebooks-list`
	May appear in `notebooks`. Contains a collection of notebooks.
- `new-notebook`
	May appear in `notebooks`. Used to describe a form for creating a new notebook.
- `notebook`
	Indicates parent tag of a notebook document.
- `notes-list`
	May appear in a `notebook`. Contains a collection of notes.
- `new-note`
	May appear in `notebook`. Used to describe a form for creating a new note.
- `note`
	Indicates parent tag of a note document.
- `note-text`
	May appear in a `note`. Contains the text of the note.
- `references`
	Indicates parent tag of a references document.
- `references-list`
	May appear in a `reference`. Contains a collection of references.
- `add-reference`
	May appear in a `references-list`. Used to describe a form for creating a new reference.
- `reference`
	Indicates parent tag of a reference document.
- `reference-text`
	May appear within `reference`. Contains the text of the reference.
- `related-notes`
	May appear within `reference`. Contains a collection of notes related to the reference.

### rel
- `alternate`
	May be used to describe an alternate representation of a resource, such as a JSON representation of a notebook, note, or reference.
- `item`
	May be used to describe a notebook part of a notebook list, a note part of a notebook, or a reference part of a reference list.
- `collection`
	May be used to describe a containing notebook list (in relation to a notebook), containing notebook (in relation to a note), or a containing reference list (in relation to a reference). 
- `related` 
	May be used to describe a reference related to a note, or a note related to a reference.

## JSON-LD Representations
These are the types and properties used to describe the data.

### http://schema.org/CreativeWork 
Notebooks, notes, and references are all of the schema.org type CreativeWork. Refers to http://schema.org/CreativeWork

### author 
Used to describe the author of a reference. Refers to http://schema.org/author.

### children
Used to describe the notes contained in a notebook. Can have more that one. Refers to http://schema.org/hasPart.

### citation
Used to describe a citation of a reference in a note. Can have more than one. Refers to http://schema.org/citation.

### notebooks
Used to describe the container element of notebooks. Is of type http://www.w3.org/2000/01/rdf-schema#member.

### notes
Used to describe the container element of notes. Is of type http://www.w3.org/2000/01/rdf-schema#member.

### parent
Used to describe the notebook that contains a note. Refers to http://schema.org/isPartOf.

### place
Used to describe the publication location of a reference. Refers to http://schema.org/locationCreated.

### publisher
Used to describe the publisher of a reference. Refers to http://schema.org/publisher.

### references
Used to describe the container element of references. Is of type http://www.w3.org/2000/01/rdf-schema#member.

### related
Used to describe a note that cites a reference. Is the reverse property of http://schema.org/citation.

### text
Used to describe the main text of a note. Refers to http://schema.org/text.

### time
Used to describe the time a note, notebook, or reference was created. For notes and notebooks, time is an automatically-generated timestamp. For references, time is the year entered in the "date" field when creating a reference, and refers to the date published. Refers to http://schema.org/dateCreated.

### title
Used to describe the title of a note, notebook, or reference. Refers to http://schema.org/name.
