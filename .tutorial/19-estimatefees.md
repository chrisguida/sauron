# estimatefees

`estimatefees`: Estimate fees for various lightning transactions.
```python
@plugin.method("estimatefees")
def estimatefees(plugin, **kwargs):
    """
    Args:
        plugin: The plugin instance.
        kwargs: Additional arguments.

    Returns:
        A dictionary with the following keys:
        - opening: The estimated fee for opening a channel.
        - mutual_close: The estimated fee for a mutual close.
        - unilateral_close: The estimated fee for a unilateral close.
        - delayed_to_us: The estimated fee for a delayed to_us output.
        - htlc_resolution: The estimated fee for resolving an HTLC.
        - penalty: The estimated fee for a penalty transaction.
        - min_acceptable: The minimum acceptable fee.
        - max_acceptable: The maximum acceptable fee.
    """
    pass
```