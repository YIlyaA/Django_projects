
### Before we can build the containers, let's confirm that these services are able to get these environment variable files:
```docker compose -f local.yml config```
<hr>

### Build containers:
```docker compose -f local.yml up --build -d --remove-orphans```
```bash
--build           // build images before running the containers
-d                // run containers in the background
--remove-orphans  // remove containers for services not defined in the compose file.
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
```docker compose -f local.yml down```