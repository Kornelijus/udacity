
i. The IP address and SSH port so your server can be accessed by the reviewer.
---

52.29.248.128 on port 2200

ii. The complete URL to your hosted web application.
---

http://52.29.248.128/

iii. A summary of software you installed and configuration changes made.
---

#### Update all currently installed packages.

```sh
sudo apt-get update
sudo apt-get upgrade
```

#### Change the SSH port from 22 to 2200. Make sure to configure the Lightsail firewall to allow it.

First, make sure the Lightsail firewall isn't blocking TCP port 2200.

[image]: https://image.prntscr.com/image/oV2aVMenTbGY6MCc5EaYEg.png "image"

`sudo nano /etc/ssh/sshd_config`
- Change `Port 22` to `Port 2200`
- Save changes

#### Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).

```sh
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2200/tcp
sudo ufw allow www
sudo ufw allow ntp
sudo ufw enable
```

UFW should be active now:

```sh
sudo ufw status

Status: active

To                         Action      From
--                         ------      ----
2200/tcp                   ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
123                        ALLOW       Anywhere
2200/tcp (v6)              ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
123 (v6)                   ALLOW       Anywhere (v6)
```

#### Create a new user account named grader.

```sh
sudo adduser grader
```

#### Give grader the permission to sudo.



iv. A list of any third-party resources you made use of to complete this project.
---

http://songhuiming.github.io/pages/2016/10/30/set-up-flask-web-host-on-digitalocean-vps/
