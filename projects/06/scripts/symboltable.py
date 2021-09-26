SYMBOLS = {
    "R0": "0",
    "R1": "1",
    "R2": "2",
    "R3": "3",
    "R4": "4",
    "R5": "5",
    "R6": "6",
    "R7": "7",
    "R8": "8",
    "R9": "9",
    "R10": "10",
    "R11": "11",
    "R12": "12",
    "R13": "13",
    "R14": "14",
    "R15": "15",
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4",
    "SCREEN": "16384",
    "KBD": "24567"
    }
class SymbolTable:

       
     def __init__(self):
        # deep copying
        self.table = {symbol: value for symbol, value in zip(SYMBOLS.keys(), SYMBOLS.values())}
        self.available_address = 16  # default is 16

     def addEntry(self, symbol, address):
        self.table[symbol] = str(address)

     def contains(self, symbol):
        return True if symbol in self.table else False

     def GetAddress(self, symbol):
        return str(self.table[symbol])
   
     def get_available_address(self):
         return str(self.available_address)

