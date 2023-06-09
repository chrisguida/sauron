# getutxout: Look up a specific outpoint

This method is used to look up the specific utxos for your channels or other channels you're interested in. We return back the amount and script to confirm they match our expectations from the transaction we negotiated with our channel partner.

The pseudocode for `getutxout` is...


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

Try implementing it yourself! Read on for implementation details.

## `getutxout` Implementation

Another easy one! 