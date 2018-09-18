[![Build Status](https://travis-ci.org/jillo-abdullahi/stackoverflow-lite-challenge3.svg?branch=develop)](https://travis-ci.org/jillo-abdullahi/stackoverflow-lite-challenge3)
[![Coverage Status](https://coveralls.io/repos/github/jillo-abdullahi/stackoverflow-lite-challenge3/badge.svg?branch=develop)](https://coveralls.io/github/jillo-abdullahi/stackoverflow-lite-challenge3?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/1bfaa35c80afbd62e838/maintainability)](https://codeclimate.com/github/jillo-abdullahi/stackoverflow-lite-challenge3/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4b24587a09db4a66b9ac27ef59d831ad)](https://www.codacy.com/app/jillo-abdullahi/stackoverflow-lite-challenge3?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jillo-abdullahi/stackoverflow-lite-challenge3&amp;utm_campaign=Badge_Grade)

# stackoverflow-lite-challenge3
This is the third installment of stackoverflow-lite, a platform where people can ask questions and provide answers.

## Documentation

**EndPoint** | **Functionality**
--- | ---
POST `/auth/signup` | Register a user.
POST `/auth/login` | Login a user.
POST  `/questions` | Post a question.
POST `/questions/<questionId>/answers`| Post an answer to a question.
GET `/questions`| Fetch all questions.
GET `/questions/<questionId>`| Fetch a specific question.
PUT `/questions/<questionId>/answers/<answerId>`| Mark an answer as accepted or update an answer.
DELETE `/questions/<questionId>` | Delete a question.

## Setup

Use this guide to get this project up and running:

### Dependencies

1. [python 3.x](https://www.python.org/downloads/)
2. [Git](https://git-scm.com)
3. Working browser or [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?utm_source=chrome-app-launcher-info-dialog)
4. [virtualenv](http://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv) for an isolated working environment.&nbsp;

### Getting started

| **Instruction** | **Command** |
| --- | --- |
| 1. Clone the repo into a folder of your choice | `git clone --depth=50 https://github.com/jillo-abdullahi/stackoverflow-lite-challenge3.git` |
| 2. Navigate to the cloned folder | `cd stackoverflow-lite-challenge3`|
| 3. Create a virtual environment |`virtualenv venv` |
| 4. Activate the virtual environment you just created | `source venv/bin/activate` |
| 5. Install all dependencies into your virtual environment | `pip install -r requirements.txt` |
| 6. Confirm you have all packages installed | `pip freeze` |
| 7. Set environment variables for `APP_SETTINGS` | `export APP_SETTINGS="development"` |
| 8. Set the entry point for the app | `export FLASK_APP="run.py"` |

### Run the service

Get the app running by typing
`flask run`

## Testing

To run all tests type
`nosetests --with-coverage --cover-package=app`

#### Api documentation
[API documentation at Apiary](https://stackoverflowlite19.docs.apiary.io/#)
