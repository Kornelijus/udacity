
I. The IP address and SSH port so your server can be accessed by the reviewer.
---

52.29.248.128 on port 2200

```
ssh grader@52.29.248.128 -p 2200 -i key
```

II. The complete URL to your hosted web application.
---

http://52.29.248.128.nip.io/

Google OAuth doesn't like IPs, so I had to improvise.

III. A summary of software you installed and configuration changes made.
---

#### Update all currently installed packages.

```
sudo apt-get update
sudo apt-get upgrade
```

#### Change the SSH port from 22 to 2200. Make sure to configure the Lightsail firewall to allow it.

Make sure the Lightsail firewall isn't blocking TCP port 2200.

![Image of the Lightsail firewall](https://image.prntscr.com/image/oV2aVMenTbGY6MCc5EaYEg.png)

```
sudo nano /etc/ssh/sshd_config
```
```
...
Port 2200
...
```
```
sudo service ssh restart
```

#### Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).

```
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2200/tcp
sudo ufw allow www
sudo ufw allow ntp
sudo ufw deny 22/tcp
sudo ufw enable
```

```
sudo ufw status

Status: active


To                         Action      From
--                         ------      ----
2200/tcp                   ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
123                        ALLOW       Anywhere
22/tcp                     DENY        Anywhere
2200/tcp (v6)              ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
123 (v6)                   ALLOW       Anywhere (v6)
22/tcp (v6)                DENY        Anywhere (v6)
```

#### Create a new user account named grader.

```
sudo adduser grader
```

#### Give grader the permission to sudo.

```
sudo nano /etc/sudoers.d/grader
```
```
# User rules for grader
grader ALL=(ALL) NOPASSWD:ALL
```

#### Create an SSH key pair for grader using the ssh-keygen tool.

You're supposed to generate the keys on a local machine, not Lightsail.

```
ssh-keygen
cat key_path.pub
```
```
ssh-rsa AAAAB7Nza...
```

Log in into the server as `grader` and make sure you're in `/home/grader/`.

```
mkdir .ssh
sudo nano .ssh/authorized_keys
```
```
ssh-rsa AAAAB7Nza...
```
```
chmod 700 .ssh
sudo chmod 644 .ssh/authorized_keys
```

Make sure `sshd_config` forces key based authentication.

```
sudo cat /etc/ssh/sshd_config
```
```
...
PasswordAuthentication no
...
```

#### Configure the local timezone to UTC.

```
sudo dpkg-reconfigure tzdata
```
```
>> None of the above
>> UTC
```

#### Install and configure Apache to serve a Python mod_wsgi application.

At this point, it's very easy to mess something up, so it's a good idea to make a screenshot of your Lightsail instance.

![Image of the Lightsail snapshot progress](https://image.prntscr.com/image/ruC8MYQjRa6TVsZBOR6slQ.png)

It'll take forever for it to create the snapshot, but still better than doing everything all over again if you mess something up.

Time to install a bunch of stuff.

```
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi-py3
sudo apt-get install python3-pip
sudo apt-get install postgresql
sudo apt-get install git
sudo -H pip3 install flask requests oauth2client sqlalchemy psycopg2
```

Clone the Github repo for catalog-postgresql.

```
cd var/www/
sudo git clone https://github.com/Kornelijus/catalog-postgresql catalog
```

Set up the apache2 virtualhost.

```
sudo nano /etc/apache2/sites-available/000-default.conf
```
```xml
<VirtualHost *:80>
        ServerAdmin admin@website
        WSGIScriptAlias / /var/www/catalog/catalog.wsgi
        <Directory /var/www/catalog/>
            Order allow,deny
            Allow from all
        </Directory>
        Alias /static /var/www/catalog/static
        <Directory /var/www/catalog/static/>
            Order allow,deny
            Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
```
sudo apache2ctl restart
```

At this point, the only way to test if everything is alright is to check the logs. The server will still return a 500 because the database is not set up and the only error left should be:

```
FATAL:  password authentication failed for user "catalog"
```

If that's the case, time to set up the postgresql database.

#### ~~Install~~ and configure PostgreSQL:

Well, the install part is already done.

```
sudo su postgres
psql
create user catalog_user with password '123456';
create database catalog with owner catalog_user;
```
```
cd var/www/catalog/
python3 example_catalog.py
```
```
sudo apache2ctl restart
```

The website should work fine now.

#### Rubrics: You cannot log in as root remotely.
```
sudo nano /etc/ssh/sshd_config
```
```
...
PermitRootLogin no
...
```
```
sudo service ssh restart
```

IV. A list of any third-party resources you made use of to complete this project.
---

http://songhuiming.github.io/pages/2016/10/30/set-up-flask-web-host-on-digitalocean-vps/

https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps/

http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/

https://medium.com/@iktw/postgresql-create-user-create-database-grant-privileges-access-aabb2507c0aa

https://stackoverflow.com/questions/28619686/what-is-the-h-flag-for-pip

https://mediatemple.net/community/products/dv/204643810/how-do-i-disable-ssh-login-for-the-root-user
