# getrawblockbyheight

`getrawblockbyheight`: Get a raw block's hex data at the given height.
```python
@plugin.method("getrawblockbyheight")
def getrawblock(plugin, height, **kwargs):
    """
     Args:
        plugin: The plugin instance.
        height: The block height.
        kwargs: Additional arguments.

    Returns:
        A dictionary with the following keys:
        - blockhash: The hash of the requested block.
        - block: The raw block in hexadecimal format.
    """
    pass
```