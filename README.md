# RunbookSolution Network Agent

This codebase composes the core of the Network Agent for RunbookSolutions.

## Installation

### Prebuilt Docker Image
NOTE: THE DOCKER IMAGE DOES NOT CURRENTLY EXIST

```sh
mkdir agent
cd agent
mkdir plugins,stores,kerberos
wget https://raw.githubusercontent.com/RunbookSolutions/agent/staging/config.ini

docker run \
    --name RunbookSolutions_Agent \
    -v $(pwd)/config.ini:/app/config.ini \
    -v $(pwd)/plugins:/app/plugins \
    -v $(pwd)/stores:/app/stores \
    -v $(pwd)/kerberos/krb5.conf:/etc/krb5.conf \
    -v $(pwd)/kerberos:/keytabs \
    -d \
    --restart unless-stopped \
    runbooksolutions/image_agent:latest

```

### From Source:
```sh
git clone https://github.com/RunbookSolutions/agent.git
cd agent
./run
```

## Configuration
Configuration maintained in a simple `config.ini` file consisting of the server_url of the backend; and the client_id for the device authentication.

```ini
[agent]
server_url=http://192.168.1.197 # Note: Do NOT include a trailing slash on the server_url
client_id=9ab55261-bfb7-4bb3-ad29-a6dbdbf8a5af # Device Code Grant client_id provided by the server
```

### Creating a Keytab File

```
docker run -it --rm \
            -v $(pwd):/output \
            -e PRINCIPAL=<user@EXAMPLE.COM> \
            simplesteph/docker-kerberos-get-keytab
```