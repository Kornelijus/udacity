# Item Catalog
A Flask project that users can connect to, log in with Google OAuth and add, edit, delete items in premade categories.
## Requirements
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](https://www.vagrantup.com/downloads.html)
- [Python 3.*](https://www.python.org/)
- [`fullstack-nanodegree-vm`](https://github.com/udacity/fullstack-nanodegree-vm)
- `flask`
- `sqlalchemy`
- `oauth2client`
- `requests`

## Setup
- Copy this project into `fullstack-nanodegree-vm/vagrant/catalog/`
- Open your terminal
- `cd` into `fullstack-nanodegree-vm/vagrant/`
- `vagrant up`
- `vagrant ssh`
- `cd vagrant/catalog/`

## How to run
- `python3 app.py`

## How to reset the database
- `rm catalog.db`
- `python3 example_catalog.py`
