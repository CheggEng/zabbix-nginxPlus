# Zabbix Nginx Plus Monitoring

## LLD
This template & script supports low level discovery via Nginx+ status url.  The nginx plus status page needs to be configured

In this example you can access the Nginx+ status page at 

* http://localhost:8080/status.html for the HTML5 page
* http://localhost:8080/status for the JSON page

```
server {
    listen 8080;
    root /usr/share/nginx/html;

    location = /status {
        status;
    }
}
```


### Script Usage

```
[zabbix@nginx]/var/lib/zabbix]$ /var/lib/zabbix/nginx/scripts/nginxPlusInfo.py --help
usage: nginxPlusInfo.py [-h] [--url URL] [--key KEY] [--lld-caches]
                        [--lld-zones] [--debug]

This is a simple Python tool that fetches data from nginx+ status api

optional arguments:
  -h, --help    show this help message and exit
  --url URL     Default: http://localhost:8080/status
  --key KEY     Return a specific key using dot notation
  --lld-caches  Use Zabbix low level discovery to find all caches
  --lld-zones   Use Zabbix low level discovery to find all zones
  --debug       Dumps all the data in dot notation from the status url
```

## User paramter conf