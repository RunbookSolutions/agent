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
    runbooksolutions/agent:latest

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
auth=True # To disable auth when not using with RunbookSolutions.
```

## Expected Server Responses
Due to the Agent's nature; it can easily be used by others outside of RunbookSolutions.

To implement a backend for this agent you will need to provided the following endpoints.

`GET /api/agent` for the agent to load information about itself. This endpoint also provides the agent with a list of PLUGIN_ID's that it needs to load.

`GET /api/agent/plugin/{PLUGIN_ID}` for the agent to download plugins. This endpoint also provides details about commands the plugin provides.

`GET /api/agent/tasks` for the agent to load tasks that it needs to run. Tasks include scheduled and one-off tasks to run; and will always present tasks until they are removed from the backend. This allows for the agent to restart without skipping task execution.

Additional details can be found on the [Expected Server Responses](/docs/Responses.md) page.

## Creating a Keytab File

Some plugins may require authentication against your windows domain.

The simplest way to acomplish this is by using the [Docker Kerberos Keytab Generator](https://github.com/simplesteph/docker-kerberos-get-keytab):

```sh
cd agent
docker run -it --rm \
            -v $(pwd)/kerberos:/output \
            -e PRINCIPAL=<user@EXAMPLE.COM> \
            simplesteph/docker-kerberos-get-keytab
```