#!/usr/bin/env python3
#Time-stamp: <Sat Oct 20 21:25:45 JST 2018 hamada>
from web3 import Web3,HTTPProvider
import sys, time, datetime

if __name__ == "__main__":
    geth_node = 'http://localhost:18545'
    geth_node = 'http://192.168.103.62:18545'
    geth_node = 'http://192.168.103.64:18545'
    geth_node = 'http://192.168.103.202:18545'
    geth_node = 'http://192.168.103.202:28545'
    geth_node = 'http://192.168.103.60:18545'
    geth_node = 'http://192.168.103.100:18545'
    geth_node = 'http://192.168.103.253:18545'


    www3 = Web3(HTTPProvider(geth_node))
    print ("Geth: ", geth_node)

    blockNumber = www3.eth.blockNumber

    print('blockNumber:', blockNumber)

    is_syncing = True

    while is_syncing:
        is_syncing = www3.eth.syncing
        currentBlock = is_syncing.currentBlock
        t = datetime.datetime.now()
        print ("%s, %d"%(t, currentBlock), flush=True)
        time.sleep(60)
