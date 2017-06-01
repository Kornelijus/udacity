# Logs Analysis
A tool that connects to a PostgreSQL database and prints out reports.

## Requirements
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](https://www.vagrantup.com/downloads.html)
- [Python 3.*](https://www.python.org/)
- [`fullstack-nanodegree-vm`](https://github.com/udacity/fullstack-nanodegree-vm)
- `newsdata.sql`
- `psycopg2`

## Setup
- Copy `newsdata.sql` and `reportingtool.py` to `fullstack-nanodegree-vm/vagrant/`
- Open your terminal and `cd` there
- `vagrant up`
- `vagrant ssh`
- `cd vagrant`
- `psql -d news -f newsdata.sql`

## How to run
- `python3 reportingtool.py`
