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
    # Instructs Nginx to listen on port 80 (HTTP). 
    # This is the default HTTP port.

    client_max_body_size 20;
    # Sets the maximum allowed size of a client's request body. 
    # Note: By default, '20' is interpreted as 20 bytes, 
    # so typically you would specify '20M' for 20 megabytes.

    error_log /var/log/nginx/error.log error;
    # Defines where server-level errors will be logged 
    # and at which log level (here, 'error').

    proxy_set_header Host $host;
    # Passes the original 'Host' header from the client 
    # through to the upstream (your Django app).

    proxy_set_header X-Real-IP $remote_addr;
    # Sets the client IP address so the upstream sees 
    # the actual client IP instead of the proxy's IP.

    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    # Appends the client's IP address (and any previous proxy IPs) 
    # to the X-Forwarded-For header for tracking the request chain.

    proxy_set_header X-Forwarded-Proto $scheme;
    # Tells the upstream whether the original request 
    # was over HTTP or HTTPS.

    proxy_pass_header X-Django-User;
    # Instructs Nginx to forward the custom 'X-Django-User' header 
    # from the upstream response back to the client or logs.

    location /api/v1/ {
        proxy_pass http://api;
        # Any request starting with /api/v1/ 
        # is forwarded (proxied) to the service named 'api' on port 8000.

        access_log /var/log/api_access.log detailed_log;
        # Access logs for requests to /api/v1/ 
        # are stored in /var/log/api_access.log using the 'detailed_log' format.

        error_log /var/log/api_error.log error;
        # Errors specific to /api/v1/ go to /var/log/api_error.log.
    }

    location /supersecret {
        proxy_pass http://api;
        # Another location block that proxies requests to the same 'api' service.
        # Often used for admin or sensitive endpoints.

        access_log /var/log/nginx/admin_access.log detailed_log;
        # Keeps separate access logs for admin or sensitive requests.
    }

    location /static/ {
        alias /app/staticfiles/;
        # Serves static files directly from /app/staticfiles/ 
        # (bypassing Django entirely for efficiency).

        expires 30d;
        # Tells browsers and proxies to consider these files fresh for 30 days.

        add_header Cache-Control "public, amx-age=2592000";
        # Adds a Cache-Control header. 
        # (Likely meant to say "max-age" for 30 days in seconds: 2592000)
        # This ensures files can be cached publicly for performance.
    }
}
}
```