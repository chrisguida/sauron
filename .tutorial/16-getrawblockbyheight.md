# getrawblockbyheight: Check out new blocks for any transactions that affect you and your channels

Your lightning node's channels exist as unspent transaction outputs on chain. Sometimes Core Lightning will need block data to prove whether a transaction exists or has been included in a specific block. It's specifically looking for any transactions included in the newest block in case your channel partner published his transaction: if it was the most recent chain state you're good but if it's a prior state he's stealing from you and you need to publish your justice transaction!

The pseudocode for `getrawblockbyheight` is...

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

Try implementing it yourself! Read on for implementation details.

## `getrawblockbyheight` Implementation

This method takes a `height` parameter so you know which specific block CLN wants you to get data for. Esplora doesn't let us get the rawblock by height directly so we'll do 2 calls: 
1. Get the blockhash by blockheight
2. Get the rawblock by blockhash

For error handling we'll return Nones if we can't find the blockhash at all, and implement a retry loop incase the esplora api we're hitting against returns incomplete raw data.

So first we get the blockhash, then use that to get the rawblock
```python 
blockhash_req = f"{plugin.api_endpoint}/block-height/{height}"
blockhash_res = fetch(blockhash_req)
if blockhash_req.status_code != 200:
    # blockhash not found at all, return Nones
    return {
        "blockhash": None,
        "block": None,
    }

rawblock_req = f"{plugin.api_endpoint}/block/{blockhash_res.text}/raw"
# Use a retry loop incase Esplora returns incomplete blockdata
while True:
    rawblock_res = fetch(rawblock_url)
    if not rawblock_res.status_code == 200:
        # rawblock not found at all, return Nones
        return {
            "blockhash": None,
            "block": None,
        }
    # Check full raw block data content was returned
    content_len = block_req.headers.get("Content-length")
    if content_len is None or int(content_len) == len(block_req.content):
        break
    
    plugin.log("Esplora returned an incomplete block, retrying in 2s", level="error")
    time.sleep(2)

return {
        "blockhash": blockhash_req.text,
        "block": block_req.content.hex(), # need to return as hex for compatibility with CLN's expected return
    }
```

## TODO: 
- [ ] Verify that your method works against both blockstream and mempool's esplora APIs, there's sometimes slight differences.
- [ ] Write complete test coverage of the `getrawblockbyheight` method. See the "writing plugin tests" appendix of this tutorial for help.
- [ ] Write a test that passes back an incomplete block and assert that your method actually does the retry correctly.