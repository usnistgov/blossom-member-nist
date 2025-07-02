import json
import logging
import os
import time
from enum import Enum
from pprint import pprint

import boto3

# ===============================================

class Environment:

    EC2_INSTANCES   = None
    EC2_CLIENT      = None
    SSM_EC2_CLIENT  = None
    OUR_REGION      = None
    EC2_ID          = None
    @staticmethod
    def set_up() -> None:
        """ Set up necessary environment variables for the lambda to execute
        """
        # ===--- Read lambda environment variables ---===
        Environment.OUR_REGION      = os.environ.get('BLOSSOM_REGION')
        Environment.EC2_ID  = os.environ.get('EC2_INSTANCE_ID')
        # Array in case we need to split members by different EC2 instances
        Environment.EC2_INSTANCES   = [Environment.EC2_ID] 
        Environment.EC2_CLIENT      = boto3.client('ec2', region_name=Environment.OUR_REGION)
        # Create SSM Client
        Environment.SSM_EC2_CLIENT  = boto3.client('ssm')


def run_ec2_commands(command: str):
    """ Run the commands on EC2 from Lambda
    Args:
        file_name (str, optional): The file-name of the new S3-file that triggered event. Defaults to 'X.test'.
        file_dict (str, optional): The dict of the file content. Defaults to {}.
    """
    Environment.set_up()
    print(f'Environment Read\n{"="*64}')
    client = Environment.SSM_EC2_CLIENT
    response = client.send_command(
      
        InstanceIds= Environment.EC2_INSTANCES,
        DocumentName='AWS-RunShellScript',
        Parameters={            
            'commands': [
                ### 1. Run the S3-Bucket Handler
                (f' runuser -l  ec2-user -c "{command}"'),
            ],
            'workingDirectory': ['~/'], # /home/ec2-user
            # 'id': ['BloSS@M-Test'],
            ### !!! The script executes a long-running chunk of work !!! 
            ### !!! Be super-careful playing with the timeout value !!! 
            'executionTimeout':['99'] 
        }
    )
    command_id = response['Command']['CommandId']
    tries = 0
    output = 'False'
    Statuses=[]
    Contexts=[]
    while tries < 100:
        tries = tries + 1
        try:
            time.sleep(0.99)  # some delay always required...
            
            result = client.get_command_invocation(
                CommandId=command_id,
                InstanceId=Environment.EC2_INSTANCES[0] ,
            )
            # print(f"{result['Status']=}")
            # print(f"{result['StandardOutputContent']=}")
            Statuses.append(f"{result['Status']=}")
            Contexts.append(f"{result['StandardOutputContent']=}")
            if result['Status'] == 'InProgress':
                continue
            output = result['StandardOutputContent']
            break
        except client.exceptions.InvocationDoesNotExist:
            continue

    pprint(Statuses)
    pprint(Contexts)
    pprint(result)
    print('\n\n')
    print(f'{"="*64}')
    return(output, Statuses, Contexts)

class Key(Enum):
    ActionType = "type"
#------------------------------------------------------------------------------

class Command(Enum):
    # "Assess" - maps to assess command for assessment results of the particular test
    Assess      = "Assess"
    # "Execute" - maps to predefined command execution (e.g. Cognito pool users list as JSON, etc)
    Execute     = "Execute"
    # "GetUsers" - pulls users from Cognito IDP pool
    Get_Users   = "Get_Users"
    #--------------------------------------------------------------------------
    @staticmethod
    def get_commands() -> list[str]:
        return [x.value.lower() for x in Command]
    #--------------------------------------------------------------------------    
    def get_command_text(self)->str | None:
        if self.value in TEXT_MAP.keys():
            return TEXT_MAP[self.value]
        else:
            return None  
    #--------------------------------------------------------------------------
    def get_key_str(self) -> str:
        return self.value.lower()
#------------------------------------------------------------------------------

TEXT_MAP={
    Command.Assess.value: "aws cognito-idp list-users --user-pool-id us-east-1_wioSQKwya | jq",
    Command.Execute.value: "aws cognito-idp list-users --user-pool-id us-east-1_wioSQKwya | jq",
    Command.Get_Users.value: "aws cognito-idp list-users --user-pool-id us-east-1_wioSQKwya | jq",
}
#------------------------------------------------------------------------------    
def lambda_handler(event, context):

    try:

        event_keys = [ key.lower() for key in event.keys() ]
        event_types = [ value.lower() 
                            if isinstance(key, str) and key.lower()==Key.ActionType.value.lower()
                            else print(f"The {key} object is not of type str, but {type(key)} and {Key.ActionType.value=}")
                            for (key, value) in event.items() 
                        ]
        print(f"{event_keys=}")
        print(f"{list(filter(None,event_types))=}")
        print(f"{Command.Assess.get_command_text()=}")
        if Key.ActionType in event_keys:
            if "Assess" in event_types:
                pass
            elif "Execute" in event_types:
                pass
    except Exception as e:
        print(f"Exception {e}")
    finally:
        print(f"Finally")
    out, x, y = run_ec2_commands(Command.Assess.get_command_text())
    print(f"\n{out=},\n{x},\n{y}")
    return {
        'statusCode': 200,
        'body': json.dumps(out)
    }