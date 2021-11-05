# Kanvas

API developed in Django, for online education system. With it, the user can register people as a student, facilitator and instructor. For each type of person, they will have different forms of access to courses, activities and submissions.

# Clone

Clone this repository on your local machine. 

Use the terminal for this.

```bash
git clone git@gitlab.com:CarlosMartorini/kanvas.git
```

# Installation

Enter the project dependencies and install the virtual environment.

```bash
python -m venv venv
```

Enter the virtual environment

```bash
source venv/bin/activate
```

And now install the dependencies stored in the requirements.txt file

```bash
pip install -r requirements.txt
```
# Usage

Run migrations with the following command so that db.sqlite is created.

```bash
python manage.py migrate
```

Put the local server to run.

```bash
python manage.py runserver
```

Local server URL: http://127.0.0.1:8000/

# Routes

## Create User

- POST api/accounts/
- Status HTTP 201 CREATED

```json
{
  "username": "John",
  "password": "123456",
  "is_superuser": false,
  "is_staff": false
}
```
- Expected response

```json
{
  "id": 1,
  "username": "John",
  "is_superuser": false,
  "is_staff": false
}
```

- If there is an attempt to create a user who is already registered.
- Status HTTP 409 CONFLICT.

```json
{
    "error": "User already exists!"
}
```


## Login

- POST api/login/
- Status HTTP 200 OK

```json
{
  "username": "John",
  "password": "123456"
}
```

- Expected response

```json
{
  "token": "dfd384673e9127213de6116ca33257ce4aa203cf"
}
```

- If you try to give wrong information
- Status HTTP 401 UNAUTHORIZED

```json
{
    "error": "Username or password may be wrong!"
}
```

- If any information is missing
- Status HTTP 406 NOT ACCEPTABLE

```json
{
    "error": "username it's missing"
}
```

## Invalid token

- All endpoints that require the use of an access token must respond as follows if an invalid token is entered
- Status HTTP 401 UNAUTHORIZED

```json
// REQUEST
// Header -> Authorization: Token <invalid-token>
```

```json
{
    "detail": "Invalid token."
}
```

- If a valid token is entered but does not meet the minimum permission requirements
- Status HTTP 403 FORBIDDEN

```json
// REQUEST
// Header -> Authorization: Token <forbidden-token>
```

```json
{
    "detail": "You do not have permission to perform this action."
}
```

## Showing a specific course

- GET api/courses/< int:course_id >/
- Status HTTP 200 OK

```json
[
  {
    "id": 1,
    "name": "Flask",
    "users": [
      {
        "id": 1,
        "username": "John"
      }
    ]
  },
  {
    "id": 2,
    "name": "Django",
    "users": [
      {
        "id": 2,
        "username": "Doe"
      }
    ]
  }
]
```

- If you try to access a non-existent course
- Status HTTP 404 NOT FOUND

```json
{
    "error": "invalid course_id"
}
```

## Create course

- POST api/courses/
- Status HTTP 201 CREATED

```json
{
  "name": "Flask"
}
```

- Expected response

```json
{
  "id": 1,
  "name": "Flask",
  "users": []
}
```

- If course name already exists
- Status HTTP 400 BAD REQUEST

```json
{
    "error": "Course with this name already exists"
}
```

- If any information is missing
- Status HTTP 406 NOT ACCEPTABLE

```json
{
    "error": "name it's missing"
}
```

## Update course

- PUT api/courses/< int:course_id >/
- Status HTTP 200 OK

```json
{
  "name": "Django"
}
```

- Expected response

```json
{
  "id": 1,
  "name": "Django",
  "users": []
}
```

- If you try to update a non-existent course
- Status HTTP 404 NOT FOUND

```json
{
    "error": "Course not founded!"
}
```

- If any information is missing
- Status HTTP 406 NOT ACCEPTABLE

```json
{
    "error": "course it's missing"
}
```

- If course name already exists
- Status HTTP 400 BAD REQUEST

```json
{
    "error": "Course with this name already exists"
}
```

## Include students in courses

- PUT api/courses/< int:course_id >/registrations/
- Status HTTP 200 OK

```json
{
  "user_ids": [1, 2, 3]
}
```

- Expected response

```json
{
  "id": 1,
  "name": "Django",
  "users": [
    {
      "id": 1,
      "username": "John"
    },
    {
      "id": 2,
      "username": "Doe"
    },
    {
      "id": 3,
      "username": "Mark"
    }
  ]
}
```

- If type user_ids is not a list
- Status HTTP 400 BAD REQUEST

```json
{
    "error": "user_ids is not a list"
}
```

- If you try to pass an id that is a facilitator or instructor
- Status HTTP 400 BAD REQUEST

```json
{
    "error": "Only students can be enrolled in the course."
}
```

- If you try to update a non-existent course
- Status HTTP 404 NOT FOUND

```json
{
    "error": "invalid course_id"
}
```

- If you try to pass a user_id that doesn't exist
- Status HTTP 404 NOT FOUND

```json
{
    "error": "invalid user_id list"
}
```

## Showing all courses

- PUT api/courses/< int:course_id >/registrations/
- Status HTTP 200 OK

```json
[
  {
    "id": 1,
    "name": "Django",
    "users": [
      {
        "id": 1,
        "username": "John"
      }
    ]
  },
  {
    "id": 2,
    "name": "Flask",
    "users": [
      {
        "id": 2,
        "username": "Doe"
      }
    ]
  }
]
```

