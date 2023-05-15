#!/usr/bin/env python3
import requests
import sys
import time

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from art import sauron_eye
from pyln.client import Plugin

plugin = Plugin(dynamic=False)
plugin.sauron_socks_proxies = None
plugin.sauron_network = "test"


class SauronError(Exception):
    """Exception raised when there is an error in the Sauron plugin."""
    pass


def fetch(url):
    """Fetch a URL with retry and proxy support.

    Args:
        url: The URL to fetch.

    Returns:
        The response object.

    Raises:
        SauronError: If there is an error fetching the URL.
    """
    # FIXME: Maybe try to be smart and renew circuit to broadcast different
    # transactions ? Hint: lightningd will agressively send us the same
    # transaction a certain amount of times.
    session = requests.session()
    session.proxies = plugin.sauron_socks_proxies
    retry_strategy = Retry(backoff_factor=1,
                           total=10,
                           status_forcelist=[429, 500, 502, 503, 504],
                           method_whitelist=["HEAD", "GET", "OPTIONS"])
    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session.get(url)


@plugin.init()
def init(plugin, options, configuration, **kwargs):
    """Initialize the Sauron plugin.

    Args:
        plugin: The Plugin object.
        options: The command line options passed to the plugin.
        configuration: The lightningd configuration.
        kwargs: Additional arguments.

    Raises:
        SauronError: If the sauron-api-endpoint option is not specified.
    """
    plugin.api_endpoint = options["sauron-api-endpoint"]
    if not plugin.api_endpoint:
        raise SauronError(
            "You need to specify the sauron-api-endpoint option.")
        sys.exit(1)

    if options["sauron-tor-proxy"]:
        address, port = options["sauron-tor-proxy"].split(":")
        socks5_proxy = "socks5h://{}:{}".format(address, port)
        plugin.sauron_socks_proxies = {
            "http": socks5_proxy,
            "https": socks5_proxy,
        }
        plugin.log("Using proxy {} for requests".format(socks5_proxy))

    plugin.log("Sauron plugin initialized")
    plugin.log(sauron_eye)


@plugin.method("getchaininfo")
def getchaininfo(plugin, **kwargs):
    """Get information about the blockchain.

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
    blockhash_url = "{}/block-height/0".format(plugin.api_endpoint)
    blockcount_url = "{}/blocks/tip/height".format(plugin.api_endpoint)
    chains = {
        "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f":
        "main",
        "000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943":
        "test",
        "0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206":
        "regtest"
    }

    genesis_req = fetch(blockhash_url)
    if not genesis_req.status_code == 200:
        raise SauronError("Endpoint at {} returned {} ({}) when trying to "
                          "get genesis block hash.".format(
                              blockhash_url, genesis_req.status_code,
                              genesis_req.text))

    blockcount_req = fetch(blockcount_url)
    if not blockcount_req.status_code == 200:
        raise SauronError("Endpoint at {} returned {} ({}) when trying to "
                          "get blockcount.".format(blockcount_url,
                                                   blockcount_req.status_code,
                                                   blockcount_req.text))
    if genesis_req.text not in chains.keys():
        raise SauronError("Unsupported network")
    plugin.sauron_network = chains[genesis_req.text]

    # We wouldn't be able to hit it if its bitcoind wasn't synced, so
    # ibd = false and headercount = blockcount
    return {
        "chain": plugin.sauron_network,
        "blockcount": blockcount_req.text,
        "headercount": blockcount_req.text,
        "ibd": False,
    }


@plugin.method("getrawblockbyheight")
def getrawblock(plugin, height, **kwargs):
    """
    Get a raw block at the given height.

    Args:
        plugin: The plugin instance.
        height: The block height.
        kwargs: Additional arguments.

    Returns:
        A dictionary with the following keys:
        - blockhash: The hash of the requested block.
        - block: The raw block in hexadecimal format.

    Raises:
        None.
    """
    blockhash_url = "{}/block-height/{}".format(plugin.api_endpoint, height)
    blockhash_req = fetch(blockhash_url)
    if blockhash_req.status_code != 200:
        return {
            "blockhash": None,
            "block": None,
        }

    block_url = "{}/block/{}/raw".format(plugin.api_endpoint,
                                         blockhash_req.text)
    while True:
        block_req = fetch(block_url)
        if block_req.status_code != 200:
            return {
                "blockhash": None,
                "block": None,
            }
        # We may download partial/incomplete files for Esplora. Best effort to
        # not crash lightningd by sending an invalid (trimmed) block.
        # NOTE: this will eventually be fixed upstream, at which point we should
        # just reuse the retry handler.
        content_len = block_req.headers.get("Content-length")
        if content_len is None:
            break
        if int(content_len) == len(block_req.content):
            break
        plugin.log("Esplora gave us an incomplete block, retrying in 2s",
                   level="error")
        time.sleep(2)

    return {
        "blockhash": blockhash_req.text,
        "block": block_req.content.hex(),
    }


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

    Raises:
        None.
    """
    sendtx_url = "{}/tx".format(plugin.api_endpoint)

    sendtx_req = requests.post(sendtx_url, data=tx)
    if sendtx_req.status_code != 200:
        return {
            "success": False,
            "errmsg": sendtx_req.text,
        }

    return {
        "success": True,
        "errmsg": "",
    }


