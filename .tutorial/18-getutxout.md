# getutxout

`getutxout`: Get the UTXO at the given transaction ID and output index.
```python
def getutxout(plugin, txid, vout, **kwargs):
    """
    Args:
        plugin: The plugin instance.
        txid: The transaction ID.
        vout: The output index.
        kwargs: Additional arguments.

    Returns:
        A dictionary with the following keys:
        - amount: The amount of the UTXO.
        - script: The scriptPubKey of the UTXO.

    Raises:
        SauronError: If there is an error fetching the UTXO.
    """
    pass
```