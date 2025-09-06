# healthcare-backend

This is the solution for the WhatBytes assignment. 
It is a backend for a hospital management system built with Django, DRF, and PostgreSQL as the database. It uses JWT-based Authentication. Use an API client like cURL or Postman or RestFox

## Test coverage
- Wrote test cases for Auth, Patients, and Doctor endpoints. With 15+ testcases. 
- Coverage report

```bash
Name                                                                              Stmts   Miss  Cover
-----------------------------------------------------------------------------------------------------
hospital/__init__.py                                                                  0      0   100%
hospital/admin.py                                                                     1      0   100%
hospital/apps.py                                                                      4      0   100%
hospital/migrations/0001_initial.py                                                   8      0   100%
hospital/migrations/0002_alter_patientdoctormapping_unique_together_and_more.py       6      0   100%
hospital/migrations/0003_alter_patient_created_by.py                                  6      0   100%
hospital/migrations/__init__.py                                                       0      0   100%
hospital/models.py                                                                   32      3    91%
hospital/serializers.py                                                              57      0   100%
hospital/tests.py                                                                   105      0   100%
hospital/urls.py                                                                      4      0   100%
hospital/views.py                                                                   110     36    67%
-----------------------------------------------------------------------------------------------------
TOTAL                                                                               333     39    88%
```

## Features:
- Endpoint for patients
- Endpoints for doctors
- Endpoints for authentication
- Endpoints for Patient-Doctor Mappings


### Setup instructions:
- Create a virtual environment and activate it
- Install all the dependencies in the requirements
- Install postgresql and create a database called "healthcare_db"
- Create a .env file and fill in the following credentials:
```bash
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_NAME=healthcare_db
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```
- Apply migrations
- Run the test cases
```json
coverage run --source='hospital' manage.py test
```
- Run the server

### API endpoints:

#### Authentication: 

1. POST ```/api/auth/register/```
- Create a user account
- Body example:
```json
{
    "username": "admin",
    "email": "admin@gmail.com",
    "password": "strongpassword"
}
```
- The response should include id, username, and email of the created user. Password is not included for obvious reasons. Remember, username is unique.

2. POST ```/api/auth/login/```
- Log in to get access token
```json
{
    "username": "admin",
    "password": "strongpassword"
}
```

#### Patient:

1. GET ```/api/patients/``` (Auth)
- This is a protected route, so you need the Auth header. Send in ```Bearer your_token_here```
- The response is a list of patients:
```json
[
    {
        "firstname": "Syed",
        "lastname": "Mehdi",
        "age": 21,
        "gender": "M",
        "created_by": 1
    },
    ...
]
```
- ```created_by``` is a foreign key pointing to authenticated user


2. POST ```/api/patients/``` (Auth)
- Requires Auth
- Body example:
```json
{
    "firstname": "Syed",
    "lastname": "Mehdi",
    "age": 21,
    "gender": "M",
    "email": "syedmehdi@gmail.com"
}
```


3. GET ```/api/patients/1/```
- Returns a single patient if found, else returns a 404 error


4. PUT ```/api/patients/1/``` 
- email, firstname, lastname and age can be updated. If the patient isn't found, 404 error is returned


5. DELETE ```/api/patients/1/``` 
- Deletes the patient if it exists, else 404 Not Found error

#### Doctors:
The same applies to all the doctors endpoints.
- POST ```/api/doctors/``` requires authentication


#### Patient Doctor Mappings:
1. POST ```/api/mappings/ ```
- Assigning a doctor to a patient
- Requires doctor's and patient's ID
- Body example:
```json
{
    "patient": 3,
    "doctor": 2
}
```
- Doctor with ID of 2, is assigned to patient with ID 3

2. GET ```/api/mappings/``` 
- Retrieves a list of all the mappings
- Response:
```json
[
    {
        "id": 1,
        "patient": {
            "firstname": "John",
            "lastname": "Doe",
            "age": 28,
            "gender": "M",
            "created_by": 1
        },
        "doctor": {"firstname": "Dr. Jane","lastname": "Doe",...},
        "assigned_at": "2025-09-06T09:45:06.922295Z"
    },
    {
        "id": 2,
        "patient": {
            "firstname": "Bruce",
            "lastname": "Wayne",
            "age": 33,
            "gender": "M",
            "created_by": 1
        },
        "doctor": {"firstname": "Jackie", "lastname": "Stewart",...},
        "assigned_at": "2025-09-06T09:45:12.144187Z"
    },
    ...
]
```
- Each mapping contains the patient data, and the doctor(or a list of docs if more than 1) assigned to him/her


3. GET ```/api/mappings/<patient_id>/```
- Retrieves all the doctors assigned for a patient
- Response:
```json
{
    "patient": "Syed Mehdi",
    "doctors": [
        {
            "firstname": "Dr. John",
            "lastname": "Doe",
            "specialization": "DERM",
            "max_appointments_per_day": 10,
            "gender": "M"
        },
        {
            "firstname": "Erling",
            "lastname": "Haaland",
            "specialization": "CARD",
            "max_appointments_per_day": 10,
            "gender": "M"
        }
    ]
}
```

- The patient `Syed Mehdi` has two doctors assigned to him

4. DELETE ```/api/mappings/<id>/delete```
- Removes a mapping if exists