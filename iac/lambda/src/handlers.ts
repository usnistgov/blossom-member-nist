import { APIGatewayEvent, APIGatewayProxyResult } from "aws-lambda";
import { setupNetwork } from "./fabric-network";
import { error } from "console";
import { int } from "aws-sdk/clients/datapipeline";

// const CHANNEL_NAME = process.env.CHANNEL_NAME ?? 'acquisition';
// const CONTRACT_NAME = process.env.CONTRACT_NAME ?? 'blossom';
const CHANNEL_NAME = process.env.CHANNEL_NAME ?? 'blossom-auth';
const CONTRACT_NAME = process.env.CONTRACT_NAME ?? 'blossom-auth-cc';
const F_CONTRACT_NAME = process.env.CONTRACT_NAME ?? 'account';
// -------------------------------------------------------------
const AUTH_CHANNEL = process.env.AUTH_CHANNEL ?? 'blossom-auth';
const AUTH_CONTRACT = process.env.AUTH_CONTRACT  ?? 'blossom-auth';
const BUS_CHANNEL = process.env.BUS_CHANNEL ?? "blossom-asset" ;
const BUS_CONTRACT = process.env.BUS_CONTRACT ?? "blossom-asset";
const THIS_FILE = "handlers.ts";

export type HandlerFunc = (event: APIGatewayEvent, bodyJson: any) => Promise<APIGatewayProxyResult>;

/**
 * 
 * @param error - The external error if present
 * @returns Descriptor of the error location
 */
function pinErrorMsg(error: any = undefined, depth: int = 2):string {  
    const index = (!error ? 2 : ((depth>=0)?depth:1))
    const e = !error ? new Error(): error;
    const regex = /\((.*):(\d+):(\d+)\)$/
    if(e.stack){
        const match = regex.exec(e.stack.split("\n")[index]);
        if (match){
            return `File: ${match[1]} @Ln:${match[2]} Col:${match[3]}\n`;
        }
    }
    return `Couldn't locate Error`
    // return {filepath: match[1], line: match[2],column: match[3]};
  }
/** Provides placement information for the location of the message and origin of the log entry
 *
 * @param specialPrefix - Additional prefix if needed
 * @param depth (default=2) stack diving depth - 2 will point to the correct place
 * @returns String with the CALLERS "FILE: LINE: Col:" location
 */
function pinLocationMsg(specialPrefix = '', depth = 2) {
    const index = (!specialPrefix ? 2 : ((depth >= 0) ? depth : 1));
    const error = new Error();
    const regex = /\((.*):(\d+):(\d+)\)$/;
    if (error.stack) {
        const match = regex.exec(error.stack.split("\n")[index]);
        if (match) {
            return `${specialPrefix ? specialPrefix + '-' : '@'}File: ${match[1]} @Line:${match[2]} Col:${match[3]}\n`;
        }
    }
    return `No Location Found for Caller in Trace-Stack`;
    // return {filepath: match[1], line: match[2],column: match[3]};
}
/**
 * Returns user name from event
 * @param event Original AWS API-GAteway Event
 * @returns User-Name as string
 */
function getUsername(event: APIGatewayEvent): string {
    const username = event.requestContext.authorizer?.claims.username;
    if (username === undefined || username === null) {
        const error = new Error(  `${pinErrorMsg(new Error())} Could not get username from requestContext`
                           +` (got ${JSON.stringify(event.requestContext.authorizer)})`);
        throw error;
    }
    return username as string;
}

type TransactionRequestBody = {
    function:string;
    functionType:string;
    args: string[];
    // optional in the latest API version
    channel?: string;
    contract?: string;
    functionName?: string;
    transient?: Record<string, string>;
    // Added for debugging
    transaction?:string;
    name?:string;
}

/**
 * Convert string-string map to string-buffer
 * @param transient Request part to convert into buffer
 * @returns buffer-converted object
 */
function convertTransientToBuffer(transient: Record<string, string>) {
    return Object.keys(transient).reduce<{
        [key: string]: Buffer;
    }>((acc, key) => {
        acc[key] = Buffer.from(transient[key]);
        return acc;
    }, {})
}

/**
 * 
 * @param event 
 * @param bodyJson 
 * @param type 
 * @returns 
 */
