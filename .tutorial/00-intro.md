# Let's Build Sauron: an Esplora Plugin for your CoreLightning Node

Running a bitcoin node is a pain in the butt! (especially with the new inscriptions fad filling up everybody's mempools). Sauron is an opt-in set of tradeoffs you might be interested in if:

1. You want to quickly spin up a corelightning node without running a bitcoin node (pruned or full) for the backend
2. You are unconcerned with trusting a hosted Esplora instance in order to accomplish (1)

For instructions on how to use and deploy CoreLightning nodes on different networks with Sauron, please see the README.md at the root of this repo's file tree.

This tutorial will walk through implementing the Sauron plugin for a core lightning node: first in Python, then in Golang (pending impl), and finally in Rust (pending impl). It's a great way to learn how the Lightning Network operates and CoreLightning's reference implementation and plugin system for programming your own lightning applications

## What is Sauron?

Sauron (originally written by darosier and cdecker) is an alternate backend to the default `bcli` bitcoin plugin that connects your lightning node to a bitcoin core instance. Sauron uses an `esplora` instance like `https://blockstream.com/api`, `https://mempool.space/api` or `https://mutinynet.com/api` to get all the onchain bitcoin data you need to run a lightning node like:

1. Publishing transactions
2. Getting new block data
3. Getting information about the current UTXO set
4. Estimating fees for on chain transactions like channel opens/closes

While Sauron probably isn't the best choice for running a mainnet node with significant funds (although feel free to, MIT License so use this software however you want :) ) , it's EXTREMELY useful for:

1. Quickly spinning up corelightning nodes on Mutinynet or other testnets/signets for side projects
2. Learning the basics of core lightning plugin development
3. Running core lightning nodes on light infrastructure (e.g. running a node out of a free-tier Repl or EC2 instance.)

Again, for just normal documentation see the README at the root, otherwise if you'd like to walk through a tutorial implementing Sauron from scratch, click next!