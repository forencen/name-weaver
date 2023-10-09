import random
import time
import uuid

import requests
import json

temp_str = "0x73d5B2f081ceDf63A9e660a22088C7724aF78774,0xdAC17F958D2ee523a2206206994597C13D831ec7,{value},{uuid}"

headers = {
    'Content-Type': 'application/json'
}


def post_to_redis(data):
    url = "http://8.134.163.70:8001/list_set_data/batch"
    response = requests.request("POST", url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception("status error")


def get_data(keys):
    t1 = time.time()
    keys = set(keys)
    url = "http://8.134.163.70:8001/get_batch"
    mapping = {}
    count = 0
    while keys:
        response = requests.request("POST", url, headers=headers, json=list(keys))
        res = response.json()
        res_data = res['data']
        for key, value in res_data.items():
            if value:
                mapping[key] = value
            keys = keys - mapping.keys()
        if keys:
            time.sleep(0.2)
            count += 1
        if count > 15:
            break
    print(f'{time.time() - t1} {len(mapping)}')
    return mapping


def test():
    gen_keys = [uuid.uuid4().hex for _ in range(20)]
    gen_value = [random.randint(10000000, 1000000000) for _ in range(20)]
    data = [{
        "key": "wait_handler_token_pair",
        "value": temp_str.format(value=value, uuid=key)
    } for key, value in zip(gen_keys, gen_value)]
    post_to_redis(data)
    print(get_data(gen_keys))


if __name__ == '__main__':
    for _ in range(50):
        test()