const transactionHandler = async (event: APIGatewayEvent, bodyJson: any, type: 'query' | 'invoke'): ReturnType<HandlerFunc> => {
    console.log(`${THIS_FILE}:${pinLocationMsg('0. Setting up NAME...')}@transactionHandler`);
    // TODO: 1. verify that function name contains f_contract_name. 
    // E.g. 'account:', 'account:' etc

    const body = bodyJson as TransactionRequestBody;
    // TODO: 2. Replace the constants with a map resolution 
    // of the Channel/Chaincode/Contract resolution 
    // mapped to the actual chaincode content
    body.channel = CHANNEL_NAME;
    body.contract = CONTRACT_NAME;
    
    // Only debugging assignments for now     
    body.functionName =  !body.function?'account:getAccounts': body.function;
    body.name = "getAccounts";
    body.transaction = "dValue";    
    const username = getUsername(event);
    // End of TODO

    // -------------------------------
    // Setting Up NETWORK for CHANNEL
    // -------------------------------
    /* Original Definition of the Network Interface:
    export interface Network {
        getGateway(): Gateway;
        getContract(chaincodeId: string, name?: string): Contract;
        getChannel(): Channel;
        addCommitListener(listener: CommitListener, peers: Endorser[], transactionId: string): Promise<CommitListener>;
        removeCommitListener(listener: CommitListener): void;
        addBlockListener(listener: BlockListener, options?: ListenerOptions): Promise<BlockListener>;
        removeBlockListener(listener: BlockListener): void;
        }
    */
    console.log(`${THIS_FILE}:${pinLocationMsg('1. Set NETWORK...')}@transactionHandler`
                +`\n${JSON.stringify(body, null, 2)}`);
    const network = await setupNetwork(username, body.channel);
    console.log(`${pinLocationMsg('2. NETWORK Set!!!')}`
                +`\nChannel Info:\n Contract-channel: ${body.channel}`
                +`\n Contract-name: ${body.contract}`
                +`\n User: ${username}`
            );

    // -------------------------------
    // Setting Up CONTRACT for NETWORK on the CHANNEL
    // -------------------------------
    /*
    export interface Contract {
        readonly chaincodeId: string;
        readonly namespace: string;
        createTransaction(name: string): Transaction;
        deserializeTransaction(data: Buffer): Transaction;
        evaluateTransaction(name: string, ...args: string[]): Promise<Buffer>;
        submitTransaction(name: string, ...args: string[]): Promise<Buffer>;
        addContractListener(listener: ContractListener, options?: ListenerOptions): Promise<ContractListener>;
        removeContractListener(listener: ContractListener): void;
        addDiscoveryInterest(interest: DiscoveryInterest): Contract;
        resetDiscoveryInterests(): Contract;
        }
    */   
    // const transaction = 
    // network.getContract(body.contract)
    //  .createTransaction(body.functionName);
    console.log(`${THIS_FILE}:${pinLocationMsg('3. Set CONTRACT...')}`+
                `\nNETWORK:\nBody-Contract: ${body.contract}`);
    const contract = network.getContract( body.contract);
    console.log(`${THIS_FILE}:${pinLocationMsg('4. CONTRACT Set!!!')}`+
                `\nCONTRACT:`
                +`\n Chaincode-ID[chaincodeId]: ${contract.chaincodeId}`
                +`\n Namespace[namespace]:  ${contract.namespace}`);


    // -------------------------------
    // Setting up TRANSACTION            
    // -------------------------------
    /*
    export declare class Transaction {
        private readonly name;
        private readonly contract;
        private transientMap?;
        private readonly gatewayOptions;
        private eventHandlerStrategyFactory;
        private readonly queryHandler;
        private endorsingPeers?;
        private endorsingOrgs?;
        private readonly identityContext;
        ....
        getName(): string;
        getTransactionId(): string;
        }
     */
    console.log(`${THIS_FILE}:${pinLocationMsg('5. Set TRANSACTION...')}`
                +`\nTRANSACTION:\nFunctio-nName: ${body.function}`);
    const transaction = contract.createTransaction(body.function);    
    console.log(`${THIS_FILE}:${pinLocationMsg('6. TRANSACTION SET!!!...')}`
                +`\nTRANSACTION:`
                +`\n Transaction-Object: ${transaction}`
                +`\n TR-getName: ${transaction.getName()}`
                +`\n TR-getTranID: ${transaction.getTransactionId()}`
            );

    if (body.transient) {
        transaction.setTransient(convertTransientToBuffer(body.transient));
    }

    transaction.setEndorsingOrganizations(network.getGateway().getIdentity().mspId);
    console.log('Evaluating/submitting transaction...');
    try {
        let result;
        if (type === 'query') {
            result = await transaction.evaluate(...body.args);
        } else {
            result = await transaction.submit(...body.args);
        }
        return {
            body: result.toString(),
            headers: {
                'Content-Type': 'application/json'
            },
            statusCode: 200
        };
    } catch (e) {
        return {
            body: `${pinErrorMsg(e)} Error: ${e}`,
            headers: {},
            statusCode: 500,
        }
    } finally {
        network.getGateway().disconnect();
    }
}

export const queryHandler: HandlerFunc = (event, bodyJson) => transactionHandler(event, bodyJson, 'query');
export const invokeHandler: HandlerFunc = (event, bodyJson) => transactionHandler(event, bodyJson, 'invoke');
export const pinError = (error: any)=> pinErrorMsg(error);
export const pinLocation = (message: string) => pinLocationMsg(message);