# Components

Content Table

- [Input](#input)

## Input

```python
# views.py

def some_view(request):
  # some code
  context = {
    "input": {
      "attributes": {
        "name": "username",
        "type": "text",
        "required": "true",
        "placeholder": "Enter Username"
      },
      "label": "Username:"
      # here we can decide its look after some input validation
      "state": "valid" if data_is_valid else "invalid" if data_is_invalid else None
    }
  }
  # some more code
  return render(request, template, context)
```

```html
<!-- html file where the input component is neede. -->
<!-- Should just be included with some context -->
{% include 'components/input.html' with input_context=input %}

<!-- 
  If there is only one input in the entire html, then having
  a key "input_context" in the main context is good enough.
  Get rid of the need to pass a specific context for the input.
-->
{% include 'components/input.html' %}
```

### Input Component Context Tale

| Key | Value | Description |
| :-- | :---- | :---------- |
| `attributes` | `dictionary` | This should be a dictionary with the keys being an attribute of an input tag and its value being the correct value the attribute needs.|
| `label` | `string` | This is the label text that is above the input box. |
| `state` | `"valid"`, `"invalid"`, `None` | This decides the look of the input box. `valid` for a green look, and `invalid` for a red look. If neither look is desired then do not defined this in the context.|

The input component is built to be able to handle simple validation that the element tag originally supports. Since the `invalid` style uses the pseudo-selector `:invalid`.