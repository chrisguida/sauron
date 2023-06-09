# How `bcli` works (so we know what functionality we're replacing)

So here's everything that `bcli` does:

### `bcli` Plugin Methods:

1. `getchaininfo`

"""Get information about the blockchain.

Returns:
    A dictionary with the following keys:
    - chain: The name of the blockchain (main, test, or regtest).
    - blockcount: The current block count.
    - headercount: The current header count.
    - ibd: False (whether or not the node is currently doing the initial block download (if blockcount != headercount, esplora's node still syncing)).

Example Return:

{
    "chain": "signet",
    "blockcount": 123456,
    "headercount": 123456,
    "ibd": False,
}

"""

2. `getrawblockbyheight`

```
"""Get a raw block at the given height.

Args:
    plugin: The plugin instance.
    height: The block height.
    kwargs: Additional arguments.

Returns:
    A dictionary with the following keys:
    - blockhash: The hash of the requested block.
    - block: The raw block in hexadecimal format.

Example Return:

{
    "blockhash": blockhash_req.text,
    "block": block_req.content.hex(),
}
```