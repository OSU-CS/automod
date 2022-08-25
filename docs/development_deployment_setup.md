# Deployment of Your Development Environment
Get your local code running and exposed to the world! Both of these options have their pros/cons, but Heroku will allow you to run with just a code editor and git locally.
## ngrok
Create an account if you do not already have one: https://ngrok.com/
Install and set up ngrok: https://dashboard.ngrok.com/get-started/setup
To expose port 3000:
```bash
ngrok http 3000
```
You can also use an environment variable to change the port:
```bash
export PORT=50000
ngrok http $PORT
```
Update your Slack app configuration to the URL ngrok provides. It should look something like:
```bash
Forwarding              http://d61a-2600-1700.ngrok.io -> http://localhost:50000
```
From this the request url would be: http://d61a-2600-1700.ngrok.io/slack/events

## Heroku
Heroku specific configuration files:
* `runtime.txt` - this specifies the version of Python
* `Procfile` - this declares what is run, `process type: command`

Environment variables:
* `$PORT` - this is required as it runs dynamically

### Getting started
Create an account if you do not already have one: https://www.heroku.com

### Create app
* On the dashboard (https://dashboard.heroku.com) click`New` -> Create new app.
* Choose whatever name you wish, this will be the domain. (such as https://name.herokuapp.com)
* Click `Create app`
* Add ths app to a pipeline: N/A
* Deployment method: Heroku Git
* Follow the instructions to set up the Heroku CLI locally.
### Configuration
Set environment variables. This can be done in the UI or via Heroku CLI.
```bash
heroku config:set SLACK_BOT_TOKEN=xoxb-some-hash

heroku config:set SLACK_SIGNING_SECRET=somehash
```
### Build
```bash
git push heroku local_branch:main
```
### Scaling up to run
As soon as it recognizes your Procfile you should be able to scale up web in the UI, but it can be done via Heroku CLI as well.
```bash
heroku ps:scale web=1
```
You should not have to do this again for subsequent deployments.

### Deploying changes to existing environment
Force is optional, but likely to be needed if you're switching back and forth between branches.
```bash
git push heroku local_branch:main --force
```
