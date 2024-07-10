const bitcoin = require('bitcoinjs-lib');
const bchLib = require('bitcore-lib-cash');

export function getAddressFromIndex(xpub, index) {
    // Decode the xpub
    const node = bitcoin.bip32.fromBase58(xpub);

    // Derive the child node at the given index
    const child = node.derive(0).derive(index);

    // Get the public key
    const { address } = bitcoin.payments.p2pkh({ pubkey: child.publicKey });

    // Convert to Bitcoin Cash address
    const cashAddr = new bchLib.Address(address).toCashAddress();

    return cashAddr;
}
