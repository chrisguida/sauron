# So what are we implementing anyway?

We're going to write a corelightning plugin that intercepts all the wire messages that the lightning daemon tries to ask the bitcoin node, go get the information from an esplora instance, and return the data to the lightning node as if it came from the bitcoin node.

## Brief Lightning 'Splainer

The Lightning Network is a Layer 2 payment channel protocol on top of Bitcoin's base layer settlement network. You open lightning channels with an on-chain transaction locking bitcoin to a 2/2 Multisig with your channel peer. You & your channel peer each hold asymmetric transactions which you can update as fast as you can communicate to sling payments back and forth. For a more in depth overview of the Lightning Network, I encourage you to check out these resources:

1. [Mastering the Lightning Network](https://github.com/lnbook/lnbook)
2. []
3. c

For our purposes, what we need to know is that running a Lightning Node on this layer 2 requires you to know a bunch of information about the current state of Bitcoin at layer 1: 

1. Is your channel still open? has your peer published their closing TX?
2. Have they published an old channel state to try to steal your funds?
3. What are the feerates we should use for our channel updates?

The way lightning nodes normally answer these questions is by running alongside a bitcoin node (full or pruned).

Bitcoin Nodes are relatively easy to run, especially pruned nodes, but generally require:
1. A couple gbs for the UTXO set
2. 300mb for the mempool
3. 6-600gb of harddrive space (depending on whether you're running a maximally-pruned, partially pruned, or full node and what indexes you set up)

This isn't all that much but it's _slightly_ too large for free-tier services through Replit and EC2 if you want to just quickly spin up nodes, so Sauron's really useful for getting a lightning node up in those circumstances. Let's get started!

