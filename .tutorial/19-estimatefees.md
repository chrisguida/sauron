# estimatefees: ensuring your TXs have high enough feerates to be included in a block

This method is extremely important! The security assumption of your lightning channel is that you'll be able to get a closing transction (mutual, unilateral, or justice that you're holding) included in a block. But lightning channels are 2/2 multisigs: you need your channel party to sign a new transaction with you if you want to update your channel state or your reserve transactions. 

Estimatefees is important because your node needs to be confident it can get its channel close TXs included in a timely manner. In fact, if you and your channel partner significantly disagree on the current fee rate estimates, your CLN node will attempt to close the channel just in case. That's how important accurate feerates are!

This is the pseudocode for `estimatefees`...

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

In high fee environments (like when people go on inscribing crazes or just in a few years when blocks are always full and fee spikes are more common), there are various attacks like "pinning" that nodes can do to try to prevent your transaction from getting confirmed. If they can pin you past when your justice transaction can sweep, your channel party might be able to steal from you.

Try implementing it yourself! Read on for implementation details.

## `estimatefees` Implementation

```python
feerate_url = f"{plugin.api_endpoint}/v1/fees/recommended"
feerate_res = fetch(feerate_url)

if not feerate_res.status_code == 200:
    raise 
feerates = feerate_req.json()

# Assigning the fees
fastest = feerates["fastestFee"]
half_hour = feerates["halfHourFee"]
hour = feerates["hourFee"]
economy = feerates["economyFee"]
minimum = feerates["minimumFee"]

assert all(fee is not None for fee in [fastest, half_hour, hour, economy, minimum]), "Fee values can't be None."

return {
    "opening": half_hour,
    "mutual_close": half_hour,
    "unilateral_close": fastest,
    "delayed_to_us": half_hour,
    "htlc_resolution": hour,
    "penalty": hour,
    "min_acceptable": economy,
    "max_acceptable": fastest * 10,
}
```