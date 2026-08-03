


    console.log(`${THIS_FILE}:${(0, exports.pinLocation)('Setting up NAME...')}`);
    // Setting Up NAME
    const body = bodyJson;
    // TODO: Replace the constants with a map resolution 
    // of the Channel/Chaincode/Contract resolution 
    // mapped to the actual chaincode content
    body.channel = CHANNEL_NAME;
    body.chaincode = CHAINCODE_NAME;
    body.contract = CONTRACT_NAME;
    // End of TODO
     body.name = "getAccounts";
    body.transaction = "dValue";
    body.functionName = !body.function ? 'GetAccounts' : String(body.name).charAt(0).toUpperCase() + String(body.name).slice(1);
    const username = getUsername(event);
    console.log(`${THIS_FILE}:${(0, exports.pinLocation)('Done Setting up NAME-TRAN-BODY...')}\nBody1:\n${JSON.stringify(body, null, 2)}`);
    
    // Setting Up CHANNEL
    console.log(`${THIS_FILE}:${(0, exports.pinLocation)('Setting up CHANNEL...')} on channel ${body.channel} for User: ${username}`);
    const network = await (0, fabric_network_1.setupNetwork)(username, body.channel);
    console.log(`${THIS_FILE}:${(0, exports.pinLocation)('CHANNEL is SET!!!...')}\nChannel Info:\n Contract-channel: ${body.channel}\n Contract-name: ${body.contract}\n User: ${username}`);
    
    // Setting up CONTRACT
    console.log(`${THIS_FILE}:${(0, exports.pinLocation)('Setting up NETWORK...')}\nSetting up NETWORK...\nBody-Contract: ${body.contract}`);
    const contract = network.getContract( body.contract); //body.chaincode,  /* Added Jun-12-25*/ 
    console.log(`${THIS_FILE}:${(0, exports.pinLocation)('NETWORK SET!!!...')} Setting up Transaction...\nContract-Object: ${contract}`);
    
    // Setting up TRANSACTION
    console.log(`${THIS_FILE}:${(0, exports.pinLocation)('Setting up TRANSACTION...')}\nTRANSACTION:\nFunctio-nName: ${body.functionName}`);
    const transaction = contract.createTransaction(body.functionName);
    console.log(`${THIS_FILE}:${(0, exports.pinLocation)('TRANSACTION is SET!!!...')}\nTRANSACTION:\nTransaction-Object: ${transaction}`);
    if (body.transient) {
        transaction.setTransient(convertTransientToBuffer(body.transient));
    }