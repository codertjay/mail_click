### Click Froward Mail

This is a script that checks a user email and click on the formail verify button every 10 seconds,

It just meant for verification process and created with `selenium` for clicking on the button and `imaplib` to get list
of all
unseen and seen mails from the user account

#### Setup

`python -m venv venv `

Mac
`source venv/bin/actiate`

Windows  `venv\Scripts\activate`

### Install requirements

`pip install -r  requirements.txt`

Update your `.env` using the `.env-sample` provided

Also the `check_script.sh` checks every 30 minutes and rerun the script if the server turns it off 
