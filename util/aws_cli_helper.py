#!/usr/bin/env python3


import logging
import os
from datetime import datetime
from enum import Enum
from pprint import pprint


def get_file_timestamp() -> str:
    return datetime.now().isoformat().replace('-', '').replace(':', '').replace('.', 'p').lower()  
### -------------------------------------------------------------------------------
#==================================================================================

class Level(Enum):
     # ALL < INFO < WARN < ERROR < PROD
    NONE = 0, 
    ALL = 1,
    INFO = 2,
    WARN = 3,
    ERROR = 4,
    PROD = 5,

    @staticmethod
    def get_by_str( value: str) -> Enum:
        try:
            UP = value.upper()
            if UP in Level.__members__.keys():
                return Level[UP]
            return Level.ALL
        except ValueError:
            return Level.ALL

    def call_log_method(self, msg: str) -> None:
        if self==Level.ALL:
            return APP.LOGGER.info(msg)
        elif self==Level.INFO:
            return APP.LOGGER.info(msg)
        elif self == Level.WARN:
            return APP.LOGGER.warning(msg)
        elif self==Level.ERROR:
            return APP.LOGGER.error(msg)
        elif self==Level.PROD:
            return APP.LOGGER.error(msg)
    
    def log_at_level(self, ) -> str:
        if self==Level.ALL:
            return logging.INFO
        elif self==Level.INFO:
            return logging.INFO
        elif self == Level.WARN:
            return logging.WARNING
        elif self==Level.ERROR:
            return logging.ERROR
        elif self==Level.PROD:
            return logging.CRITICAL
    # -----------------------------------------------------------------------------
#==================================================================================

class APP:
    """_summary_ Container for static app-level settings
    """
    PROJECT_NAME = "BloSS🌻M"
    LOGGER: logging.Logger = logging.getLogger(__name__)
    LOG_AT: Level  = Level.ALL
    PRINT_AT: Level = Level.ALL
    LOG_DIR: str = ''
    # ENV_CONFIG: EnvConfig = None

    CMD_ONLY_PRINT: bool = False
    CLI_DEBUG_MODE: bool = False

    @classmethod
    def init_log(cls, 
                 envName: str, 
                 envLog: Level = Level.NONE, 
                 envLogLevel: Level = Level.NONE,
                ) -> None:
        cls.LOG_DIR = envName
        cls.LOG_AT = Level.ALL if envLog==Level.NONE else envLog
        cls.PRINT_AT = Level.ALL if envLogLevel==Level.NONE  else envLogLevel
        if not APP.LOGGER:
            APP.LOGGER = logging.getLogger(__name__)
            CLI.pin_warning("Not initialized APP.LOGGER")            
        log_file = os.path.join(cls.LOG_DIR, f'b@-{get_file_timestamp()}.log' )
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        logging.basicConfig(filename=log_file, level=cls.LOG_AT.log_at_level())
    # -----------------------------------------------------------------------------
    @staticmethod
    def print(info):
        if APP.CLI_DEBUG_MODE:
            print(info)
    # -----------------------------------------------------------------------------
    _DEBUG_LOG_AT_LEVEL=Level.INFO
    _DEBUG_ON=True
    _DETAILS_ON=True
    _DEBUG_DO_LOG=True
    _DEBUG_DO_CLI=True
    _DEBUG_STR='🦋'
    # -----------------------------------------------------------------------------
    @staticmethod
    def debug(message:str, stack_depth:int=1):
        # print(f"{message=} and {stack_depth=}")
        tick = APP._DEBUG_STR*2
        deb_str = APP._DEBUG_STR
        deb_bar = '[❌🐛 🐜 🐝 🪲 🐞 🦗🪳❌]'
        stack_txt = ''
        if APP._DEBUG_ON:
            if APP._DETAILS_ON:
                actual_depth = len(inspect.stack())
                # print(f"{actual_depth=}{type(actual_depth)}\t{stack_depth=}{type(stack_depth)}")
                stack_depth = min(actual_depth, stack_depth)
                locator = sys._getframe(stack_depth) # elevate in stack to the previous position (the caller)
                stack_info = (
                        f' func: {locator.f_code.co_name}'
                        f' at line: {locator.f_lineno}'
                        f' of file: {locator.f_code.co_filename} ')
                
                stack_txt = ( f' {stack_info} '.center(111,deb_str)  
                                if len(stack_info)<105 
                                else
                              f'{tick}\t{stack_info}\t{tick}' 
                            )
                            

            mod_info = message.replace('\n', f'\n{tick}\t')
            title=('\tDebug Message :\t'.center(80,deb_str)
                   +'\n'
                   +f' {deb_bar} '.center(76,deb_str)
                   )
            debug_message = (  f'\n{title}\n{tick}'
                    f'\n{tick}\t{mod_info}\n{tick}\n'
                    f'{stack_txt}\n')
            
            if (APP._DEBUG_DO_LOG and APP._DEBUG_DO_CLI):
                CLI.print_log_at(
                    debug_message,
                    APP._DEBUG_LOG_AT_LEVEL
                )
            elif APP._DEBUG_DO_CLI:
                print(debug_message)
            else:
                CLI.print_log_at()
    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    def print_dir(obj: object, columns:int = 3, show_internals:bool = False):
        if APP.CLI_DEBUG_MODE:
            object_guts = dir(obj)
            data = {}
            for attr in object_guts:
                data[attr]=[f'{attr}']
                if attr.startswith('_'):
                    if attr in data.keys():
                        data[attr].append('i') 
                    else: 
                        data[attr]=['inside']
                if callable(getattr(obj, attr, None)):
                    if attr in data.keys():
                        data[attr].append('()') 
                    else: 
                        data[attr]=['()']
            print(f"\nParsing Instance of TYPE: {type(obj).__name__}")
            part = ''            
            for idx, atr_info in enumerate(data.values(),start=1):
                specs = ''.join([x for i, x in enumerate(atr_info, start=1) if i>1])
                part += f'{idx}. {atr_info[0]}:{specs}; '
                if idx%columns == 0:
                    print(part)
                    part=''
    # -----------------------------------------------------------------------------
