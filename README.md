# notebook-service
A scholarly notebook service

## Application flow
These are the attribute values used to describe the application flow.

###class
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

###rel
- `item`
	May be used to describe a notebook part of a notebook list, a note part of a notebook, or a reference part of a reference list.
- `collection`
	May be used to describe a containing notebook list (in relation to a notebook), containing notebook (in relation to a note), or a containing reference list (in relation to a reference). 
- `related` 
	May be used to describe a reference related to a note, or a note related to a reference.
