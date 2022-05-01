# Side Menu

# Side Menu (Version1)

---

## Before you read, you have to understand that:

- The side menu template haven't finish, and it got a few problems that need to be addressed:
  1. The side menu needed to be include almost every pages, except the 'landing page' and 'login and register page', but currently it works only in 'homepage'.
  2. Since we haven't created projects yet, I basically render the dummy context to the homepage.html:
     ```
     tech = {
         'python': ['E-commerce', 'Hotel Booking App'],
         'html':['E-commerce', 'Hotel Booking App', 'Portfolio'],
         'css':['AmazingMe', 'Coding Journey'],
     }
     ```
     ```
     context = {
         "name" : 'item name',
         "logo" : 'svg/bookmark.html',
         "link" : 'homepage',
         "tech" : tech
     }
     ```
     which supposed to be project querysets that we can extract values from it, but for now...yeah.

## Ok Continue...

This is the look of side menu
![The side menu included in homepage](https://snipboard.io/zj5MxI.jpg) - The top part of the menu is the menu list, which contains list items - The bottom part is all the tech cards.

```
<!-- Include the side menu -->
{% block side_menu %}
    {% include "components/sidemenu.html" %}
{% endblock side_menu %}
```

Side menu is one of the major components in our app.  
It is used to show both the menu list, and the tech cards.

## Inside sidemenu.html

I would like to talk about menu list first.

### Menu List

---

```
<div class="mb-8 space-y-1">
      {% include 'components/menu_item.html' with name="Skill Tree"  link="homepage" logo="
        logo='svg/bookmark.html'%}
      {% include 'components/menu_item.html' with name="All Projects"  link="landing_page" %}
      {% include 'components/menu_item.html' with name="Settings"  link="landing_page" %}
  </div>
```

- A list that contains multiple links (aka menu item), which allows user to link to certain page more easily.
- There are 3 attributes that you can change while including menu item component in any html page:
  1. name: the name of the item list
  2. link: the link of the certain page
  3. logo: the logo aside the name

### Tech Card Section

---

picture for tech card section

```
<div class="mb-10 space-y-4">
    {% include "components/tech_card.html" %}
</div>
```

- A section that contains multiple tech card, which contains the technology name (python, javascript, html...), and the user project's names that use those technologies.
- User can click on the tech card they wanna look on, which act as a navigation to the part of the project.
- The context inside the tech card is rendered through context

#### Side Note:

Inside the base.html, there are two new blocks created, **Side menu block** and **side content block** that act like a placeholder for us to pui / not put the code in whenever we extends the base.html.

What is **side menu block** & **side content block**?
**Side menu block**: the block to include the sidemenu template
**Side Content Block**: the block to include the main content, like the node tree, and the tables...

```
{% block content %}
    {% block side_menu %}
    {% endblock side_menu %}

    {% block side_content %}
    {% endblock side_content %}
{% endblock content %}
```
