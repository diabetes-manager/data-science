# data-science

![Flask App Build Badge](https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiVE02NmNMVHAyb0c4U2UrNTBIM1NLTmloLytMTkFFZlF3bG5iZkxNcWI1a2NvOEpMbHdtcWtwbStINVZNQkhaQzBITlNzbWVSK2VsYS9VK245S0VLQVZFPSIsIml2UGFyYW1ldGVyU3BlYyI6ImhzcisvN0k2ZVJ0a2VKVGciLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

## Development Build

In the root of this repo, create  virtual environment ([guide](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/))
```
python -m virtualenv venv
```
Activate the environment (Windows method)
```
venv\Scripts\activate
```
Install requirements
```
pip install -r requirements.txt
```

Create a `.env` in the root directory of this repo with the following info. This file **is not version controlled**. This is where we place secret credentials.
```
FLASK_APP=diabetesmanager:APP
FLASK_ENV="development"
FLASK_DEBUG=True
```

Run the server in development
```
flask run
```
