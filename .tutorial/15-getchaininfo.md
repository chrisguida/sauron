# getchaininfo

`getchaininfo`: Get information about the blockchain.

```python
@plugin.method("getchaininfo")
def getchaininfo(plugin, **kwargs):
    """
    Args:
        plugin: The Plugin object.
        kwargs: Additional arguments.

    Returns:
        A dictionary with the following keys:
        - chain: The name of the blockchain (main, test, or regtest).
        - blockcount: The current block count.
        - headercount: The current header count.
        - ibd: False (whether or not the node is currently in IBD).

    Raises:
        SauronError: If there is an error fetching the information.
    """
    pass
```