#!/usr/bin/env python3
#Time-stamp: <Thu Oct 18 14:03:42 JST 2018 hamada>
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
    geth_node = 'http://192.168.103.200:18545' # ropsten node, private # Constantinople #ChainB
    geth_node = 'http://192.168.103.201:28545' # ropsten node, private # Byzantine
    geth_node = 'http://192.168.103.202:18545' # ropsten node, private # Constantinople # ChainA
    geth_node = 'http://192.168.103.201:18545' # ropsten node, private # Constantinople # ChainA
    geth_node = 'http://192.168.103.61:18545' # ropsten node, private # Constantinople # ChainB



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

        block_latest = www3.eth.getBlock('latest')
        #puts_block(block_latest)
        bnum_latest =block_latest['number']
        print ("current block#:", bnum_latest)

        miner_count = {}

        nblock_end   = bnum_latest
        nblock_start = 4230000
        nblock = nblock_end - nblock_start + 1
        t_next = block_latest['timestamp']

        for i in range(nblock):
            bnum = nblock_end - i
            block = www3.eth.getBlock(bnum)
            try:
                miner = block['miner'].lower()
                if miner not in miner_count:
                    miner_count[miner] = 1
                else:
                    miner_count[miner] += 1
            except:
                print(sys.exc_info())

            t_curr = block['timestamp']
            print ('BLOCK:', bnum, ', --------------------------------------------------------------')
            #print (bnum, "% 4d"%(t_next-t_curr), miner, miner_count[miner])
            print (block)
            t_next = t_curr

        miner_list = sorted(miner_count.items(), key=lambda x: -x[1])
        print ()

        print ("----------------------------------------------------------------------")
        print (" %d miners won in the last %d blocks." % (len(miner_list), nblock))
        print (" Range of blocks: %d  - %d" % (nblock_start, nblock_end))
        print ("----------------------------------------------------------------------")
        print ("Account,                                   count (ratio): balance")
        print ("----------------------------------------------------------------------")
        for k, v in miner_list:
            ratio = v / (nblock * 1.) 
            adr = www3.toChecksumAddress(k) 
            ballance = www3.fromWei(www3.eth.getBalance(adr), "ether")
            print ("%s, %d (%s): %f" %(adr, v, '{:.2%}'.format(ratio), ballance))
