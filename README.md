# TODO App with Charge Time functionality
## CS-50 Final Project
#### Video Demo:  Hidden
#### Description:

I've managed to create a web application that allows user to create a bunch of tasks and lets them track time spent on each of them.
` Please be aware that this project was uploaded in one commit, because it was prepared using CS50s github workspace`
## Dependencies

```
cs50
Flask
Werkzeug
```

The following app runs the backend using Python Framework called Flask. For frontend basically HTML and CSS is used, and some functionalities to make
website interactive were developed using Vanilla JavaScript. Jinja templates were also very helpful in this project.

After small research I found that CS50 Staff allows to use SQL from cs50 library so I manage my database using that.

Also I used decorator to check that user needs to be logged in, that is similarly developed as this in PSet 9.


### app.py

Starting with main flask app, here I declared some functions with routes to:
* Retrieve main site => stored in manage_tasks.html
* Handle registering and logging a user (with unique email address and password)
* Provide a functionality to add, edit and remove tasks based on user preferences
* Let user charge their time [timer()] => This function receives json data provided by the ajax request so data can be sent without a html form
* Finally user can be logged out and the session disappears

### auth templates

I think going through the auth templates is not necessary, they are just simple forms that can send data to Flask app.
They contain required attribute, but flask handles receiving no input anyway.

### manage_tasks.html

This template works as a main site that user sees after being authenticated.

Here he can start the stopwatch, change the theme, add, edit and remove tasks.

Tasks assigned to user are listed inside a table, and user can manage changing it's content by checking appropriate radio button
`<td><input type="radio" name="task_id" value='{{ task.task_id }}' required></td>`
which contains task id as value.

It is worth adding that for representing time charged on specific tasks I had to create a jinja filter (stored in decorators.py) to represent time as HH:MM:SS (database stores number of seconds as this was the best convention).
`<td id='result'>{{task.charged|format_time}}</td>`

### styles.css

This files manages all of the styles used in my project. I used bootstrap mainly for buttons that matched my project visualization.
I created some additional classes for handling the dark-mode


### main.js
This file stores all of the site functionality (stopwatch and dark-mode)
What I am proud of is adding the `localStorage` that lets me save the stopwatch time and theme after refreshing the page.

### Stopwatch
uses setInterval for it is main functionality, then inside this function I format the data to be presented as HH:MM:SS,
digit function helps me presenting this data with two digits even with current time is presented as for example 8 seconds.

### changeTheme
handles changing the theme for three objects: body, table and main container => that is the convention that made site less boring in my opinion.

Two event listeners at the bottom handle the site refreshing magic, `DOMContentLoaded` reads the data from localStorage and based on that retrieves stopwatch state and sets appropriate theme.

`beforeunload` event sets the stopwatch data when page is about to be unloaded.

I also wanted to add reloading functionality after charging the time, but it started to messing with the cookies, so website needs to be reloaded after this action manually, but since all important states are saved, thanks to localStorage, it is not that huge problem, but worth fixing in the future.

### error_handling.html

Template used for informational purpose when error occurs.

### decorators.py

Stores `login_required` decorator and jinja time filter.


### database.db

sqlite3 database that contains two tables:
* users that stores id - primary key, email, and hashed password
* tasks that stores task_id - primary key, name of a task, charged time presented in seconds (with default value of 0) and user_id => user assigned to this task

