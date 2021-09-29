#SoftDesk API: A multi-platform Issue tracking system 
___
SoftDesk is a software development and collaboration compagny. \
SoftDesk API is an application that is aimed at the companies that are customers of SoftDesk. \
SoftDesk API allows users to report and track technical issues on all three platforms (website, Android and IOS applications). \
It allows users to create various projects, add users to projects, create issues within projects and assign labels to these issues.

SoftDesk API uses JWT authentification. So you have to register and login to access all ressources.

## Technologies
___
- python 3.2.9
- Django 3.2.7
- djangorestframework 3.12.4
- djangorestframework-simplejwt 4.8.0

## Installation
___

1. Clone this repository using ```$ git clone https://github.com/dardevetdidier/SoftDeskClass.git```
2. Move to the SoftDeskClass root folder with ```$ cd SoftDeskClass```
3. Create a virtual environment for the project with ```$ py -m venv venv``` on Windows or ```python3 -m venv venv````on macos or linux.
4. Activate the virtual environment with ```$ venv\Scripts\activate``` on Windows or ```$ source venv/bin/activate``` on macos or linux`.
5. Install the project dependancies with ```$ pip install -r requirements.txt```
6. Create and populate the project database with ```$ python manage.py`create_db```
7. Run the server with ```$ python manage.py runserver```

When the server is running, after the step 7 of the procedure, you have to register with :\
https://localhost:8000/signup/ \
and login with : \
https://localhost:8000/login/ \
to obtain access and refresh tokens. \

Once you are logged in, the SoftDesk API can be requested from endpoints starting with the following base URL:
https://localhost:8000/projects/ \

Steps 1-3 and 5-6 are only required for the initial installation. For subsequent launches of the API, you only have to execute steps 4 and 7 from the root folder of the project.

## Usage and detailed endpoints documentation
___

Once you have launched the server, you can read the API documentation by visiting :

AJOUTER LE LIEN DE LA DOC POSTMAN