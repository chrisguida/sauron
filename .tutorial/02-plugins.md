# How Core Lightning Plugins Work (by cguida)

Core Lightning Plugins are executables that run as subprocesses of `lightningd`, the master process of your core lightning node. CLN ships with a bunch of default plugins that implement the fundamentals of the lightning network specification like `gossipd`, `channeld`, `pay`, etc.

You can "plug in" additional plugins to the node at run time by writing an executable and defining for `lightningd` what it does, what it needs, and how to interact with it.

## Plugin Life Cycle

## 1) Plugin launches
- Plugin is started by CLN in one of two ways: at CLN startup, or dynamically at runtime.
  - At startup:
    - Via a command line option: `lightningd --plugin=/path/to/plugin1 --plugin=path/to/plugin2`
    - Via an option in the config file: `plugin=/path/to/plugin`
  - At runtime:
    - Via `lightning-cli plugin start /path/to/plugin [options]`

## 2) `lightningd` calls `getmanifest` on the plugin
- Plugin responds with a manifest where everything the plugin needs is registered with CLN, including options, hooks, rpc methods, and notifications.

The plugin's response will look something like this:
```json
{
  "options": [
    {
      "name": "greeting",
      "type": "string",
      "default": "World",
      "description": "What name should I call you?",
      "deprecated": false
    }
  ],
  "rpcmethods": [
    {
      "name": "hello",
      "usage": "[name]",
      "description": "Returns a personalized greeting for {greeting} (set via options)."
    },
    {
      "name": "gettime",
      "usage": "",
      "description": "Returns the current time in {timezone}",
      "long_description": "Returns the current time in the timezone that is given as the only parameter.\nThis description may be quite long and is allowed to span multiple lines.",
      "deprecated": false
    }
  ],
  "subscriptions": [
    "connect",
    "disconnect"
  ],
  "hooks": [
    { "name": "openchannel", "before": ["another_plugin"] },
    { "name": "htlc_accepted" }
  ],
  "featurebits": {
    "node": "D0000000",
    "channel": "D0000000",
    "init": "0E000000",
    "invoice": "00AD0000"
  },
  "notifications": [
    {
	  "method": "mycustomnotification"
	}
  ],
  "nonnumericids": true,
  "dynamic": true
}
```

## 3) `lightningd` calls the plugin's `init` method
- CLN parses plugin options and passes them back by calling the plugin’s `init` method. This is also the signal that `lightningd`’s JSON-RPC over Unix Socket is now up and ready to receive incoming requests from the plugin.
- The request will look something like this:
```json
{
  "options": {
    "greeting": "World",
	"number": [0]
  },
  "configuration": {
    "lightning-dir": "/home/user/.lightning/testnet",
    "rpc-file": "lightning-rpc",
    "startup": true,
    "network": "testnet",
    "feature_set": {
        "init": "02aaa2",
        "node": "8000000002aaa2",
        "channel": "",
        "invoice": "028200"
    },
    "proxy": {
        "type": "ipv4",
        "address": "127.0.0.1",
        "port": 9050
    },
    "torv3-enabled": true,
    "always_use_proxy": false
  }
}
```
- The plugin sends a success response.
  - The plugin can optionally send a response at this point indicating that it’s disabled.
- This response must occur within a certain timeout:
  - During startup, a plugin must respond within 60 seconds or it is killed.
  - Plugins launched dynamically must respond to both getmanifest and init within 60 seconds or they are killed.

## The plugin is now running.

Alright, that's everything you need to know about plugins.