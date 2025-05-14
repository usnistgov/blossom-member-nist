#!/usr/bin/env python3

import os
import subprocess
import textwrap
from enum import Enum
from posixpath import expanduser

from aws_cli_helper import APP, CLI, Level


class Prerequisites:

    def IsOktaCliInstalled() -> bool:
        # Run octa-aws-cli and check the return ode and output
        return os.path.exists("")
#==============================================================================


class Environment:
    """ Aggregates all environment settings for single-source use
    """
    # region: The default AWS region that this script will connect to for all API calls
    region = os.environ.get('AWS_DEFAULT_REGION', os.environ.get('AWS_REGION', 'us-east-1'))
    
    # awsconfigfile: The file where this script will store the temp credentials under the saml profile
    filename = os.environ.get('AWS_SHARED_CREDENTIALS_FILE', f"{expanduser('~')}/.aws/credentials")

    # blossom-dev: The name of section in okta file
    section = os.environ.get('AWS_PROFILE_SECTION', 'blossom-dev')

    # SSL certificate verification: Whether or not strict certificate verification is done, False should only be used for dev/test
    ssl_verification = os.environ.get('IDP_VERIFY_TLS', True)

    realm = os.environ.get('IDP_REALM', 'nist')
    uid = os.environ.get('IDP_USER')
    password = os.environ.get('IDP_PASS')
#==============================================================================

class ProcessRunner:

    def __init__(self, ) -> None:
        super().__init__()
        self.result: str = None
        self.out: str = None
        self.error: str = None
        self.code: str = None
        self.quiet_mode: bool = False
        self.reset_status()
    # -------------------------------------------------------------------------

    def reset_status(self):
        """ Simple reset of the status-state variables
        """
        self.result: str = None
        self.out: str = None
        self.error: str = None
        self.code: str = None
    # -------------------------------------------------------------------------

    def report_command_status(self, command, quiet_mode = False, depth:int =5):
        if self.error and self.code!=0:
            CLI.pin_error(f'Command: {self.get_command_text(command)}\n{self.result=}\n{self.error=}\n{self.code=}\n', depth=depth)
        elif not quiet_mode:
            CLI.cmd_status(self.get_command_text(command),str(self.result), str(self.error), self.code, stack_depth=depth)
    # -------------------------------------------------------------------------

    def run_command( self, 
                     command: list,
                     output_extractor: callable = None,                     
                ) -> tuple[str, str, int]:
        if command and isinstance(command, list) and len(command)>0:
            proc = None
            try:
                proc = subprocess.run(command, encoding='utf-8', 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE, 
                                    stdin=subprocess.PIPE)
                ### If called needs post-processing of output
                ### (e.g. YAML/JSON parsing of the output)
                if output_extractor and callable(output_extractor) :
                    self.result = output_extractor(proc.stdout)
                else:
                    self.result = proc.stdout
            except Exception as ex:
                self.error = f"Command \n\t{command}\nFailed with exception: \n\t{ex}"
                self.code = f"-101"
            finally:
                # Finalize information gathering
                if proc:
                    self.result=proc.stdout
                    self.error=proc.stderr
                    self.code=proc.returncode
        else:
            self.error = f"No Command!!!"
            self.code = f"-1010"

        return (self.result, self.error, self.code)
    # -------------------------------------------------------------------------
#==============================================================================


class OktaSettings:
    OKTA_CONFIGURATION_FILE = "~/.okta/okta.yaml"
    OKTA_FILE_SECTION_NAME = "blossom-saml"
    OKTA_INIT_LOGIN_COMMAND = ["okta-aws-cli", "web", "--profile", "blossom-dev"]
    OKTA_BASE_COMMAND = ["okta-aws-cli"]
    OS_UNAME_OS_NAME = ["uname"]
    OS_UNAME_OS_CPU = ["uname", "-m"]  # x86_64, arm64
#==============================================================================

class OktaOps:
    """
    Sample the content in  ~/.aws/credentials
    """

    @staticmethod
    def exists_okta_config_file(
            possibly_file: str = OktaSettings.OKTA_CONFIGURATION_FILE,
            ) -> bool:
        """True if the file exists and False - otherwise
        Args:
            possibly_file (str, optional): OKTA config file name. Defaults to OKTA_CONFIG_FILE.
        Returns:
            bool: true if file exists and is file    """
        return os.path.exists(possibly_file) and os.path.isfile(possibly_file)
    #--------------------------------------------------------------------------

    @staticmethod
    def exists_required_section( section_name: str, 
                                 section_entries: list
                                ) -> bool:
        compliant_section = True

        return compliant_section
    #--------------------------------------------------------------------------

    @staticmethod
    def insert_okta_file_section(
            okta_file: str = OktaSettings.OKTA_CONFIGURATION_FILE, 
            section_name: str = OktaSettings.OKTA_FILE_SECTION_NAME,
            ) -> None:
        """ Reads and modifies OKTA YAML file if the section does not exist
        Args:
            section_name (str, optional): OKTA SECTION NAME. Defaults to OKTA_FILE_SECTION_NAME.
        """
        if OktaOps.exists_okta_config_file():
            pass
    #--------------------------------------------------------------------------
#==============================================================================

def print_proc_status(cmd_output: str, error_text: str, error_code: int) -> None:
    print(f"\n\t{cmd_output=}\n\t${error_text=}\n\t${error_code=}")

if __name__ == "__main__":
    proc = ProcessRunner() # Create a process  
    # OKTA Login Extra Steps (since May 1, 2025):

    # 0. Assure that there is a ~/.okta.okta.yaml is populated as follows or at least contains 
    # saml (or maybe `blossom`) section in the YAML 
    """
    ---
    awscli:
    profiles:
        ...
        ...
        # Tht's the section we need for the 
        blossom-dev:
        aws-region: "us-east-1"
        aws-acct-fed-app-id: "ALPHA_NUMERIC_STRING"
        oidc-client-id: "ALPHA_NUMERIC_STRING"
        org-domain: "login.nist.gov"
        write-aws-credentials: true
        open-browser: true
        ...
        ...
"""
    # 1. Call `okta-aws-cli web --profile saml` (maybe blossom instead of saml)

    (cmd_output, error_text, error_code)=proc.run_command(OktaSettings.OKTA_BASE_COMMAND)
    if error_code==0:
        (cmd_output, error_text, error_code)=proc.run_command(OktaSettings.OKTA_INIT_LOGIN_COMMAND)
        # print(f"\n\t{cmd_output=}\n\t${error_text=}\n\t${error_code=}")
        print_proc_status(cmd_output, error_text, error_code)
    else:
        if error_code==-101 or error_code==127:
            (os_name, error_text, error_code)=proc.run_command(OktaSettings.OS_UNAME_OS_NAME)
            print_proc_status(cmd_output, error_text, error_code)
            if os_name.strip()=='Darwin':    
                # MacOS Installation
                print(textwrap.dedent(
                        """
                        On MacOS you can install okta-aws-cli by running the following command:

                        \tbrew install okta-aws-cli
                        """
                        )
                    )
        else:
            print(f"\nFailed to find {OktaSettings.OKTA_BASE_COMMAND[0]}\n\t{cmd_output=}\n\t${error_text=}\n\t${error_code=}")
    # 2. Use `aws sts get-caller-identity --profile saml | jq...` to verify that the token is still valid 
