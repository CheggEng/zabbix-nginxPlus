# Zabbix Nginx Plus Monitoring
This repo comes with the monitoring script, template and example user_params config.  Below are some random thoughts on how this all comes together.  Their are a lot of items in this config, feel free to remove the items you don't know.  Also because every env is very unique no triggers are defined.  You should define your own based off of your usage pattern.

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


### Monitoring Script
**nginxPlusInfo.py** is the script that will connect to your nginx status pages json interface and fetch all the metrics.  It also has the ability to do Zabbix low level discovery to populate metrics for zones and caches. In the future we may add upstreams for load balancers.


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

#### Example LLD Usage

Here's an example of how the zabbix lld gets nginx cache metrics

```
[zabbix@monitor01.prod2 ~]$ zabbix_get -s nginx.prod.example.com -k nginx.plus['--lld-caches']
{
    "data": [
        {
            "{#CACHE_NAME}": "news"
        },
        {
            "{#CACHE_NAME}": "photos"
        },
        {
            "{#CACHE_NAME}": "blog"
        }
    ]
}
```



### User paramter conf
The discovery runs local on the nginx server.  In order to be used it needs to be added to userparams.  Create a file under ***/etc/zabbix/zabbix_agentd.d/user_params_nginxPlus.conf*** with the following

```
# We use the same script for fetching individual metrics as we use for LLD
# Change the path /var/lib/zabbix/nginx/scripts to where ever you place your 
# Zabbix Scripts
UserParameter=nginx.plus[*],/var/lib/zabbix/nginx/scripts/nginxPlusInfo.py $1
```

Once you've created the file and paid special attention to set the path to the script where it lives on **YOUR** system be sure to recyle the zabbix_agent daemon.