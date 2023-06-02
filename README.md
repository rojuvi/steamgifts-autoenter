# Steamgifts Autoenter

This is a simple automation based on Selenium to enter giveaways from https://www.steamgifts.com.
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

Create a `.env` file with the following content, replacing the placeholders with your actual credentials:
```
STEAM_USERNAME=<your username>
STEAM_PASSWORD=<your password>
```

And finally run 
```
docker-compose up
```

Alternatively you can manually run the image with:
```
docker run --env STEAM_USERNAME=<your steam user name> --env STEAM_USERNAME=<your steam password> rojuvi/steamgifts-autoenter:latest
```

