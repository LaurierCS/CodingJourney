# Quick Start With Tailwind In Django

## Pre-requisites ❗

### - Have NodeJS install in your machine. [Download NodeJS](https://nodejs.org/en/download/)

## Before running server
Run the following commands

`pipenv install --skip-lock` to install all the new packages needed. \
`python manage.py tailwind install` to install tailwind and other npm packages. \
\
NOTE:
`--skip-lock` IS A WORK AROUND DUE TO AN ISSUE WHEN INSTALLING WITHOUT THE OPTION. [Click for more details.](https://github.com/LaurierCS/Pod4/issues/10)


## Run Development Server
First we need to build our css and have a hot reload to make our lives easier.\
We will need to terminals because one is for building the css and another for the web server.\
In vscode, you can open two terminals side by side by clicking on the split icon located to the left of the trash icon.\
`python manage.py tailwind start` to watch changes in our css files, hot reload.\
`python manage.py runserver` to start development server.

## [Tailwind Docs](https://tailwindcss.com/docs/aspect-ratio)


## Theme Configuration 🎨

To edit the theme, read [customize theme](https://tailwindcss.com/docs/theme). Then edit `tailwind.config.js` file located in `app/static_src`.

#### Font Family

```html
  <h1 class="font-sans">Sans Family</h1>
```

| Font priority |
| :-------- | 
| `-apple-system` | 
| `BlinkMacSystemFont` | 
| `Segoe UI` | 
| `Roboto` | 
| `sans-serif` | 

Top most font has the highest priority and bottom has the lowest priority.

#### Colors

```html
  <p class="text-primary">This is a text with the primary color</p>
```

| Color Name | Color Code |
| :-------- | :------- |  
| `primary`      | `#475aaa` | 
| `secondary`      | `#ae8fdf` |
| `rice-white`      | `#f1faee` |
| `dark`      | `#002d3d` |
| `success`      | `#43d678` |
| `error`      | `#e3282A` |
| `darker-primary`      | `#23307a` |
| `inactive-primary`      | `rgba(71, 90, 170, 0.4)` |
| `inactive-secondary`      | `rgba(122, 86, 201, 0.4)` |
| `inactive-primary`      | `#002d3d` |
| `outline-primary`      | `#1125da` |
| `outline-secondary`      | `#8b69d7` |
| `outline-white`      | `#c4c4c4` |
| `outline-dark`      | `#000000` |
| `outline-success`      | `#a2f0b3` |
| `outline-error`      | `#ff7387` |
| `transparent` | `-` |

These colors extend the built-in colors in tailwind. \
Built-in colors and arbitary color values can also be used. [For more information.](https://tailwindcss.com/docs/customizing-colors)

#### Max Width

```html
    <div class="mx-vw-full mx-vh-full">
        ...
    </div>
```
| Options   | Size (CSS units) | 
| :-------- | :------- |  
| `mx-vw-full` | `100vw` | 
| `mx-vh-full`      | `100vh` |

The only reason that these are here is because to extends the max-width \
option from what tailwind has to offer already. \
Might come in handy.
