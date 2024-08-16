SYSTEM:

Title: Simple JSON format template
returns the answer with following format:
{"result":["x","y","z"]}

Title:  Nested JSON format template
returns the answer with following format:
{"result":[{"result":["x","y","z"]},{"result":["x","y","z"]}]}

Title:  Simple HTML format template
returns the answer with following format:
<div>content</div>

Title:  Nested HTML format template
returns the answer with following format:
<div>
    content 0
    <div>
        content 1
    </div>
</div>