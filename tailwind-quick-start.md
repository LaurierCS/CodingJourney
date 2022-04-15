# Quick Start With Tailwind In Django

## Content Table

- [Quick Start With Tailwind In Django](#quick-start-with-tailwind-in-django)
  - [Content Table](#content-table)
  - [Resources](#resources)
  - [Pre-requisites](#pre-requisites)
  - [Start Development Environment](#start-development-environment)
  - [Build For Production](#build-for-production)
  - [Theme Configuration](#theme-configuration)
      - [Font Family](#font-family)
      - [Colors](#colors)
      - [Max Width](#max-width)
  - [What does each file do?](#what-does-each-file-do)
    - [tailwind.config.js](#tailwindconfigjs)
    - [postcss.config.js](#postcssconfigjs)
    - [package.json and package-lock.json](#packagejson-and-package-lockjson)
    - [node_modules](#node_modules)


## Resources
- [Tailwind Docs](https://tailwindcss.com/docs/)

## Pre-requisites

- Have NodeJS install in your machine. [Download NodeJS](https://nodejs.org/en/download/)
- Install tailwind dependency. \
  Before we can use the power of tailwind, we need to install all the dependencies that tailwind needs to run properly.
  ```bash
  # Navigate to where package.json is located
  $ (Pod4) cd ./static/js/tailwind
  # Install dependencies
  $ (Pod4/static/js/tailwind) npm install
  ```

## Start Development Environment

With 2 shells / terminal windows
```bash
# shell 1
# navigate to the tailwind folder
$ (Pod4) cd ./static/js/tailwind
# start watching changes in html files
$ (Pod4/static/js/tailwind) npm start
```

```bash
# shell 2
# start web server
$ (Pod4) python manage.py runserver
```

## Build For Production
Before deploying our project we need to build a production ready css.

To build a production ready css, we run the following command. Make sure you are in `static/js/tailwind` before running the command.
```bash
# navigate to static/js/tailwind
$ (Pod4) cd static/js/tailwind
# run build command
$ (Pod4/static/js/tailwind) npm run build
# ... building production ready css
```

## Theme Configuration

To edit the theme, read [customize theme](https://tailwindcss.com/docs/theme). Then edit `tailwind.config.js` file located in `app/static_src`.

#### Font Family

As configured in `tailwind.config.js` located in `static/js/tailwind`, the font family has been applied to our entire website. \
There is no need to specify a font family unless there is a need to use a different font family.

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

## What does each file do?

### tailwind.config.js
This file is responsible for our tailwind configuration. It has where our templates are located, our theme, custom css values and plugins.

### postcss.config.js
[PostCSS](https://postcss.org/) is a library that does pre-processing and post-processing of css files. The file is used to set up configuration for each plugin we are using. At the moment, the configurations are empty. \
We are using the [Autoprefixer](https://github.com/postcss/autoprefixer) plugin for PostCSS. The plugin fills in prefixes for some css properties that requires prefixes such as `-webkit-, -moz-, -ms-`.

### package.json and package-lock.json
These two files are the same as Pipfile and Pipfile.lock. However, package.json have some npm commands that makes our life easier when it comes to starting a development environment and building a production ready css.

### node_modules
This is not a file, but a directory. It has all the js dependencies that tailwind needs. This directory should not be deleted or push to github due to how massive it is.