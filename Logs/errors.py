#!/usr/bin/env python

"""
A module used to hendle throwing and recording errors that occur
Written in accordance to the STAR Payload Software Standards
Makes use of the log module to handle recording errors that occur
"""

__author__="Simon Kowerski"
__credits__=["Simon Kowerski"]
__creation_date__="1/22/2024"

from Logs.log import log

class ERROR(BaseException): 
    """
    Class containing the definition of ERROR, a base exception which can be raised to output and log a custom error code/message
    Written in accordance to the STAR Payload Software Standards

    Atributes:
        ALL OF THE BELOW MUST HAVE ERROR CODES SORTED IN ASCENDING ORDER
        __EXP_CODES[] - a string array which stores error messages in the form "10XX - Error Message" 
                        used for storing experiment wide codes
        __COMM_CODES[] - a string array which stores error messages in the form "11XX - Error Message" 
                         used for storing errors that occur during communication with the OBC
        __ADCS_CODES[] - a string array which stores error messages in the form "13XX - Error Message" 
                         used for storing errors that occur during communication with the DCE/IMU
        __SNSR_CODES[] - a string array which stores error messages in the form "14XX - Error Message" 
                         used for storing errors that occur during communication with any sensors (camera, leds, pressure sensors, etc)
    """

    __EXP_codes = [     # 10XX      (If you see one of these there is a huge problem)
        "1000 - Unknown error occured",
        "1001 - CRITICAL ERROR - unable to stop reaction wheel"
    ]

    __COMM_codes = [    # 11XX

    ]

    __ADCS_codes = [    # 13XX
        "1300 - Failed to generate torque command",
        "1301 - Failed to generate speed command",
        "1302 - Failed to generate read command",
        "1303 - Failed to send command to DCE",
        "1304 - Failed to recieve data from DCE",
        "1305 - Recieved incorrect data from DCE",
        "1310 - Failed to open serial connection to DCE",
        "1311 - Failed to confirm DCE startup",
        "1350 - Failed to initalize IMU"
    ]

    __SNSR_codes = [    # 14XX
        "1400 - Failed to start camera"
    ]

    def __init__(self, code, context=""):
        """
        Initializes the error to be thrown. Finds the proper error message for the given code
        Logs the code, error message, and additional context
        Context DOES NOT need to include the leading "- "

        Args:
            code (int): the error code to be logged
            context (string): Optional additional message to be appended to the log
        """
        type=(int)(code/100)%10
        match type:
            case 0:
                codes=self.__EXP_codes
            case 1:
                codes=self.__COMM_codes
            case 3:
                codes=self.__ADCS_codes
            case 4:
                codes=self.__SNSR_codes
            case _:
                codes=self.__EXP_codes
                code=0
    
        str=f"{self.__binary_search(code, codes)}"
        #FIXME: no '-' when no context
        if(context == ""):
            log(str)
        else:
            log(str, f"- {context}")
        super().__init__(str)
        #super().add_note(context)

    def __binary_search(self, code, codes, front=0, back=-1000):
        #TODO: Finish docustring then push changes
        """
        Performs a binary search to locate the error message for the given error code in the provided array

        Args:
            code (int): the error code to search for
            codes (string[]): the array containing the appropriate error codes and messages
            front (int): the current front of the array indicating where to start the search, can be set by default to the start of the array
            back (int): the current back of the array indicating where to end the search, can be set by default to the end of the array

        """
        if(back==-1000):
            back=len(codes)-1

        cur = int((front + back) / 2)
        current = int(codes[cur][:4])

        if(front > back):
            return -1 

        if(code == current):
            return codes[cur]
        
        if(code < current):
            return self.__binary_search(code, codes, front, cur - 1)
        
        if(code > current):
            return self.__binary_search(code, codes, cur+1, back)
        
        return -1

