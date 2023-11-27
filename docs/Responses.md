# Responses From Backend

GET /api/agent
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

GET /api/agent/plugin/{plugin_id}
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

GET /api/agent/tasks
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