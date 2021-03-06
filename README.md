# Ride My Way Bot

[![Codeship Status for BolajiOlajide/rmw-bot](https://app.codeship.com/projects/2cb88090-604d-0136-6722-766075984356/status?branch=develop)](https://app.codeship.com/projects/296252)

This repository contains the source code for the ride-my-way slack application that can be used to hook drivers and riders heading to the same destination together.

## Installation

Installation has been automated by the script `setup.sh` contained in the root of the project.
You can choose one of two ways to do installation listed below.

### AUTOMATIC

This leverages the shell script provided. To run it just run the command below from the command line:

```bash
./setup.sh fresh
```

Ensure the following is installed:

* Pipenv
* Pip
* Python3.6+

### MANUAL

* this project uses [pipenv](https://docs.pipenv.org/en/latest/) for managing dependency. Ensure `pipenv` is installed. You can confirm this by checking the version installed on your PC with the command

```bash
pipenv --version
```

if it's not installed you can install with the command

```bash
pip install python
```

if installed, create a python3.6 virtual environment with the command

```bash
pipenv --python=python3.6 shell
```

* install the application's dependencies with the command `pipenv install`

* make a copy of the `.env.example` file named `.env` and populate with your development details

* run migrations on the DB by running the command from the root of the project

```bash
make upgrade
```

* You'll need to down [ngrok](https://ngrok.com/) to act as a tunneling engine to serve your APP.

## Contributors

View the list of [contributors](https://github.com/BolajiOlajide/rmw-bot/contributors) who participate in this project.
