AutoMod
=======


### To run locally:
* Clone this repository
    ```bash
    git clone git@github.com:OSU-CS/automod.git
    ```
* Install python3.7 and pip
* Create base venv (virtual environment)
    ```bash
    pip install virtualenv
    virtualenv -p `which python3.7` venv
    ```
* Activate venv
    ```bash
    source venv/bin/activate
    ```
* Rebuild venv with dependencies
    ```bash
    pip install -Ur requirements.txt
    ```
  * The app runs on port 3000 by default. You can also override the port it runs on by running
    ```bash
    export PORT=50000
    ```
* Run app (after activating venv). API key should be the "Bot User OAuth Token" under the Oauth &
  Permissions tab and signing secret should be the "Signing Secret" under the Basic Information tab.
    ```bash
    export SLACK_BOT_TOKEN=<app_bot_user_oath_token>
    export SLACK_SIGNING_SECRET=<app_signing_secret>
    python app.py
    ```

Alternatively, most of these steps are set up in the makefile. For more info on how to use a makefile, read [this](docs/about_makefiles.md).
## Contributing

### 1. Submitting an Issue

Before submitting a PR please submit an issue that accurately describes the feature you are requesting or bug you'd like to fix. If one exists, skip ahead to "Submitting a Pull Request". When you are writing an issue, please include as many details as possible. Fill in the template provided for either a bug fix or a feature request.

### 2. Submitting a Pull Request

1. Pick a descriptive name for your branch (this README update was done on `contribution-guide`).
    ```bash
    git checkout -b your-branch-name
    ```
1. Add all the commits related to this change.
1. Push your changes
    ```bash
    git push --set-upstream origin your-branch-name
    ```
1. Navigate to https://github.com/OSU-CS/automod/pull/new/your-branch-name
1. Fill out the information requested in the template
1. Press submit, tag with any relevant labels, and ensure all tests pass before requesting a review
1. Once your PR passes reviews, hit the "Squash and merge" button

### 3. Reviewing a Pull Request

1. Checkout the branch you will be reviewing
1. Run the app locally and test changes in the [integration testing workspace](https://app.slack.com/client/TP02CBTQV/CP02CC0SZ)
    ```bash
    SLACK_BOT_TOKEN=<integration_testing_api_key>
    export SLACK_BOT_TOKEN
    python app.py
    ```
1. Add comments or suggestions
1. Ensure all of the acceptance criteria are hit, manual testing succeeds, and all linting and tests pass before approving
1. Notify the PR author that their PR is approved to let them merge into master

_NOTE: We deploy from master, so do not merge anything that has not been thoroughly tested._

### 4. Testing After Merging

1. After merging an approved PR, deploy master to our [integration testing instance](https://dashboard.heroku.com/apps/osuautomodint/deploy/github)
1. Run all tests again in our [integration testing workspace - osu-cs-int.slack.com](https://app.slack.com/client/TP02CBTQV/CP02CC0SZ) and confirm nothing has broken and all acceptance criteria has been met

### 5. Deploying to Production

1. After testing thoroughly, deploy master to our [production instance](https://dashboard.heroku.com/apps/osuautomod/deploy/github)
1. Pray the above steps were enough to not break the real slack workspace