## Delete courses

- PUT api/courses/< int:course_id >/registrations/
- Status HTTP 204 NO CONTENT

- Expected response

```json
// RESPONSE STATUS -> HTTP 204 NO CONTENT
```

- If you try to delete a non-existent course
- Status HTTP 404 NOT FOUND

```json
{
    "error": "Course not founded!"
}
```

## Create activity

- POST api/activities/
- Status HTTP 201 CREATED

```json
{
  "title": "Kenzie Pet",
  "points": 10
}
```

- Expected response

```json
{
    "id": 1,
    "title": "Kenzie Pet",
    "points": 10,
    "submissions": []
}
```

- If you try to create an existent activity
- Status HTTP 400 BAD REQUEST

```json
{
    "error": "Activity with this name already exists"
}
```

## Showing all activities

- GET api/activities/
- Status HTTP 200 OK

```json
[
  {
    "id": 1,
    "title": "Kenzie Pet",
    "points": 10,
    "submissions": [
      {
        "id": 1,
        "grade": 10,
        "repo": "http://gitlab.com/kenzie_pet",
        "user_id": 3,
        "activity_id": 1
      }
    ]
  },
  {
    "id": 2,
    "title": "Kanvas",
    "points": 10,
    "submissions": [
      {
        "id": 2,
        "grade": 8,
        "repo": "http://gitlab.com/kanvas",
        "user_id": 4,
        "activity_id": 2
      }
    ]
  }
]
```

## Update activity

- PUT api/activities/< int:activity_id >/
- Status HTTP 200 OK

```json
{
  "title": "Kenzie Pet",
  "points": 10
}
```

- Expected response

```json
{
  "id": 1,
  "title": "Kenzie Pet",
  "points": 10,
  "submissions": []
}
```

- If you try to update an activity that has a submission
- Status HTTP 400 BAD REQUEST

```json
{
    "error": "You can not change an Activity with submissions"
}
```

- If you try to update an nonexistent activity
- Status HTTP 404 NOT FOUND

```json
{
    "error": "Invalid activity_id"
}
```

- If any information is missing
- Status HTTP 406 NOT ACCEPTABLE

```json
{
    "error": "title it's missing"
}
```

- If the activity already exists
- Status HTTP 406 NOT ACCEPTABLE

```json
{
    "error": "Activity with this name already exists"
}
```

## Activity submission by the student

- PUT api/activities/< int:activity_id >/submissions/
- Status HTTP 201 CREATED

```json
{
  "grade": 10, // Optional
  "repo": "http://gitlab.com/kenzie_pet"
}
```

- Expected response

```json
{
  "id": 7,
  "grade": null,
  "repo": "http://gitlab.com/kenzie_pet",
  "user_id": 3,
  "activity_id": 1
}
```

- If you try to pass an id that is a facilitator or instructor
- Status HTTP 403 FORBIDDEN

```json
{
    "error": "Only students can apply submissions"
}
```

- If you try to apply an nonexistent activity
- Status HTTP 404 NOT FOUND

```json
{
    "error": "Invalid activity_id"
}
```

## Grade edition by facilitator or instructor

- PUT api/activities/< int:activity_id >/submissions/
- Status HTTP 200 OK

```json
{
  "grade": 10
}
```

-Expected response

```json
{
  "id": 3,
  "grade": 10,
  "repo": "http://gitlab.com/kenzie_pet",
  "user_id": 3,
  "activity_id": 1
}
```

- If you try to apply an nonexistent submission
- Status HTTP 404 NOT FOUND

```json
{
    "error": "Invalid submission_id"
}
```

- If any information is missing
- Status HTTP 406 NOT ACCEPTABLE

```json
{
    "error": "grade it's missing"
}
```

## Shows student submissions or all student submissions if facilitator or instructor token exists

- GET api/submissions/
- Status HTTP 200 OK

```json
//REQUEST
//Header -> Authorization: Token <token-student>
```

```json
[
  {
    "id": 2,
    "grade": 8,
    "repo": "http://gitlab.com/kanvas",
    "user_id": 4,
    "activity_id": 2
  },
  {
    "id": 5,
    "grade": null,
    "repo": "http://gitlab.com/kmdb2",
    "user_id": 4,
    "activity_id": 1
  }
]
```

```json
//REQUEST
//Header -> Authorization: Token <token-facilitator or token-instructor>
```

```json
[
    {
        "id": 1,
        "grade": 10,
        "repo": "http://gitlab.com/kenzie_pet",
        "user_id": 3,
        "activity_id": 1
    },
    {
        "id": 2,
        "grade": 8,
        "repo": "http://gitlab.com/kanvas",
        "user_id": 4,
        "activity_id": 2
    },
    {
        "id": 3,
        "grade": 4,
        "repo": "http://gitlab.com/kmdb",
        "user_id": 5,
        "activity_id": 3
    },
    {
        "id": 4,
        "grade": null,
        "repo": "http://gitlab.com/kmdb2",
        "user_id": 5,
        "activity_id": 3
    }
]
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

```bash
python manage.py test -v 2 &> report.txt
```

# Thank's!

## License
[MIT](https://choosealicense.com/licenses/mit/)
