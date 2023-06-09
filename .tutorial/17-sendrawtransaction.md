# sendrawtransaction

`sendrawtransaction`: Send a raw onchain transaction
```python
@plugin.method("sendrawtransaction")
def sendrawtx(plugin, tx, **kwargs):
    """
    Send a raw transaction.

    Args:
        plugin: The plugin instance.
        tx: The raw transaction.
        kwargs: Additional arguments.

    Returns:
        A dictionary with the following keys:
        - success: True if the transaction was successfully sent, False otherwise.
        - errmsg: An error message, if applicable.
    """
    pass
```
