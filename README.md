# CCPS610 Flask API

This API acts as a 'middleman' for the front-end portion and the backend database portion of the assignment.

## Requirements

*Base software requirements:*
 - python3 (as well as pip)
 - Oracle Client Libraries (grab the link below) <br>
    https://download.oracle.com/otn_software/nt/instantclient/19600/instantclient-basic-windows.x64-19.6.0.0.0dbru.zip
 - Visual C++ Redistributable (grab the link below) <br>
   https://download.visualstudio.microsoft.com/download/pr/8c211be1-c537-4402-82e7-a8fb5ee05e8a/B6C82087A2C443DB859FDBEAAE7F46244D06C3F2A7F71C35E50358066253DE52/VC_redist.x64.exe



## Usage

1. Clone this repository
2. Install the pip packages: <br>
   ```
   pip install -r requirements.txt
   ```

3. Set up the configuration
   ```
   1. You can either:
      a. set environment variables (remember, these are school credentials):
         ORACLE_USER=my-oracle-username
         ORACLE_PASS=my-oracle-password
      
      b. Go into config.py and set the ORACLE_USER and ORACLE_PASS variables to
         your connection credentials (Note: this is much less secure but OK for
         development purposes)
   ```
4. Set the flask environment
   ```
   # Windows (in a powershell window):
   $env:FLASK_APP="app.py"

   # Linux
   export FLASK_APP=app.py

   # Mac
   Sorry, don't know how to set environment variables in Mac.  Probably a quick google search on that then just set the variable FLASK_APP=app.py
   ```

5. Run the flask app
   ```
   # From the root of the project directory
   flask run
   ```