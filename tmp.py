#!/usr/bin/env python3
#Time-stamp: <Sat Oct 20 12:40:28 JST 2018 hamada>
'''
Example: an analysys of the top miners
'''

import web3
import sys

def puts_block(block):
    for key in block:
        print (key, block[key])

if __name__ == "__main__":
    geth_node = 'http://117.102.189.70:18545'  # ropsten node, public primary # Constantinople
    geth_node = 'http://117.102.189.70:28545'  # ropsten node, public secondary # Byzantine
    geth_node = 'http://192.168.103.201:28545' # ropsten node, private # Byzantine
    geth_node = 'http://192.168.103.200:18545' # ropsten node, private # Constantinople # ChainB
    geth_node = 'http://192.168.103.100:18545' # ropsten node, private # Constantinople # ChainB
    geth_node = 'http://192.168.103.202:18545' # ropsten node, private # Constantinople # ChainA
    geth_node = 'http://192.168.103.253:18545' # ropsten node, private # Constantinople # ChainB
    geth_node = 'http://192.168.103.201:18545' # ropsten node, private # Constantinople # ChainA

    provider = web3.HTTPProvider(geth_node)
    www3 = web3.Web3(provider)

    try:
        is_syncing = www3.eth.syncing
        if is_syncing:
            print("Chain hasn't been synced yet.") 
    except:
        print(sys.exc_info())
        print('provider_node:', geth_node)
        exit(-1)

    if True:
        block_last = www3.eth.getBlock('latest')
        #puts_block(block_last)
        bid_last =block_last['number']
        print ("current block#:", bid_last)

        miner_count = {}
        nblock = bid_last - 4230000 + 1
        bid_end   = bid_last
        bid_start = bid_end - nblock + 1
        t_prev = (www3.eth.getBlock(bid_start - 1))['timestamp']

        for i in range(nblock):
            bid = bid_start + i
            block = www3.eth.getBlock(bid)
            try:
                miner = block['miner'].lower()
                if miner not in miner_count:
                    miner_count[miner] = 1
                else:
                    miner_count[miner] += 1
            except:
                print(sys.exc_info())

            t_curr = block['timestamp']
            print (bid, "% 4d"%(t_curr-t_prev), "\t", miner, miner_count[miner] , "\t", block['difficulty'], "\t", www3.toHex(block['hash']) )
            t_prev = t_curr

        miner_list = sorted(miner_count.items(), key=lambda x: -x[1])
        print ()

        print ("----------------------------------------------------------------------")
        print (" %d miners won in the last %d blocks." % (len(miner_list), nblock))
        print (" Range of blocks: %d  - %d" % (bid_start, bid_end))
        print ("----------------------------------------------------------------------")
        print ("Account,                                   count (ratio): balance")
        print ("----------------------------------------------------------------------")
        for k, v in miner_list:
            ratio = v / (nblock * 1.) 
            adr = www3.toChecksumAddress(k) 
            ballance = www3.fromWei(www3.eth.getBalance(adr), "ether")
            print ("%s, %d (%s): %f" %(adr, v, '{:.2%}'.format(ratio), ballance))
