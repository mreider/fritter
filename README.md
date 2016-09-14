## What is Fritter?

The goal of Fritter is to help Product Managers prioritize their backlog. Product Managers use fritter to conduct user surveys to answer the question "Which features are most important to you?"

You can see a demo of Fritter [here](http://frittata.cfapps.io/).

## How are Fritter surveys unique?

Fritter Surveys force respondants to consider the scope of a feature. Everyone gets a certain amount of money, say $400, and each feature costs something. Respondants can choose many small features, or one big feature, but not both.

## Why force respondants into considering scope?

Because you, as a PM, prioritize things based on Scope.

## How do I create a survey?

1.  Compile a list of feature requests that you have not prioritized
2.  Ask your engineering lead to help you size each feature in terms of XS, S, M, L, and XL
3.  Create a YAML file, based on the example [here](https://github.com/mreider/fritter/blob/master/yamls/survey2.yml)
4.  Upload the YAML file via the /loadyaml page and send an email to your users to complete the Survey.

## How did you come up with the increments of $?

I wanted the survey to give enough $ for users to buy features for about one release cycle. The XL stories felt like they would take about that long. It also felt like you could do about 40 XS stories for a release cycle. Sure, complexity is different than time, we know that. These are best guesses, and it's not scientific.

## How do you delete / modify the surveys, users and responses?

This application was built in only 2 days. It's not very full featured. If you want to modify surveys, users, and responses, you can use SQL.

## How Do I install Fritter on Cloud Foundry?

Download this git repo

```
git clone git@github.com:mreider/fritter.git
```

CD into the director

```
cd fritter
```

Modify line 20 to change the domains limited into your app

```
vim mrsurvey/config/app_config.py
```

Login to Cloud Foundry

```
cf login
```

Deploy Fritter without starting it

```
cf deploy my-app224 --nostart
```

Create a MySQL instance

```
cf create-service cleardb boost mydb
```

Bind the service to your instance

```
cf bind-service my-app224 mydb
```

Set some environment variables (see below for how to generate these)

```
cf set-env my-app224 GOOGLE_CONSUMER_KEY xxxxxxxxxxxxxxxxxx.apps.googleusercontent.com
cf set-env my-app224 GOOGLE_CONSUMER_SECRET xxxxxxxxxxxxxxxxxxxxxx
cf set-env platform cf
```

Create the tables you need by logging into your db instance and running the create script [here](https://github.com/mreider/fritter/blob/master/db_scripts/00-create-schema.sql)

Start your app

```
cf start my-app224
```

## How Do I install Fritter on Heroku?

Do the same as above, but change the platform variable to 'heroku'


## How Do I generate google oauth keys?

Visit [Google's API Console](https://console.developers.google.com) and create a project.

Go to the "Library" and search for an API matching "survey". Select "Consumer Surveys API".

Go to "Credentials" and create a credential for the survey API. You'll want to select "User data" access, and access "From a web server".

For restrictions, here's what worked for me (YMMV):

Javascript origins:

  * https://appname.cfapps.io/
  * http://appname.cfapps.io/

Redirect URIs:

  * https://appname.cfapps.io/authorized
  * http://appname.cfapps.io/authorized
