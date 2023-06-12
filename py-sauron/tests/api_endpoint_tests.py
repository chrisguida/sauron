import requests

supported_sauron_api_endpoints = {
    blockstream_mainnet: "https://blockstream.info/api",
    mempool_mainnet: "https://mempool.space/api",
    blockstream_testnet: "https://blockstream.info/testnet/api",
    mempool_testnet: "https://mempool.space/testnet/api",
    mempool_signet: "https://mempool.space/signet/api",
    mutiny_signet: "https://mutinynet.com/api",
}

for k,v in supported_sauron_api_endpoints:
    genesis_req = f"{v}/block-height/0"
    genesis_res = fetch(genesis_req)
    
    chaintip_req = f"{v}/blocks/tip/height"
    chaintip_res = fetch(genesis_req)
    
    blockhash_req = f"{v}/block-height/{chaintip_res.text}"
    blockhash_res = fetch(blockhash_req)
    
    rawblock_req = f"{v}/block/{blockhash_res.text}/raw"
    rawblock_res = fetch(rawblock_url)

    
