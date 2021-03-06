# Census-API-Map
## This project is a python script that requests data from the API of the United States Census Bureau, and saves the data on the state, county, tract, and block group level as a .CSV file
## This markdown will show you how to navigate and run the census_api_bg.py script

First, make sure you have the python language and a code editor downloaded. I personally prefer to use anaconda and visual studio code.

After all of the programs and code are properly installed and are in your respective file directory locations, open the code which is in the "scripts" folder of this repo.

In the config.py file, you will need to replace the "INSERT_API_KEY" string with an API key string. You can request a Census API key from the Census Bureau website at census/developers.gov. On that page, there is a large button that says "request a key". Click that key, enter your credentials, and you will recieve an email with your API key. Copy and paste that key into the api_key variable in config.py

![censusapi1](https://github.com/mitchdolby/Census-API-Map/blob/main/pics/censusapi1.PNG)

![censusapi2](https://github.com/mitchdolby/Census-API-Map/blob/main/pics/censusapi2.PNG)

The script should be ready now. Open your command prompt terminal.
  
 ![censusapi3](https://github.com/mitchdolby/Census-API-Map/blob/main/pics/censusapi3.PNG)

In your terminal, you will need to change your directory to the location where the census API code is stored;
the command for this is "cd <your_directory_path>"
   
![censusapi4](https://github.com/mitchdolby/Census-API-Map/blob/main/pics/censusapi4.PNG)
  
At this time the script takes four arguments: state, var, name, and overwrite, the first two being positional (required), and the second two being optional. An optional argument means that you can choose if you want to include it in the argument or not.
  
Enter in the command terminal "python census_api_bg.py -h" (the -h can be substituted with --help) which is the command that will show the list of arguments and what each argument entails. See the screenshot below for the descriptions of each argument.
  
![censusapi5](https://github.com/mitchdolby/Census-API-Map/blob/main/pics/censusapi5.PNG)
  
For --state, you will need to input the two-letter abbreviation of the state of your choosing (i.e. 'VA' for Virginia). It also supports Washington DC ('DC') and Puerto Rico.
  
To find the variables you need, you will have to return to the census/developers.gov website. Under the "Available APIs" tab in the lefthand menu, click on the American Community Survey 5-year Data, and open the html of the variables list from the Detailed Tables. There you will see an exhaustive list of variables and their respective codes that you can choose from. Keep in mind that as of now this script only supports Detailed Tables, so don't choose anything from the Subject Tables, Data Profile, and Comparison Profile.

![censusapi6](https://github.com/mitchdolby/Census-API-Map/blob/main/pics/censusapi6.PNG)

![censusapi7](https://github.com/mitchdolby/Census-API-Map/blob/main/pics/censusapi7.PNG)
  
After learning the arguments, it's time to run the code
  
In this screenshot, I ran an example of what running the script could look like:
  
 ![censusapi8](https://github.com/mitchdolby/Census-API-Map/blob/main/pics/censusapi8.PNG)

If you check your file, the data that you requested should have saved into your directory, and should now be ready for use. It should be saved into a NEW FOLDER called 'states_data'. Here is what the cleaned file should look like:

![censusapi9](https://github.com/mitchdolby/Census-API-Map/blob/main/pics/censusapi9.PNG)

