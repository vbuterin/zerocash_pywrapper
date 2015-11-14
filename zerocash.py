import subprocess
import sys
import os
import json
import pipes

DEFAULT_CONF = """
connect=46.105.126.215:29000
dnsseed=0
keypool=10
listen=1
port=29000
regtest=1
relaypriority=0
rpcpassword=123
rpcport=29001
rpcuser=admin
server=1
upnp=0
"""

path = os.path.join(os.path.expanduser('~'), 'zcalpha')

if not os.path.exists(path):
    os.mkdir(path)
    open(os.path.join(path, 'bitcoin.conf'), 'w').write(DEFAULT_CONF)

x = subprocess.Popen(["zerocashd", "-datadir="+path, "-daemon"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)

def run_command(command, *args):
    p = subprocess.Popen(["zerocash-cli", "-datadir="+path, command] + list(args), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if stderr:
        raise Exception(stderr)
    return stdout

def json_encode(obj):
    o = json.dumps(obj)
    return o.replace("t", "\\x74").replace("u", "\\x75").replace("f", "\\x66").replace(' ', '')

def keygen():
    return json.loads(run_command('zc-raw-keygen'))

def getnewaddress():
    return run_command('getnewaddress').strip()

def generate_coins():
    return json.loads(run_command('setgenerate', 'true', '50'))

def get_spendable_coins():
    coins = json.loads(run_command('listunspent'))
    return [{'txid': coin['txid'], 'vout': coin['vout']} for coin in coins]

def createrawtransaction(inputs, to, value):
    if not isinstance(inputs, list):
        inputs = [inputs]
    return run_command('createrawtransaction',
                                  json_encode(inputs), json_encode({to: value})).strip()
    
def raw_protect(tx, addr, value):
    return json.loads(run_command('zc-raw-protect', tx, addr, str(value)))

def decode(tx):
    return json.loads(run_command('decoderawtransaction', tx))

def sign(tx):
    return json.loads(run_command('signrawtransaction', tx))['hex']

def send(tx):
    return run_command('sendrawtransaction', tx)

def zc_keygen():
    return json.loads(run_command('zc-raw-keygen'))

def pour(secret1, bucketsecret1, secret2, bucketsecret2, output1, value1, output2, value2, output_pub, value_pub):
    return json.loads(run_command('zc-raw-pour', secret1, bucketsecret1, secret2, bucketsecret2, output1, str(value1), output2, str(value2), output_pub, str(value_pub)))
