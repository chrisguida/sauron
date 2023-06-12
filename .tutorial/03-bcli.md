# How `bcli` works (so we know what functionality we're replacing)

These are all the plugin methods that `bcli` implements. It (normally) uses these to interact through the `bitcoin-cli`'s json-rpc to get the information from whatever bitcoin node you're running:

1. `init`: Initializes the Sauron Plugin
3. `getchaininfo`: Get information about the blockchain.
4. `getrawblockbyheight`: Get a raw block's hex data at the given height.
5. `sendrawtransaction`: Send a raw onchain transaction
6. `getutxout`: Get the UTXO at the given transaction ID and output index.
7. `estimatefees`: Estimate fees for various lightning transactions.

In order to fully swap the `bcli` plugin out for our esplora plugin, we'll have to :
1. intercept these wire calls in their specific format
2. return a wire call in the expected format

For the implementation of each method we'll have to make sure that we handle any differences between mempool.space and standard esplora, and we'll write test coverage as we go along. 

Let's begin by writing the plugin's `init` method, the first method called in the plugin lifecycle.

# Complete list of functions we'll be implementing with their inputs/outputs copied below

## Helper Functions

`fetch`: Fetch a URL with retry and proxy support
```python
def fetch(url):
    """
    Args:
        url: The URL to fetch.

    Returns:
        The response object.
    """
    pass
```

## Plugin Setup Methods

`init`: Initializes the Sauron Plugin
```python
@plugin.init()
def init(plugin, options, configuration, **kwargs):
    """
    Args:
        plugin: The Plugin object.
        options: The command line options passed to the plugin.
        configuration: The lightningd configuration.
        kwargs: Additional arguments.

    Returns:
        None
    
    Raises:
        SauronError: If the sauron-api-endpoint option is not specified.
    """
    pass
```

## Plugin Methods

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

