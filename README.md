# webapp
I have build an GET api using Flask. 


Git Commands to clone the repositories:
-  git clone ssh-key   (Organization Repo)

To host the API:
Command to run the python file to host the API in local server:

```code
python GET_API.py
```

Test the below endpoints:

```code
http://127.0.0.1:5000/healthz
```

Built CI pipline and we can check workflow in actions.

Basic auth is implemented in GET and PUT API's-  


Without auth POST API is implemented:
- Encrypted password with Bcrypt with salt

username should be unique and http response is managed for this as well.
If user try to retrieve more impormation than the http response is also managed. 

http responses are managed like: 
- 201, 400, 204, 401, 403



