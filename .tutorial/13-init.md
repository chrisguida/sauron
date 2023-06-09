# Init: Setting up the Plugin

`init`: Initializes the Sauron Plugin
```python
@plugin.init()
def init(plugin, options, configuration, **kwargs):
    """
    Args:
        plugin: The Plugin object.
        options: The command line options passed to the plugin.
        configuration: The lightningd configuration.
        kwargs: Additional arguments.

    Returns:
        None
    
    Raises:
        SauronError: If the sauron-api-endpoint option is not specified.
    """
    pass
```