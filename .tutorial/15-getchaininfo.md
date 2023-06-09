# `getchaininfo`

Like we've covered before, the `bcli` plugin we're swapping out is how the Core Lightning node gets all of its information about the blockchain its running against. Lightning is a Layer 2 on top of Bitcoin's Base Layer: the security assumptions of Lightning rely on the node's ability to close its channel in a timely manner if you disagree with your channel partner.

The first call CLN uses is `getchaininfo` to get the blockchain and network configs. This is the pseudocode for the method looks like.

```python
@plugin.method("getchaininfo")
def getchaininfo(plugin, **kwargs):
    """
    Args:
        plugin: The Plugin object.
        kwargs: Additional arguments.

    Returns:
        A dictionary with the following keys:
        - chain: The name of the blockchain (mainnet, signet, mutinynet, testnet, or regtest).
        - blockcount: The current block count.
        - headercount: The current header count.
        - ibd: False (whether or not the node is currently in IBD).

    Raises:
        SauronError: If there is an error fetching the information.
    """
    pass
```

Try implementing it yourself! Read on for implementation details.

## `getchaininfo` Implementation

This method just takes the initialized plugin configuration and returns: `chain`, `blockcount`, `headercount`, and `ibd`. Let's take each of these in turn:

### `chain`: identified by known genesis block

Chain defines WHICH BLOCKCHAIN'S GENESIS BLOCK the lightning node is running against. Bitcoin has several different well-known chains:
1. `mainnet`: the heaviest proof of work bitcoin chain with real value. This is "real" Bitcoin.
2. `testnet`: a test network blockchain with all the same configurations as the mainnet chain, including mining a block approximately every 10 minutes through PoW.
3. `signet` (there are multiple signet) : test network bitcoin chains WITHOUT mining. Blocks are "signed" into existence at some interval by the developer or group of developers running the signet (normally 10 minutes like mainnet but some like mutiny-signet go every 1 minute)
4. `regtest` : a local regression testing environment you run on your local computer.

These different blockchains are identified by the heaviest work chain that builds off their specific genesis blocks. We identify these genesis blocks by their blockhashes, which are copied below:

```python
chains = {
        "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f":
        "main",
        "000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943":
        "test",
        "0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206":
        "regtest"
    }
```

So when our core lightning node asks us to `getblockchaininfo`, it's asking what network it's running on. We can get that information by getting the genesis block for the esplora api endpoint we configured in our plugin `init` method. The genesis block is just the index=0 block in our blockchain so we can do...

```python
genesis_req = f"{plugin.api_endpoint}/block-height/0"
genesis_res = fetch(genesis_req)

if not blockcount_res.status_code == 200:
    raise SauronError(f"Error getting genesis blockhash from \nreq: {genesis_req}\nres: {genesis_res}")
    
if genesis_req.text not in chains.keys():
    raise SauronError(f"Got unsupported genesis blockhash from \nreq: {genesis_req}\nres: {genesis_res}")

chain = chains[genesis_req.text]
# have to set sauron_network for later plugin method calls 
plugin.sauron_network = chain
```

### `blockcount`, `headercount`, and `ibd`: just get the chain tip

When syncing a bitcoin node, the node first gets the complete list of blockheaders that make up the blockchain to verify the proof of work. Once the node verifies it's on the heaviest work chain building off the configured genesis block, the node will get block data for each block from genesis to chain tip to verify that no rules were violated. This is called the `initial block download` or `ibd`. 

During `ibd=true`, the `headercount` will be up to the chain tip (most recent block), but the `blockcount` will only be up to whatever block the node has verified to.

We're not able to hit against an esplora api if it isn't fully synced, so we can just get the most recent chain tip, verify there isn't an error, set `ibd` to false, and set the remaining return values.

```python
chaintip_req = f"{plugin.api_endpoint}/block-height/0"
chaintip_res = fetch(genesis_req) # this just returns an int of the current blockheight
blockheight = chaintip_res.text

if not blockcount_res.status_code == 200:
    raise SauronError(f"Error getting chain tip from \nreq: {chaintip_req}\nGot res: {chaintip_res}")

return {
    "chain": chain,
    "blockcount": blockheight,
    "headercount": blockheight,
    "ibd": False
}

```

## TODO: 
- [ ] Verify that your method works against both blockstream and mempool's esplora APIs, there's sometimes slight differences.
- [ ] Write complete test coverage of the `getchaininfo` method. See the "writing plugin tests" appendix of this tutorial for help
- [ ] There are multiple different signets people might want to use: add support for the `mutiny-signet` by finding its genesis blockhash and adding special handling logic around returning `signet` from `getchaininfo`