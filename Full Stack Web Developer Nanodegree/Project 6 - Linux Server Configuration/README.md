
I. The IP address and SSH port so your server can be accessed by the reviewer.
---

52.29.248.128 on port 2200
```
ssh grader@52.29.248.128 -p 2200 -i key
```

II. The complete URL to your hosted web application.
---

http://52.29.248.128/

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
2200/tcp (v6)              ALLOW       Anywhere (v6)
80/tcp (v6)                ALLOW       Anywhere (v6)
123 (v6)                   ALLOW       Anywhere (v6)
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

IV. A list of any third-party resources you made use of to complete this project.
---

http://songhuiming.github.io/pages/2016/10/30/set-up-flask-web-host-on-digitalocean-vps/
