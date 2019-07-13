#Linux Server Configuration
Part of Udacity nanodegree.

### 1. connect to server

Open the terminal.

```
# Login to server
ssh  grader@54.187.88.4 -i ~/.ssh/linuxcouse -p 2200
```

# private key
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEArvIqfgmE8z72QbhofykCaQOTZKtFFKjtFtWTPsehxUcwCItz
H3SpRleA4CGm4bcgURwhOvkvNxGQGHjNGqT+zadL7q9+2luqY4wb0DrKPdfoLzS/
lohw1hMnrzj9TS1v6UfwNepWLoFkNtZFABT1bfKoGtMBIInnq8D5Mqa20Ylplnjz
1ff+ngv0M1ZfUyM1F62xemOObiTVZmS0TcoDjLL81iqxiowxiOW2wq8j9JGfjzd3
H37YooZMezWxWqmv5J3q8e0xbqr0YRdTdy5Y4hBewahssuIUAI8Okc8NViFP3grR
/Uc0oHIIz4gfI7JQJ+MaoqQ9VWklyb0AgZIQcQIDAQABAoIBAQCODadBRjuFREez
X6jCMCt71+Jz6LokJ3K0iuGQJYuO49n15j2pehIFQwIrfEfEme0Mz1mQSEv1XDZ0
GIr6qqUXmlOG0UugxLPbNyZSc5pKkyk+Q4eaFNoCifU8S3sqks1/T+GV9dza0Efu
WxgWE+6hw1qKxXDx2eiaxwvR/BsQkjqVX9whCcsdU0154Ir6CivMseBLukzZv5CF
N/Q4smHh2Ox4GBndJJzkvjv/vD6yCHlzsWxZO6FJywcLIDDfaqEtBhcFp+fi2bPq
EoY158HhYqHMJ1LlWx/+ArjvH1I9rAWRFEeT60P+2lu+79laW1PxlJvJCgzyUvMY
yvJDxfkRAoGBANuyKWuJMjvKkjI3hKVJXFcJykjjEN8uAk+Pk+hoqTZXqDKFWWd7
xPvNw1nzUlmsnfXUc2K7E/vHr2wl5ltXFOaCpYZBML3AkQOE/ON9b6svFNmp+xGM
5fIfzCyFrYWWreuooYCIRfSjwHyYjvspMobnZguE3wNHKCCoosCIp7NdAoGBAMva
7/YOT6OW/S+x7V1fR/F/6FvZezduS8wOh9I8t80RC3jNtaIHgwJAESQ9zz5e82kX
sIOyzrXmmZWUVpXvb73aafG54upYnOI7Sjrm8x7l/0pjjO/KRPCxaAdktWxNkP//
O/0mJ2Tpymu7TWck5ugDBRa1j/kCPgLnOGXqW3QlAoGAGd9jbVyc49m5Wdyb7HM1
QrLOdcL367CZaRE5k/cvZkzwa/K0UrGKwzS6Os+i9RiVCaxZYlkxw0cC67OS61LY
DUV5hNQMj2wsJ8PznD7bdcd3pyKThL+ZHOiNvPiJNOBH3ybezio+Qs8+De5ReFaj
sqtxow2kzdgFa8MwV4hAZ6kCgYEAwVkLhZX3RRK9WxJoLspjQxPs/8jbjCyJqaYS
fn3mWpKTDeYWIvL6+BRp7bTOLrsCJSg52/+o/XAVNYD3SshJdImHOKT1Kw4W5qAT
fKB18VV1+ElJcFmpX5z0LScAyBMdtyCO9kDM1nLD8cA53t1qQJ40omBciHHu/PPv
UwKf8R0CgYEAzOkU8dEbQjotsHcI1MiC40GF2VpADJ8cVQRv6jkSDrNxwapRQDqM
2Kh4SexSrwDpAt4LA2Hjevd1/1ExJCq17btbvboHGnHg98HEa1Pt7H9h63J0TbVC
J7O8f6HZFhSukucS5NVNnJt+dkhJV5YMr1Ow7+6ksdW7up183vSzx6U=
-----END RSA PRIVATE KEY-----

```

# passphrase for key
```
grader
```

#Configuration

### Install apache
```
sudo apt-get install apache2
```

### Installing mod_wsgi
```
sudo apt-get install libapache2-mod-wsgi
```

### edit
```
/etc/apache2/sites-enabled/000-default.conf
```
adding
```
WSGIScriptAlias / /var/www/html/catalog/application.wsgi
```
then
```
sudo apache2ctl restart
```

### Installing PostgreSQL
```
sudo apt-get install postgresql
```

### Installing git
```
sudo apt-get install git
```

### add user
```
sudo add user grader
```

### Giving Sudo Access
create
```
/etc/sudoers.d/grader
```
add
```
grader ALL=(ALL) NOPASSWD:ALL
```

### Generating Key Pairs
run on your local machine
```
ssh-keygen
```
give it name
```
linCourse
```
add this public key inside my server at
```
/home/grader/.ssh/authorized_keys
```
and run
```
chmod 700 .ssh
chmod 600 .ssh/authorized_keys
```

### to handle permissions
```
sudo chown -R grader.grader /home/grader/.ssh
```

### ports
```
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2200/tcp
sudo ufw allow www
sudo ufw allow ntp
sudo ufw enable
```

### edit 
```
/etc/ssh/sshd_config
```
change ssh port from (22) to (2200) and edit (PermitRootLogin) set to (no)


### connect to sesrver localy

### add postgres user
```
sudo -u postgres createuser -P catalog
```

### create catalog database
```
sudo -u postgres createdb -O catalog catalog
```

### clone
clone inside  ``/var/www/html``

### run
```
sudo pip install httplib2
sudo pip install requests
sudo pip install oauth2client
sudo pip install sqlalchemy
sudo pip install flask
sudo pip install psycopg2
```


# Third-party Authentication

```
using Google Accounts
```

## Rubric

## User Management

|SECTION|CRITERIA|
|---|---|
| Login To Server as grader User | can login to server as grader user using the submitted key |
| Remote Login Disabled | You cannot log in as root remotely|
| Sudo Access | grader User Has Sudo Access|

## Security

|SECTION|CRITERIA|
|---|---|
| SSH, HTTP, and NTP | Only allow connections for SSH (port 2200), HTTP (port 80), and NTP (port 123) |
| Required RSA keys | users required to authenticate using RSA keys|
| Applications up-to-date | All system packages have been updated to most recent versions|
| SSH hosted on non-default port | SSH is hosted on non-default port|

## Application Functionality

|SECTION|CRITERIA|
|---|---|
| Web Server Running On Port 80 | Only allow connections for SSH (port 2200), HTTP (port 80), and NTP (port 123) |
| Database Server | Database server has been configured to serve data (PostgreSQL)|
| web server been configured to serve the Item Catalog application | Web server has been configured to serve the Item Catalog application as a WSGI app|
| SSH hosted on non-default port | SSH is hosted on non-default port|

## Documentation

|SECTION|CRITERIA|
|---|---|
| Web Server Running On Port 80 | Only allow connections for SSH (port 2200), HTTP (port 80), and NTP (port 123) |
| Database Server | Database server has been configured to serve data (PostgreSQL)|
| web server been configured to serve the Item Catalog application | Web server has been configured to serve the Item Catalog application as a WSGI app|
| SSH hosted on non-default port | SSH is hosted on non-default port|

## Resources
https://knowledge.udacity.com/questions/31565
