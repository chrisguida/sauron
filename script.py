import requests

urls = ['https://blockstream.info/api/fee-estimates',
        'https://mempool.space/api/v1/fees/recommended']

filenames = ['blockstream.txt', 'mempool.txt']

for i in range(len(urls)):
    response = requests.get(urls[i])
    with open(filenames[i], 'w') as file:
        file.write(response.text)