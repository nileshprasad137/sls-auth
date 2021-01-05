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
## Test for the Serverless-Auth0-Handler API
1. Login to Auth0.
2. Set up an app in the Auth0 Dashboard.
    You can set up the following app types:
    - Register a Regular Web Application
    - Register a Native Application
    - Register a Single-Page Application
    - Register a Machine-to-Machine Application
    #### Example;
    - You can set up the Regular Web Application to use python app. You can follow this url: https://auth0.com/docs/quickstart/webapp/python?framed=1&sq=1#configure-auth0.
3. Configure Auth0
    - Download Sample Code
    - Get your Application Keys: Domain, CleintID, ClientSecret
    - Configure Callback URLs: Whitelist the API gateway's endpoint you got from deploying of the Serverless-Auth0-Handler  in the Allowed Callback URLs field in your Application Settings to check the endpoint of the API.
    If you need to redirect customers to a spcific url, then you will need to set the Callback URL to the specific url.
    - Configure social connections you want to use in Connections/Social in Auth0 Dashboard.
    - Run the sample code you downloaded according as the README.md of the sample code. Then you can sign up or sing in, then you will be seen the result(user_profile info) in the Callback URL.
    
This service uses Authorization Code Flow Grant Type from [Serverless-Auth0-Handler](https://github.com/Venus713/Serverless-Auth0-Handler). I have made minor changes in it to suit my needs and I have also added Implicit Login Grant Type Handler for Auth0.
    