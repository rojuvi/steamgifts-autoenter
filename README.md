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

### Dockergit 
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
You can find the format of the game titles as they should be set in your BLACKLIST variable in the steamgifts giveaway url. For example, if you would like to avoid entering giveaways for The Lord of the Rings: Gollum - Precious Edition and ET: The Game, you could check the urls, that would look something like https://www.steamgifts.com/giveaway/7LOA4/the-lord-of-the-rings-gollum-precious-edition and https://www.steamgifts.com/giveaway/7LOA4/et-the-game, and take the last part of the url, then set your BLACKLIST variable to "the-lord-of-the-rings-gollum-precious-edition,et-the-game"

And finally run 
```
docker-compose up
```

Alternatively you can manually run the image with:
```
docker run --env STEAM_USERNAME=<your steam user name> --env STEAM_USERNAME=<your steam password> rojuvi/steamgifts-autoenter:latest
```

