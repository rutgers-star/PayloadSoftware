class DCE_ERROR(BaseException):
    __codes = [
        "1300 - Failed to generate torque command",
        "1301 - Failed to generate speed command",
        "1302 - Failed to generate read command",
        "1303 - Failed to send command to DCE",
        "1304 - Failed to recieve data from DCE",
        "1305 - Recieved incorrect data from DCE",
    ]

    def __init__(self, code, context=""):
        super().__init__(f"{self.__binary_search(code)}")
        super().add_note(context)

    def __binary_search(self, code, front=0, back=len(__codes)-1):
        codes = self.__codes

        cur = int((front + back) / 2)
        current = int(codes[cur][:4])
        print(current)

        if(front > back):
            return -1 

        if(code == current):
            return codes[cur]
        
        if(code < current):
            return self.__binary_search(code, front, cur - 1)
        
        if(code > current):
            return self.__binary_search(code, cur+1, back)
        
        return -1
            
raise DCE_ERROR(1301)

#look at exception group?

