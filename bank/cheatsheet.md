# Docker
### Before we can build the containers, let's confirm that these services are able to get these environment variable files:
```docker compose -f local.yml config```
<hr>

### Build containers:
```docker compose -f local.yml up --build -d --remove-orphans```
```bash
--build           # build images before running the containers
-d                # run containers in the background
--remove-orphans  # remove containers for services not defined in the compose file.
```
<hr>

### Check logs:
```docker compose -f local.yml logs <name_of_service_optionaly>```
<hr>

### Check volumes:
```docker volume inspect <name_of_the_volume>```
<hr>

### Inspect network:
```docker network inspect <name_of_the_network>```

<hr>

### Bring down containers:
```bash
docker compose -f local.yml down
docker compose -f local.yml down -v  # bring down our containers and remove any associated volumes.
```

<hr>
<br><br>

# Postgres
### Commads
```bash
\list      #  list available db
\connect   # connect to db
\dt        # show the tables in db
\q         # exit
```


<hr>
<br><br>

# NGINX
## CONFIG
```nginx
log_format detailed_log '$remote_addr - $ipstream_http_x_django_user - [$time_local]'
                        '"$request" $status $body_bytes_sent'
                        '"$http_referer" "$http_user_agent"'
                        '$request_time $upstream_response_time '
                        '"$http_x_forwarded_for" ';
```
- `remote_addr` - the IP address of the client making the request to the API.
- `upstream_http_x_django_user` - the value of the X-Django-User header from the middleware.
- `time_local` - local time when the request was received.
- `request` - the request from the client.
- `status` - http status code.
- `body_bytes_sent` - number of bytes sent to the client excluding the headers.
- `http_referer` - the referrer header from the client request.
- `http_user_agent` - the user agent header from the client request.
- `request_time` - the total time spent processing the request.
- `upstream_response_time` - the time it took for the upstream server to respond.
- `http_x_forwarded_for` - the header from the client request typically used to pass the original client IP address through proxies


```nginx
server {
    listen 80;

    client_max_body_size 20;     # set the max allowed size of a client request body

    error_log /var/log/nginx/error.log error;     # location, where all server errors are going to be stored 

    proxy_set_header Host $host;

    proxy_set_header X-Real-IP $remote_addr;

    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    
}
```