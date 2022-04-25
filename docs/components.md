# Components

Content Table

- [Components](#components)
  - [Input](#input)
    - [Input Component Context Tale](#input-component-context-tale)
  - [Filter](#filter)
    - [Filter Object For Context](#filter-object-for-context)

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

## Filter

```html
{% include 'components/filter.html' with filter=filter_object %}
<!-- or with context = { "filter": { ... } " -->
{% include 'components/filter.html' %}
```

```python
# views.py

def view_with_filter(request):
  template = "app/template.html"
  endpoint = "/api/filter"
  # create a list of selections
  ...
  context = {
    "filter": {
      "selections": selections, # list
      "endpoint": endpoint
    }
  }
  if request.method == "POST":
    # handle filter query
    # get filter query value
    filter_query = request.POST.get("filter-query")
    # search in database
    ...
    # make context
    ...
    return render(request, template, context) # return a view with filtered content

  return render(request, template, context) # return a view with all content
```

### Filter Object For Context
| Field | Description |
| :---- | :---------- |
| `selections` | A list of strings with the available filtering selections. This values should match the category that we can actually query or compare with what it is in the database. |
| `endpoint` | The endpoint url. It is going to send a `POST` request with a form. Get the value of the query with `request.POST.get("filter-query")`. |