import requests
import json

def check():
    response = json.loads(requests.get('https://api.github.com/repos/vicinaehq/vicinae/releases/latest').text)

    import re
    tag: str = response['tag_name']
    match = re.match('v(?P<v>[0-9.]+)$', tag)
    if match is None:
        raise Exception('Unknown tag format')
    v = match.group('v')
    print('New tag:', v)

    prev_v = None
    with open('./prev_v', 'r') as f:
        prev_v = f.read()

    print('Prev tag:', prev_v)

    v_list = list(map(int, v.split('.')))
    prev_v_list = list(map(int, prev_v.split('.')))

    if len(v_list) != len(prev_v_list):
        raise Exception('Tags incompatible')

    with open('./prev_v', 'w') as f:
        _ = f.write(v)
    
    return v if v_list > prev_v_list else None
