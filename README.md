# FakeNewsBot

[![FakeNewsBot Banner](https://raw.githubusercontent.com/bondeabhijeet/FakeNewsBot/main/FakeNewsBot.png)](https://github.com/bondeabhijeet/FakeNewsBot)

# Want to deploy this bot yourself?
- Recommended operating system<br>
   ```Linux distribution```
   
- Cloning this repo
  ```
  git clone https://github.com/bondeabhijeet/FakeNewsBot.git
  ```
- Navigating inside the repo
  ```
  cd FakeNewsBot
  ```
- Download the dataset from this link 
https://drive.google.com/file/d/1hns-QpxFzxdKO6SVmm2oHG3y-Aruck20/view?usp=sharing

- Paste the file (train.csv) in the following path
  ```
  ./FakeNewsBot/BotModules
  ```
- ## config.json file
     append all the details in this file according to the fields.
   - **API_KEY** : The token you recieve from [@BotFather](https://telegram.me/BotFather) to access the HTTP API. If you are using environment variable then leave this field to default.
   - **COMMANDS** : All the commands on which the bot will work on.
     + **Help** : The command to get the help message [Default = help].
     + **News** : The command to get the prediction for a news [Default = news].
   - **Deploy** : 
   ``` [0] : to get bot token from config.json file [1] : to get the bot token from the os.environ (environment variable)```


- Run the bot
  ```
  bash RUN_BOT.sh
  ```
  -  _By running this command, all the requirements will be installed on the system (including dependencies). *Details of the installation will be printed on the         screen as well as start the bot_
- Manual installation (if the above method doesn't work)
  - Installing the requirements (linux utilities as well as python libraries)

  ```
  bash requirements.sh
  ```
  _All the requirements details are stored in "./FakeNewsBot/requirements_src" folder_
  - Running the bot

  ```
  python3 main.py
  ```
- Download the report click this link https://github.com/bondeabhijeet/FakeNewsBot/raw/main/FAKE%20NEWS%20DETECTION%20REPORT.docx
