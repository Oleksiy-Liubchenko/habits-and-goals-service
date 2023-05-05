# Goals and Habits tracker ![favicon-16x16.png](static%2Fimages%2Ffavicon-16x16.png)
> TODO killer 😄

Every day is made up of tasks and habits. So why not control them to make life more efficient?

The project helps to set tasks and goals and monitor their implementation.
It is a Django-based project, that is visualised into a site. On this site, you can create goals, assign them sub-goals for detailing, filter by progress status, and track progress.

You can create a habit and the tracker will help you see the progress and how many days the habit has been completed.

Also, you can write comments for both goals and habits.
For convenience, a search by habit name and goal, respectively, has been added.
You can create, update and delete goals, sub-goals and habits.
## Take a quick peek

[Site deployed to Render](https://habits-ang-goals-service.onrender.com/)

- Login: `test_user`
- Password: `test_user123`

## Installation

1. Copy this repository, by using your terminal:
```git
git clone https://github.com/Oleksiy-Liubchenko/habits-and-goals-service.git
```
2. Change directory to main project folder. Use this command:
```git
cd students-task-manager
```
3. Install venv, and activate it by using following commands:
```git
python3 -m venv myvenv
```
to activate on Windows:
```git
myvenv\Scripts\activate
```
to activate on Unix or Linux:
```git
source myvenv/bin/activate
```
4. Install dependencies (requirements):
```git
pip install -r requirements.txt
```
5. Run migrations to initialize database. Use this command:
```git
python manage.py migrate
```
6. Run the server of app
```git
python manage.py runserver
```
7. All is set, now you can use the site! Use this credentials to login:
  - Login: `12345678`
  - Password: `12345678`


Inside the main folder, there is a file called .env_sample which contains an example 
of the SECRET_KEY needed for the project. To proceed, you should create a new file
called .env and enter your own secret key following the example provided.

## Contributing

If you want to help improve the project, please fork the repository and create a new branch specifically
for the feature or change you want to make. When you're done, submit a pull request, so I can review
your changes and merge them into the main repository. I would be happy to accept your contributions!

## Usage
To utilize this site, it is essential to have an account. Therefore, please ensure that you log in upon visiting the main page!

Navigating this site is relatively straightforward. Once you launch the site, you will land on the main page, 
which will allow you to access any other page you need. From there, you can simply follow the links and buttons
to proceed with your desired actions.