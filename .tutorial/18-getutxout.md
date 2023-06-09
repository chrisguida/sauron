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

Another easy one so let's take this opportunity to explore how bitcoin transactions are structured while we work through it!

### A little digression on spent/unspent txouts

This method takes a `txid` and a `vout`. Transactions are uniquely identified by their `txid` which is the hash256 (2 rounds of sha256) of the raw transaction (excluding the witness data). Transactions can have many inputs and many outputs, we call them vectors of inputs/outputs or `vins` and `vouts`. So you can use the `txid` and the `vout` to identify a specific output on the bitcoin blockchain.

Outputs of previous bitcoin transactions can be used as inputs to new bitcoin transactions, so once an output is used as an input it is "spent" and cannot be used in any other transactions (that would be a "double spend").

The current supply of bitcoin can be calculated as the set of "unspent" transaction outputs, or what we call the `utxo set`.

### Getting the TX by `txid`

Let's get the raw transaction data from mempool:

```python
gettx_url = f"{plugin.api_endpoint}/tx/{txid}"
gettx_res = fetch(gettx_url)
if not gettx_res.status_code == 200:
    raise SauronError(f"Error getting transaction from \nurl: {gettx_url}\nres: {genesis_res}")
```

But this data isn't enough! We need to figure out whether the specific vout we're looking for has been spent yet. Just having the transaction means nothing: the tx could be valid but not yet in a block, or it could've been included in an earlier block and been spent by a follow on tx.

We can just ask esplora whether or not this tx has been spent, but take note that this is where you are absolutely trusting the esplora api_endpoint you're using: if they pass you garbage data, you will absolutely lose money and not be able to assess whether your channels are really live!

### Getting the outpoint (txid:vout) status

If the outpoint is spent we're just going to return `Nones` which will trigger Core Lightning to publish the justice transaction, if unspent then we're good.

```python
status_url = f"{gettx_url}/outspend/{vout}"
status_res = fetch(status_url)
if not gettx_res.status_code == 200:
    raise SauronError(f"Error getting outpoint status from \nurl: {gettx_url}\nres: {genesis_res}")

if status_req.json()["spent"]:
    return {
        "amount": None,
        "script": None,
    }

txo = gettx_req.json()["vout"][vout]
return {
    "amount": txo["value"],
    "script": txo["scriptpubkey"],
}
```

## TODO: 
- [ ] Verify that your method works against both blockstream and mempool's esplora APIs, there's sometimes slight differences.
- [ ] Write complete test coverage of the `getutxout` method. See the "writing plugin tests" appendix of this tutorial for help.