# =================================================================================


class CLI:

    def get_error_place(stack_depth: int = 1) -> str:
        locator = sys._getframe(stack_depth) # elevate in stack to the previous position (the caller)
        return (
                f' func: {locator.f_code.co_name}'
                f' at line: {locator.f_lineno}'
                f' of file: {locator.f_code.co_filename} '
                )
    # -------------------------------------------------------------------------

    @classmethod
    def print_log_at(cls, msg: str, current_level: Level) -> None:
        if APP.PRINT_AT.value <= current_level.value:
            print(msg)
        if APP.LOG_AT.value <= current_level.value:
            log_msg = f'\n @@@ {datetime.now().isoformat()}\n{msg.lstrip()}'
            current_level.call_log_method(log_msg)
    # -------------------------------------------------------------------------

    @classmethod
    def cmd_status(cls, 
                    command: str, 
                    result: str, 
                    error: str, 
                    code: int, 
                    stack_depth:int = 5) -> str:  
        marker = '✅' if code==0 else '🚧'
        mst_type = 'CMD-OK' if code==0 else 'CMD Warning'
        message = (f'CMD Ran:\t[{command.strip()}]\n'
                   +f'CMD Result:\t[{result.strip()}]\n'
                   +f'CMD Error:\t[{error.strip()}]\n'
                   +f'CMD Code:\t[{code}]'
                   )
        msg = cls.get_message(mst_type, message, marker, '\n', stack_depth=stack_depth)
        cls.print_log_at(msg, Level.INFO if code==0 else Level.WARN)
    # -------------------------------------------------------------------------

    @classmethod
    def get_message(cls, msg_type: str, 
                    message: str, 
                    marker: str, 
                    spacer:str = '\n\n',
                    stack_depth:int = 3) -> str:  
        info = list()
        if message and msg_type and marker:
            info.append(f"{spacer}{marker} {msg_type} @ {cls.get_error_place(stack_depth = stack_depth)} {marker}")
            upd = message.replace("\n", f"\n{marker} ")
            info.append(f'\n{marker}\n{marker} {upd}\n{marker}{spacer}')
        return ''.join(info)
    # -------------------------------------------------------------------------

    @classmethod
    def pin_error(cls, message: str = None, depth:int =3,) -> None:
        """ Gets location description for the call place to log exact function name, file, and line
        """
        marker = '❌❌❌'
        if message:
            msg = cls.get_message('Error', message, marker, stack_depth=depth)
            cls.print_log_at(msg, Level.ERROR)
    # -------------------------------------------------------------------------

    @classmethod
    def pin_warning(cls, message: str = None, depth:int =3, ) -> None:
        """ Gets location description for the call place to log exact function name, file, and line
        """
        marker = '!!!'
        if message:
            msg = cls.get_message('Warning', message, marker, stack_depth=depth)
            cls.print_log_at(msg, Level.WARN)
    # -------------------------------------------------------------------------

    @classmethod
    def pin_info(cls, message: str = None, depth:int =3, ) -> None:
        """ Gets location description for the call place to log exact function name, file, and line
        """
        marker = 'ⓘⓘⓘ'
        if message:
            msg = cls.get_message('Info', message, marker, spacer='\n', stack_depth=depth)
            cls.print_log_at(msg, Level.INFO)
    # -------------------------------------------------------------------------
#==============================================================================