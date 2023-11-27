# RunbookSolution Agent

This codebase comprises the core of the Agent for RunbookSolutions.

- [Introduction](#introduction)
- [Installation](#installation)
  - [Prebuilt Docker Image](#prebuilt-docker-image)
  - [Extending the Default Image](#extending-the-default-image)
  - [From Source](#from-source)
- [Configuration](#configuration)
  - [`config.ini` Parameters](#configini-parameters)
  - [Example Configuration](#example-configuration)
- [API Requests](#api-requests)
- [Additional Notes](#additional-notes)
  - [Creating a Keytab File](#creating-a-keytab-file)
  - [Security Considerations](#security-considerations)


## Introduction

The RunbookSolution Agent serves as a pivotal component within the RunbookSolutions documentation system. 
Designed as a local daemon, its primary objective is to conduct scans, identifying crucial facts and features related to networks and devices. 
What sets it apart is its ability to seamlessly relay these results to the backend without necessitating the installation of a client on each device.

To achieve the required flexibility, the Agent operates on a plugin-based architecture.
Plugins, obtained from a remote server on demand, empower the Agent with diverse functionalities, ensuring the deployment of new features and scans without manual intervention on the Agent itself.

Key components that constitute the Agent's core functionality include:

- **Auth**: Facilitates agent registration and authentication with the backend using the OAuth2 "Device Flow".
- **Stores**: Enables the Agent to persist information about its current state, ensuring data retention through restarts.
- **Queue**: Manages a task queue and efficiently executes tasks in a threadpool.
- **Schedule**: Allows the scheduling of tasks at regular intervals, employing cron notation.

In addition to these, the Agent incorporates the following components:

- **API**: Establishes communication with the backend server.
- **PluginManager**: Manages the retrieval and execution of plugins.


## Installation
To deploy the RunbookSolution Agent, you have several options depending on your requirements. Follow the instructions below based on your preferred method:

### Prebuilt Docker Image
If you prefer a quick and straightforward installation using Docker, follow these steps:

```sh
# Create necessary directories
mkdir agent
cd agent
mkdir plugins stores kerberos
wget https://raw.githubusercontent.com/RunbookSolutions/agent/production/config.ini

# Run the Docker container
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

### Extending the Default Image

If you need additional Python libraries for custom plugins, you can extend the default image. Follow these steps:

Create your custom Docker file:

```Dockerfile
FROM runbooksolutions/agent:latest
# Using a requirements.txt (Recommended)
COPY requirements.txt /app/custom_requirements.txt
RUN pip install -r custom_requirements.txt
# OR Individually
RUN pip install some_package
```

Build and run the customized Docker image:

```sh
docker build . --tag YOUR_NAME_OR_COMPANY/agent:latest

docker run \
    --name RunbookSolutions_Agent \
    -v $(pwd)/config.ini:/app/config.ini \
    -v $(pwd)/plugins:/app/plugins \
    -v $(pwd)/stores:/app/stores \
    -v $(pwd)/kerberos/krb5.conf:/etc/krb5.conf \
    -v $(pwd)/kerberos:/keytabs \
    -d \
    --restart unless-stopped \
    YOUR_NAME_OR_COMPANY/agent:latest
```


### From Source
If you prefer building from the source code, execute the following commands:

```sh
git clone https://github.com/RunbookSolutions/agent.git
cd agent
./run
```

Ensure you have the necessary dependencies installed before running the build.

These installation options provide flexibility based on your specific needs, whether you opt for a Dockerized setup, extend the default image, or build from the source code. Choose the method that aligns with your deployment preferences and system requirements.

## Configuration
Configuring the RunbookSolution Agent is a crucial step to tailor its behavior to your specific environment. The configuration is maintained in a straightforward 'config.ini' file, which includes essential parameters for seamless operation. Here's a breakdown of the key configuration options:

### `config.ini` Parameters

- `server_url`: Specifies the URL of the backend server. Avoid including a trailing slash in the URL.
```ini
[agent]
server_url=http://192.168.1.197
```
- `client_id`: Identifies the device during the authentication process. This is the Device Code Grant client_id provided by the server.
```ini
[agent]
client_id=9ab55261-bfb7-4bb3-ad29-a6dbdbf8a5af
```
- `auth`: Enables or disables authentication when not using RunbookSolutions. Set to True to enable authentication.
```ini
[agent]
auth=True
```

### Example Configuration
Here's an example configuration snippet illustrating how to structure the 'config.ini' file:

```ini
[agent]
server_url=http://your-backend-url.com
client_id=your-client-id
auth=True
```

Adjust the values according to your backend server's URL, client ID, and authentication preference.

The 'config.ini' file plays a pivotal role in customizing the RunbookSolution Agent's interaction with the backend and authentication mechanisms. Ensure accurate configuration to seamlessly integrate the Agent into your network and device environment.

## API Requests
The RunbookSolution Agent communicates with the backend server through a set of well-defined API endpoints. Understanding these API requests is essential for implementing a custom backend or extending the functionality of the Agent. Below are the key endpoints and their purposes:

- `GET /api/agent`
  - **Purpose**: This endpoint allows the Agent to load information about itself from the backend. Additionally, it provides a list of PLUGIN_IDs that the Agent needs to load.

- `GET /api/agent/plugin/{PLUGIN_ID}`
  - **Purpose**: Used by the Agent to download plugins dynamically from the backend. This endpoint also provides details about the commands the plugin offers.

- `GET /api/agent/tasks`
  - **Purpose**: Enables the Agent to load tasks that need to be executed. Tasks include both scheduled and one-off tasks, ensuring continuous operation even after restarts.

- `POST /api/agent/task/{TASK_ID}`
  - **Purpose**: Enables the Agent to send the results of a task to the backend.
  - **Example**:
  ```sh
  curl -X POST http://YOUR_BACKEND_URL/api/agent/task/TASK_ID \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
      -d '{"data": "{\"key\": \"value\", \"another_key\": \"another_value\"}"}'
  ```
  In this example:

    - The URL should be customized with your backend server's details and the actual {TASK_ID}.
    - The `-H "Authorization: Bearer YOUR_ACCESS_TOKEN"` header includes the necessary bearer token for authentication.
    - The `-d '{"data": "{\"key\": \"value\", \"another_key\": \"another_value\"}"}'` part represents the payload of the POST request. The data variable contains JSON-encoded data representing the results of the executed task.

For those implementing a custom backend for the Agent, it's crucial to provide these endpoints to facilitate smooth communication. A deeper dive into the Expected Server Responses page will offer additional details on the expected responses from these endpoints.

Understanding these API requests empowers users to integrate the RunbookSolution Agent seamlessly into their infrastructure or develop custom functionalities, enhancing the overall capabilities of the system.

For additional information about the expected responses refer to the [Expected Server Responses](docs/Responses.md) page.

> Note: A Proof-of-Concept backend is available in the [agent_backend](https://github.com/RunbookSolutions/agent_backend) repository.

## Additional Notes

### Creating a Keytab File

Authentication against a Windows domain may require the use of keytab files, especially for certain plugins. Follow these steps using the [Docker Kerberos Keytab Generator](https://github.com/simplesteph/docker-kerberos-get-keytab) for a straightforward keytab file creation:

This Docker container facilitates the generation of keytab files, an essential aspect of some plugins' authentication against Windows domains.

```sh
cd agent
docker run -it --rm \
            -v $(pwd)/kerberos:/output \
            -e PRINCIPAL=<user@EXAMPLE.COM> \
            simplesteph/docker-kerberos-get-keytab
```

### Security Considerations
When generating keytab files or implementing authentication-related configurations, prioritize security practices. Ensure that sensitive information, such as authentication credentials, is handled and stored securely. Review and adhere to best practices for securing keytab files and associated authentication processes within your network environment.

By following these guidelines, you enhance the overall security posture of your RunbookSolution Agent deployment, minimizing potential risks associated with authentication processes and ensuring a robust and secure system.





