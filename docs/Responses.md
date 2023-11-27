# Responses From Backend

> Note: The backend server is expected to identify the agent making the request without any additional parameters being sent. By default RunbookSolutions achieves this using the OAuth Device Code process to retrieve an Access Token for authentication.
>> In non-NAT'ed environments; the backend server could use the IP address from the request to identify agents.

## `GET /api/agent`

This endpoint provides the agent with basic information about itself along with a list of PLUGIN_ID's that the agent should have loaded.

- The Team ID provided here is used to identify and group agents to specific groups on the backend. It is **required** even if not used.


```json
{
	"data": {
		"id": "9ab55db0-9bfa-45a6-8280-bb94c6b0fe8d",
		"name": "Test Agent",
		"team_id": "9ab55261-b6b0-4fb4-85e5-a3491a72f720",
		"plugins": [
			"9ab56426-f429-4c4b-9755-40c92449f0be"
		]
	}
}
```

## `GET /api/agent/plugin/{plugin_id}`
This endpoint provides the agent with individual plugins for the agent along with the corresponding commands the plugin makes available.

> Note: It is important to note that two different versions of a plugin may be loaded by an agent. Commands are prefixed with the PLUGIN_ID to avoid collisions.

- The `script` variable contains the code the agent will execute when required.
- The `hash` variable is the `SHA512` hash of the script; the agent will verify both the script variable as well as the file it creates to store the plugin.
- The `commands` variable contains the details of what function in the program to run for which command is provided.

> Important: Both the `script` variable and the file written to disk must match the provided hash for the plugin to be loaded and run.

```json
{
	"data": {
		"id": "9ab56426-f429-4c4b-9755-40c92449f0be",
		"name": "Test Plugin",
		"version": 0,
		"description": null,
		"script": "class Plugin:\n    def __init__(self):\n        pass\n    def greet(self):\n        print(\"Hello from the Test Plugin!\")\n    def square(self, number):\n        result = number ** 2\n        print(f\"The square of {number} is {result}\")",
		"hash": "809c167b7b1e7fb9504dc136af3c2dc1c17545355a9aaec28c3792e54bc540943db236b6af547a732161b5d717c9b14a7c508ab49b3f06e128997de06b3abfd3",
		"commands": {
			"9ab56426-f429-4c4b-9755-40c92449f0be.greet": {
				"id": "9ab5659c-271d-40d5-be37-3a3847b92aab",
				"name": "9ab56426-f429-4c4b-9755-40c92449f0be.greet",
				"function": "greet"
			},
			"9ab56426-f429-4c4b-9755-40c92449f0be.square": {
				"id": "9ab565fc-1036-4afb-ac7e-ec92e0db6985",
				"name": "9ab56426-f429-4c4b-9755-40c92449f0be.square",
				"function": "square"
			}
		}
	}
}
```

## `GET /api/agent/tasks`
The following endpoint provides the agent with details of what commands need to be run, when (if scheduled), and any arguments for said command.

- The `command` variable must match one of the keys provided by the `plugin.commands` variable when downloading plugins.
- The `cron` variable is the cron formatted schedule for when the task runs, or `null` if it should only be run once.
- The `arguments` variable should be a JSON encoded string containing the argument name and values for the function to run.

> Note: The agent uses the `task.id` to ensure tasks are not being duplicated into the schedule and queue.

```json
{
	"data": [
		{
			"id": "9ab581cf-546d-405a-afaf-474cc631ed5c",
			"command": "9ab56426-f429-4c4b-9755-40c92449f0be.greet",
			"cron": null,
			"arguments": "{}"
		},
		{
			"id": "9ab582f7-9e64-4fad-b6b9-369633776ae4",
			"command": "9ab56426-f429-4c4b-9755-40c92449f0be.square",
			"cron": "* * * * *",
			"arguments": "{\"number\":2}"
		}
	]
}
```