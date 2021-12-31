# Python_Simple_Dev_Env
This is a example project for setting up a simple development environment for python. 
The project includes the following topics:
- Spinning up a local flask server
- Connecting a local SQL DB
- Connecting a local redis cache
- HTTP client request 
- UnitTest Framework

## Install Flask App
```
pip install Flask
```

## Install sqlite3 as SQL DB
```
pip install pysqlite3
```

## Install python redis
```
pip install redis
```

## How to start Project
1. Start Redis Server
```
redis-server
```
2. Start Python Flask Server
```
python server.py
```
3. Use your own client or PostMan to interact with python server

## How to run Unit Test
Under Python_Simple_Dev_Env directory, run
```
python -m pytest
```
