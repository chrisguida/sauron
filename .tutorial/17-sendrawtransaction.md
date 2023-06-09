# sendrawtransaction : Opening/closing channels

Again, the security assumptions and beauty of the Lightning Network is that it is a Layer 2 on top of bitcoin. Your lightning channels are unspent transaction outputs on the base layer blockchain. You and youru channel partners each hold transactions which, if broadcast and included in a block, would let you walk away with whatever amount of money in the channel each of you owned. The `sendrawtransaction` method is how your CLN node opens and closes channels by publishing transactions.

The pseudocode for `sendrawtransaction` is...

```python
@plugin.method("sendrawtransaction")
def sendrawtx(plugin, raw_tx, **kwargs):
    """
    Send a raw transaction.

    Args:
        plugin: The plugin instance.
        raw_tx: The raw transaction.
        kwargs: Additional arguments.

    Returns:
        A dictionary with the following keys:
        - success: True if the transaction was successfully sent, False otherwise.
        - errmsg: An error message, if applicable.
    """
    pass
```

Try implementing it yourself! Read on for implementation details.

## `sendrawtransaction` Implementation

This one's super easy, you're just submitting the passed in `raw_tx` to the esplora instance and passing back whether you succeeded or got an error.

 ```python
 sendtx_req = f"{plugin.api_endpoint}/tx"
 sendtx_res = requests.post(sendtx_req, data=tx) # this one's a post so can't use our fetch helper
 if sendtx_req.status_code != 200:
    return {
        "success": False,
        "errmsg": sendtx_req.text,
    }

return {
    "success": True,
    "errmsg": "",
}
```

## TODO: 
- [ ] Verify that your method works against both blockstream and mempool's esplora APIs, there's sometimes slight differences.
- [ ] Write complete test coverage of the `getrawblockbyheight` method. See the "writing plugin tests" appendix of this tutorial for help.
- [ ] Try submitting an invalid rawtransaction to confirm your error handling works.
- [ ] Extra credit: what happens if you publish an old channel state (one of the previous transactions you were holding that got invlaidated when you made another payment through the channel)?
