import prompt_toolkit.shortcuts as pt
from rich.progress import track

finaltext = ""

filename = pt.prompt("Enter the file name : ")

file = open(filename, "r")
lines = file.readlines()

for line in lines:
    if "Release" in line:
        pass
    else:
        key = line.split(" : ")[-1]
        key = key.replace("\n", "")
        key = key.replace("'", "")
        key = key.replace("!//APOS//!", "'")
        if "Key" in key:
            if "backspace" in key:
                print(f"Before {finaltext}")
                finaltext = finaltext[:-1]
                print(f"After {finaltext}")
            elif "space" in key:
                finaltext += " "
            elif "enter" in key:
                finaltext += "\n"
            elif "tab" in key:
                finaltext += "\nTab\n"
            # elif "shift" in key:
            #     if "_r" in key:
            #         finaltext += "\nRight Shift\n"
            #     if "_l" in key:
            #         finaltext += "\nLeft Shift\n"
            # elif "alt" in key:
            #     if "_r" in key:
            #         finaltext += "\nRight Alt\n"
            #     if "_l" in key:
            #         finaltext += "\nLeft Alt\n"
            
                
        else:
            finaltext += key

print("Final text :")
print(finaltext)