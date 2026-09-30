# Spopple Sync
***
### Don't you hate how apple home doesnt natively support spotify? Not anymore!!

## About
***
Spopple Sync bridges the gap between spotify and apple home by autonomously syncing your spotify playlists with a streaming service Apple Home does support (currently only YouTube Music).

Spopple Sync is meant to be run via a docker image, and can currently only support 1 playlist per container.

## Installation: Docker
***
#### Step 1: clone the repo
```bash
git clone https://github.com/duncan-mal/spopple-sync.git
```

#### Step 2: CD into repo
```bash
cd spopple-sync
```

#### Step 3: Run compose File
```bash
docker compose up -d -build
```
this will create a new directory `./app` which will contain logs and the config file

#### Step 4: Edit config file with needed values
```bash
vim app/config.ini
```
follow the [Wiki Page](https://github.com/duncan-mal/spopple-sync/wiki/Config-Values) explaining each value and where to get them
#### Step 5: Restart docker container
```bash
docker compose start
```

from here on it should now be syncing your playlist from Spotify to YouTube music


## Installation: Dockerless
#### Step 1: clone the repo
```bash
git clone https://github.com/duncan-mal/spopple-sync.git
```

#### Step 2: CD into repo
```bash
cd spopple-sync
```

#### Step 3: run for initial setup
```bash
python main.py
```

#### Step 4: Edit config file with needed values
```bash
vim app/config.ini
```
follow the [Wiki Page](https://github.com/duncan-mal/spopple-sync/wiki/Config-Values) explaining each value and where to get them
#### Step 5: Run Application
```bash
python main.py
```