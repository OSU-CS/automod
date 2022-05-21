# Integration Testing with Tokens
The instructions as they stand now were developed with Legacy Slack Tokens, which no longer exist. In order to obtain a slack token, you have to create an app now.

## Set up workspace and app integration
Create a new workspace. Use of the prefix osu-cs-test is encouraged. This can be done from the slack homepage: https://slack.com.
### Create New App
* Go here to create a new app: https://api.slack.com/apps
* Click on `Create New App`
* Click on From an app manifest
* Choose the new workspace you just created for where to develop your app and click `Next`
* Use manifest.yml as an example, request_url will need update later
* Review tabs if desired and click `Create`

This should then take you to your new app's configuration page. You may want to bookmark this page for convenience, but you can also find it again from https://api.slack.com/apps.
### Configure App
Within your app settings:
* Under Basic Information -> Building Apps for Slack -> Install your app
  * Click `Install to Workspace`
  * It will show you an overview of the permissions you're granting. Click `Allow` to proceed with install.
* Under Basic Information -> App Credentials, copy the **Signing Secret** and save it to your environment variables for your dev environment.
```bash
export SLACK_SIGNING_SECRET=somehash
```
Within Features:
* Under OAuth & Permissions -> OAuth Tokens for Your Workspace, copy the **Bot User OAuth Token** and save it to your environment variables for your dev environment.
```bash
export SLACK_BOT_TOKEN=xoxb-some-hash
```
*DO NOT COMMIT YOUR ENVIRONMENT VARIABLES!!* These should be kept in .bashrc or something similar locally.

## Set up slack channels   
* Create required channels: 
  * \#admin (private)
  * \#admin_logs (private)
  * \#emoji_meta
* Add app as an integration in each channel:
   * Click on channel name, then **Integrations** tab
   * Under Apps, click on `Add apps`
   * Find your app under **In your workspace** and click on `Add` next to it
    

## Run and link Automod 
* With environment variables specified, run the application, either locally with ngrok (to get a public url) or with heroku.
* Update your app configuration to your environment's URL.
  * Under Features -> Event Subscriptions -> Enable Events, find Request URL.
  * It will likely say "Your URL didn't respond", this is expected since it's a placeholder URL in the manifest.
  * Update the URL to where your application is hosted but keep the path /slack/events. This is the standard path where events are published by Slack.
  * Click `Retry`. 
  * If it says "Your URL didn't respond with the value of the `challenge` parameter", check your SLACK_SIGNING_SECRET and SLACK_BOT_TOKEN. 
    Highly recommend labeling your environment variables locally if you're going to be working within multiple environments, even if it's just comments between groups of them.
  * Once this is successful, you should be ready to go! Try adding an emoji or channel in your new workspace. :)   