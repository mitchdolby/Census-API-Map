# Census-API-Map
## This project is a python script that requests data from the API of the United States Census Bureau, and saves the data on the state, county, tract, and block group level as a .CSV file
## This markdown will show you how to navigate and run the census_api_bg.py script

First, make sure you have the python language and a code editor downloaded. I personally prefer to use anaconda and visual studio code.

After all of the programs and code are properly installed and are in your respective file directory locations, open the code.

In the config.py file, you will need to replace the "INSERT_API_KEY" string with an API key string. You can request a Census API key from the Census Bureau website at census/developers.com. On that page, there is a large button that says "request a key". Click that key, enter your credentials, and you will recieve an email with your API key. Copy and paste that key into the api_key variable in config.py

The script should be ready now. Open your command prompt terminal (anaconda prompt in my case).

In your terminal, you will need to change your directory to the location where the census API code is stored;
the command for this is "cd <your directory path>"
  
At this time the script takes three arguments: state, var, and overwrite, the latter being optional and the first two being positional(required). An optional argument means that you can choose if you want to include the argument or not.
  
Enter in the command terminal "python census_api_bg.py -h" the -h can be substituted with -help, which is the command that will show the list of arguments and what each argument entails. See the screenshot below for the descriptions of each argument.
  
 After learning the arguments, it's time to run the code
  
 In this screenshot, I ran an example of what running the script would look like
