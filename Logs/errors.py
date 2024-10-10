from Logs.log import log

class ERROR(BaseException):
    __EXP_codes = [     # 10XX
        "0000 - Unknown error occured"
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
        "1311 - Failed to confirm DCE startup" 
        "1350 - Failed to initalize IMU" 
    ]

    __SNSR_codes = [    # 14XX
        "1400 - Failed to start camera"
    ]

    def __init__(self, code, context=""):
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
        log(str, f"- {context}")
        super().__init__(str)
        super().add_note(context)

    def __binary_search(self, code, codes, front=0, back=-1000):
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

