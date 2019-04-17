# data-science
data science repo

![Flask App Build Badge](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiVE02NmNMVHAyb0c4U2UrNTBIM1NLTmloLytMTkFFZlF3bG5iZkxNcWI1a2NvOEpMbHdtcWtwbStINVZNQkhaQzBITlNzbWVSK2VsYS9VK245S0VLQVZFPSIsIml2UGFyYW1ldGVyU3BlYyI6ImhzcisvN0k2ZVJ0a2VKVGciLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

## Development Build

Make sure you're on Python3, use a venv

if in a venv use guide
https://packaging.python.org/guides/installing-using-pip-and-virtualenv/

Run python package manager on requirements.txt to download relevant packages

`pip3 install -r requirements.txt`

set environemt variables for Flask

```
export FLASK_DEBUG=1
export FLASK_ENV=development
export FLASK_APP=app.py
```

```
flask run
```
