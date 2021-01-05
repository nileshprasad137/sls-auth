# Serverless-Auth0-Handler

### When to use this?

You want to integrate Auth services (Auth0/Cognito) in your serverless application.
This helps to integrate different Auth flows in OAuth.

## Install required dependences
```
$ sls plugin install -n serverless-python-requirements
$ sls plugin install -n serverless-dotenv-plugin
$ pip install -r requirements.txt
```

Create .env file and add following properties:

```
AUTH0_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxx
AUTH0_DOMAIN=xxxxxxxxxxxx.us.auth0.com
AUTH0_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxx
AUTH0_AUTH_CODE_CALLBACK_URL=https://xxxxxxxxxxxxx.amazonaws.com/dev/callback
TABLE_NAME=auth0-users
```


If you integrated a specific custom domain with the api gateway, then you can use it in the place of **AUTH0_AUTH_CODE_CALLBACK_URL**. In order to get the first api gateway's endpoint, you will need to try deploy even though it doesn't work at the first time.

### Deploy
```
$ sls deploy
```
    
This service uses Authorization Code Flow Grant Type from [Serverless-Auth0-Handler](https://github.com/Venus713/Serverless-Auth0-Handler). I have made minor changes in it to suit my needs and I have also added Implicit Login Grant Type Handler for Auth0.
    
