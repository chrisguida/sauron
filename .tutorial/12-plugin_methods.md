# List of Functions we'll be building:

These are all the plugin methods that `bcli` implements. 

1. `init`: Initializes the Sauron Plugin
3. `getchaininfo`: Get information about the blockchain.
4. `getrawblockbyheight`: Get a raw block's hex data at the given height.
5. `sendrawtransaction`: Send a raw onchain transaction
6. `getutxout`: Get the UTXO at the given transaction ID and output index.
7. `estimatefees`: Estimate fees for various lightning transactions.

In order to fully the `bcli` plugin out for esplora, we'll have to 
1. intercept these wire calls in their specific format
2. return a wire call in the expected format

For the implementation of each method we'll have to make sure that we handle any differences between mempool.space and standard esplora, and we'll write test coverage as we go along. 

Let's begin by writing the plugin's `init` method, the first method called in the plugin lifecycle.