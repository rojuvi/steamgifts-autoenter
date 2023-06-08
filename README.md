# Steamgifts Autoenter
[![Docker Image CI](https://github.com/rojuvi/steamgifts-autoenter/actions/workflows/docker-image.yml/badge.svg)](https://github.com/rojuvi/steamgifts-autoenter/actions/workflows/docker-image.yml)

This is a simple automation built with Selenium to enter giveaways from https://www.steamgifts.com.
It will try to enter all giveaways until you run out of points from wishlist, DLCs and recommended in that order.

## Requirements
* python 3.11
* docker
* Mozilla Firefox (for local run)

## How to use
### Local
To run locally you can run: 
```
make run
```

### Docker
To build the docker image run: 
```
make build
``` 
or 
```
docker pull rojuvi/steamgifts-autoenter:latest
```

Create a `.env` file with the following content, replacing the placeholders with your actual credentials and desired configuration:
```
STEAM_USERNAME=<your username>
STEAM_PASSWORD=<your password>
BLACKLIST="<a comma separated list of game titles>"
```
You can find the format of the game titles as they should be set in your BLACKLIST variable in the steamgifts giveaway url. For example, if you would like to avoid entering giveaways for The Lord of the Rings: Gollum - Precious Edition and ET: The Game, you could check the urls, that would look something like https://www.steamgifts.com/giveaway/7LOA4/the-lord-of-the-rings-gollum-precious-edition and https://www.steamgifts.com/giveaway/7LOA4/et-the-game, and take the last part of the url, then set your BLACKLIST variable to `the-lord-of-the-rings-gollum-precious-edition,et-the-game`

And finally run 
```
docker-compose up
```

Alternatively you can manually run the image with:
```
docker run --env STEAM_USERNAME=<your steam user name> --env STEAM_USERNAME=<your steam password> rojuvi/steamgifts-autoenter:latest
```

### HomeAssistant - AppDaemon

If you are like me and you like automating everything you will have a HomeAssistant brain running your home (and if you don't, you should).
In that case, the easiest way to add this automation is through the AppDaemon addon.
You just have to follow the following steps:

1. Install the AppDaemon addon. Just go to your `Settings -> Addons -> Addons Store` and search for AppDaemon and install it
2. You will need to add some dependencies for this automation to run. 

    a. Navigate to `Settings -> Addons` and find the newly added AppDaemon addon

    b. Open the addon settings

    c. Add the following to system_packages: `chromium-chromedriver`, `chromium`

    d. Add the following to python_packages: `selenium`

    The end result in yml format should be something like this:
    ```
    system_packages:
        - chromium-chromedriver
        - chromium
    python_packages:
        - selenium
    init_commands: []
    ```
3. Restart the addon
4. Use the file editor to edit to config/secrets.yaml (create if it doesn't exist)
5. Add a steam_user and steam_pass to the secrets.yaml file with your credetntials. It should be something like this:
    ```
    steam_user: yourUsername
    steam_pass: yourPassword
    ```
6. Use the file editor to navigate to config/appdaemon/apps
7. Upload the src/steamgifts_autoenter.py and appdaemon/steamgifts_autoenter_app.py files there
8. Copy the content of the appdaemon/apps.yml from this repo to the apps.yml file in your HomeAssistant
9. Now you can go back to `Settings -> Addons` and open the logs for the AppDaemon addon. It should show a bunch of lines like this:
    ```
    2023-06-08 15:38:41.988856 INFO AppDaemon: Calling initialize() for steamgifts-autoenter
    2023-06-08 15:38:41.998147 INFO steamgifts-autoenter: Listening for event steamgifts-autoenter-run
    2023-06-08 15:38:42.002154 INFO steamgifts-autoenter: Scheduling run at 00:00:00
    2023-06-08 15:38:42.008841 INFO steamgifts-autoenter: Scheduling run at 06:00:00
    2023-06-08 15:38:42.014771 INFO steamgifts-autoenter: Scheduling run at 12:00:00
    2023-06-08 15:38:42.021155 INFO steamgifts-autoenter: Scheduling run at 18:00:00
    ```

That's it! It should run periodically on the defined schedule. You can modify it by editing the scheduled_run property in the apps.yml file

You can also launch the `steamgifts-autoenter-run` event to make the automation to run on demand.