@plugin.method("getutxout")
def getutxout(plugin, txid, vout, **kwargs):
    """
    Get the UTXO at the given transaction ID and output index.

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
    gettx_url = "{}/tx/{}".format(plugin.api_endpoint, txid)
    status_url = "{}/tx/{}/outspend/{}".format(plugin.api_endpoint, txid, vout)

    gettx_req = fetch(gettx_url)
    if not gettx_req.status_code == 200:
        raise SauronError("Endpoint at {} returned {} ({}) when trying to "
                          "get transaction.".format(gettx_url,
                                                    gettx_req.status_code,
                                                    gettx_req.text))
    status_req = fetch(status_url)
    if not status_req.status_code == 200:
        raise SauronError("Endpoint at {} returned {} ({}) when trying to "
                          "get utxo status.".format(status_url,
                                                    status_req.status_code,
                                                    status_req.text))

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


@plugin.method("estimatefees")
def estimatefees(plugin, **kwargs):
    """
    Estimate fees for various lightning transactions.

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

    Raises:
        None.
    """
    feerate_url = "{}/fee-estimates".format(plugin.api_endpoint)

    feerate_req = fetch(feerate_url)
    assert feerate_req.status_code == 200
    feerates = feerate_req.json()
    if plugin.sauron_network == "test":
        # FIXME: remove the hack if the test API is "fixed"
        feerate = feerates.get("144", 1)
        slow = normal = urgent = very_urgent = int(feerate * 10**3)
    else:
        # It returns sat/vB, we want sat/kVB, so multiply everything by 10**3
        slow = int(feerates["144"] * 10**3)
        normal = int(feerates["5"] * 10**3)
        urgent = int(feerates["3"] * 10**3)
        very_urgent = int(feerates["2"] * 10**3)

    return {
        "opening": normal,
        "mutual_close": normal,
        "unilateral_close": very_urgent,
        "delayed_to_us": normal,
        "htlc_resolution": urgent,
        "penalty": urgent,
        "min_acceptable": slow // 2,
        "max_acceptable": very_urgent * 10,
    }


plugin.add_option(
    "sauron-api-endpoint", "",
    "The URL of the esplora instance to hit (including '/api').")

plugin.add_option(
    "sauron-tor-proxy", "",
    "Tor's SocksPort address in the form address:port, don't specify the"
    " protocol.  If you didn't modify your torrc you want to put"
    "'localhost:9050' here.")

plugin.run()
