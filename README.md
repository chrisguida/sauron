## Sauron

A Bitcoin backend plugin relying on [Esplora](https://github.com/Blockstream/esplora).


### About

It allows Core Lightning to run without needing a *local* `bitcoind`, and can be either self-hosted (Esplora is Open Source, and self hosting it is basically a `docker` one-liner) or hit against a public esplora API.


### Run

You need to:
- disable the default Bitcoin backend (`bcli`)
- register sauron
- provide the API endpoint you want to use

Here is a fully reptilian example running against [blockstream.info](https://blockstream.info/):

```
lightningd --mainnet --disable-plugin bcli --plugin $PWD/sauron.py --sauron-api-endpoint https://blockstream.info/api/
```

You can use also proxy your requests through [Tor](https://www.torproject.org/) by
specifying a SOCKS proxy to use with the `--sauron-tor-proxy` startup option, in
the form `address:port`.

Hidden services are also supported :
```
lightningd --testnet --disable-plugin bcli --plugin $PWD/sauron.py --sauron-tor-proxy localhost:9050 --sauron-api-endpoint http://explorerzydxu5ecjrkwceayqybizmpjjznk5izmitf2modhcusuqlid.onion/testnet/api/
```