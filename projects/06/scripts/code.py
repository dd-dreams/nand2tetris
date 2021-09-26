import json

with open("binary_codes.json") as file:  # receiving the binary codes
    CODES = json.load(file)


class Code:

    def translate_comp(self, string):
        comp = CODES["comp"]
        
        if string in comp["0"]:  # if a == 0
            return CODES["comp"]["0"][string]
        return CODES["comp"]["1"][string]  # if a == 1

    def translate_jump(self, string):
        return CODES["jump"][string]
    
    def translate_dest(self, string):
        return CODES["dest"][string]

