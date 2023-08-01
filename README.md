# Gobble
Extract passwords saved by web browsers.

## Background
When you sign into your favourite web applications, you might be prompted to "save your password" for next time. This action is often taken for the sake of saving precious time since you won't need to supply your password next time you want to login, providing the end user with a smooth browsing experience. 

It might be no secret that these passwords can be seen from within the web browser itself, for example Chrome on Windows allows its users to view their saved passwords by navigating to the chrome://password-manager/passwords endpoint within the browser and entering their local user passphrase. However, this is a step that can be completely bypassed! All the components required to decrypt the passwords are stored on the filesystem waiting to be read.

This project is experimental and serves as a playground for analysing, gathering and discovering stored credentials. The first interation supports Chrome v 115.0.5790.110 on Windows. Support for additional web browsers and operating systems will be supported in later versions. 

## Installation:

**Python Virutal Environment:**
- python -m pip install virtualenv
- git clone https://github.com/Rich-Sec/gobble.git
- cd gobble
- virtualenv --python python venv
- venv\Scripts\activate
- pip install -r requirements
- python gobble.py

## Output:

Website: https://en-gb.facebook.com/ | Username: fakeemail@example.com | Password: thebestpasswordever!
Website: https://www.instagram.com/ | Username: workemail@example.com | Password: my_great_password_123

