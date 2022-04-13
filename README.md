# Quick Start With Tailwind In Django

# Pre-requisites

## - Have NodeJS install in your machine. [Download NodeJS](https://nodejs.org/en/download/)

# Before running server
Run the following commands

`pipenv install` to install all the new packages needed.

`python manage.py tailwind install` to install tailwind and other npm packages.

# Run Development Server
First we need to build our css and have a hot reload to make our lives easier.\
We will need to terminals because one is for building the css and another for the web server.\
In vscode, you can open two terminals side by side by clicking on the split icon located to the left of the trash icon.\
`python manage.py tailwind start` to watch changes in our css files, hot reload.\
`python manage.py runserver` to start development server.