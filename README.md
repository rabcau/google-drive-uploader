# Google Drive Uploader

## INTRO

The script's purpose is to upload the contents of specified dir to an appropriate folder.

## SETUP

### Google Cloud Project

#### Create a project

To interact with Google Drive programmatically you should have a Google Cloud project.
Visit [create a project](https://console.cloud.google.com/projectcreate) in Google Cloud
Console, specify the project name, and push **Create** button.

![pic1](docs/001-create-google-cloud-project.png)

#### Enable Google Drive API

After the project creation you should activate Google Drive API for you project. Visit
[api's library](https://console.cloud.google.com/apis/library) page, click on Google
Drive API and **ENABLE** the API.

![pic10](docs/010-drive-api.png)

#### Create access credentials

Visit you project [credentials](https://console.cloud.google.com/apis/credentials) page
to create access credentials. First you should configure **Consent Screen**.

![pic2](docs/002-configure-consent-screen.png)

Pick an external user type as shown in the picture below and click on **CREATE** button:

![pic3](docs/003-user-type.png)

Specify the app name, the user support email, and developer contact. Then click on
**SAVE AND CONTINUE** button.

![pic4](docs/004-app-info-01.png)
![pic5](docs/005-app-info-02.png)

Do not change anything at the Scopes step (2), then specify the test users on the
third step:

![pic6](docs/006-app-info-03.png)

Save the changes, review the settings at the Summary step, then go back to the
[credentials](https://console.cloud.google.com/apis/credentials) page. Click on the
**CREATE CREDENTIALS** button and specify the **OAuth client ID** option:

![pic7](docs/007-create-credentials.png)

Choose the **Desktop** application type, then specify the client ID name, 
and push the **CREATE** button:

![pic8](docs/008-create-oauth.png)

After client creation you will see the **OAuth client created** window. Click on
**DOWNLOAD JSON** button to save the credentials as a json file. Specify the name
as `client_secrets.json` and save the file in the project root.

#### Avoiding the browser auth

To avoid the authentication process at each script run create the `setting.yaml` file,
copy the content of code snippet below, and specify your project client_id and
client_secret. You can take it from `client_secrets.json`.

```yaml
client_config_backend: file
client_config:
    client_id: "<client_id>"
    client_secret: "<client_secret"

save_credentials: True
save_credentials_backend: file
save_credentials_file: credentials.json

get_refresh_token: True

oauth_scope:
    - https://www.googleapis.com/auth/drive
    - https://www.googleapis.com/auth/drive.install
```

Then run the script. You will have to authenticate via browser one time.
After authentication the `credentials.json` will be saved in the project
root.