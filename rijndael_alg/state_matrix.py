# Takes a 16-byte block and stores it as a state matrix.
# Operate on the state matrix.
# Return it as a 16-byte block after operations.
# Provide a copy of the state matrix.

# PAD16: If number of bytes is not a multiple of 16 then pad.
# For the purpose of this demonstration we use <= 16 for simplicity.
def pad16(data: bytes) -> bytes:
    padding_length = 16 - (len(data) % 16)
    return data + bytes([padding_length]) * padding_length

# Primary data type
class StateMatrix:
    def __init__(self, byte_array : bytes):
        if len(byte_array) != 16:
            raise ValueError(f"StateMatrix requires exactly 16 bytes, got {len(byte_array)}")
        self.state = [
            [byte_array [0],  byte_array [4],  byte_array [8],  byte_array [12]],
            [byte_array [1],  byte_array [5],  byte_array [9],  byte_array [13]],
            [byte_array [2],  byte_array [6],  byte_array [10], byte_array [14]],
            [byte_array [3],  byte_array [7],  byte_array [11], byte_array [15]]
        ]

    def display(self):
        for row in self.state:
            # Print each row as hex values
            hex_values = " ".join(f"{byte:02x}" for byte in row)
            print(f"[ {hex_values} ]")

    def to_bytes(self) -> bytes:
        output = bytearray()
        for col in range(4):
            for row in range(4):
                output.append(self.state[row][col])
        # Return the current state in bytes
        return bytes(output)
    
    def interpret(self):
        for col in range(4):
            for row in range(4):
                # Returns the current state in characters
                print(chr(self.state[row][col]), end="")
        print()

    def copy(self):
        # Return a copy of the current state
        return StateMatrix(self.to_bytes())
    
    def to_string(self) -> str:
        lines = []
        for row in self.state:
            hex_values = " ".join(f"{byte:02x}" for byte in row)
            lines.append(f"[ {hex_values} ]")
        return "\n".join(lines)
    

