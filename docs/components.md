# Components

All classes with tag `base` are required for the component to look right.\
Classes with the `utility` tag are add-ons to the `base` classes, i.e: adds animation or makes them look even better.

Content Table
- [Components](#components)
  - [Button](#button)


## Button

```html
<!-- Using button tag -->
<button class="bg-primary-gradient button button-transition" type="button">Click Me!</button>

<!-- Using anchon tag -->
<a href="#" class="bg-primary-gradient button button-transition">Click Me!</a>

<!-- Using input tag -->
<input type="submit" value="Click Me!" class="bg-primary-gradient button button-transition"/>
```

Since the component is actually just made with css, the actual element that it is used depends on the developer.\
This allow much more flexibility when trying to style a button.\

| Class | Description | Tag |
| :---- | :---------- | :-- |
| `button` | Base class of a button. | `base` |
| `button-sm` | A smaller version of the base class. | `base` |
| `button-lg` | A slightly bigger version of the base class. | `base` |
| `button-xl` | Largest version of a button. | `base` |
| `button-transition` | This is a utility class that adds animation to a button. | `utility` |