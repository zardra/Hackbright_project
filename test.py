import random

def create_random_knit_file():
    """Creates a text file representing an example of an expected OCR output file. Five lines of 20 randomly selected sttiches for demo purposes"""
    rows = []
    i = 0
    x = 0
    new_row = ""

    while x < 5:
        while i < 20:
            new_stitch = str(random.randint(1, 45)) + " "
            new_row += new_stitch
            i += 1
        new_row = new_row[:-1]
        rows.append(new_row)
        i = 0
        new_row = ""
        x += 1

    chart_rows = "\n".join(rows)
    knit_file = open("/static/text/chart_file.txt", "wb")
    knit_file.write(chart_rows)
    knit_file.close()

def reverse_even_rows(text): 
    """if chart contains both patterned right-side (RS) and wrong-side (WS) rows, this will reverse the direction of the WS rows so they read in the correct direction."""

    i = 0
    l = []
    
    while i < len(text):
        if i%2 != 0:
            l = text[i].split()
            l.reverse()
            text[i] = (" ").join(l)
        i += 1
    
    return text

def change_to_symbols(text):
    """Takes each item from the text file and changes the numbers to the written instructions"""

    l = []
    i = 0

    while i < len(text):
        l = text[i].split()
        l2 = []
        for number in l:
            number = int(number)
            l2.append(symbols[number])
            text[i] = (" ").join(l2)
        i += 1

    return text

def transform_multiples(text):
    """Takes the written instructions and consolidates multiples into concise language for easier readab"""

    instruction_list = []
    multi_count = 1
    prev_instruction = ""
    i  = 0

    while i < len(text):
        l = text[i].split()
        for instruction in l:
            if instruction == prev_instruction:
                multi_count += 1
            else:
                if multi_count > 1:
                    instruction_list.append(prev_instruction + " " + str(multi_count) + " times")
                    multi_count = 1
                else:
                    if prev_instruction == "":
                        pass
                    else:
                        instruction_list.append(prev_instruction)
            prev_instruction = instruction

        if multi_count > 1:
            instruction_list.append(prev_instruction + " " + str(multi_count) + " times")
        else:
            instruction_list.append(prev_instruction)
        text[i] = (", ").join(instruction_list)
        instruction_list = []
        multi_count = 1
        prev_instruction = ""
        i += 1

    return text

def create_knit_even_rows(text):
    """Creates instructions with Row numbers for charts worked evenly on the WS rows"""
    i = 1
    instructions = ""
    knit_even_rows = []
    
    for row in text:
        instructions += "Row %d: %s" % (i, row)
        knit_even_rows.append(instructions)
        instructions = "Row %d: work row evenly" % (i+1)
        knit_even_rows.append(instructions)
        instructions = ""
        i += 2
    
    return knit_even_rows

def create_knit_rows(text):
    """Creates instructions with Row numbers for charts worked evenly on the WS rows"""
    i = 1
    instructions = ""
    knit_rows = []

    for row in text:
            instructions += "Row %d: %s" % (i, row)
            i += 1
            knit_rows.append(instructions)
            instructions = ""
    
    return knit_rows

# dictionary assigning values to knitting instructions
symbols = {1: "knit", 2: "purl", 3: "ktbl", 4: "ptbl", 5: "bind off", 6: "yo", 7: "M1", 8: "make eyelet", 9: "right-leaning increase", 10: "left-leaning increase", 11: "double increase", 12: "triple increase", 13: "triple purl increase", 14: "increase 1 st", 15: "increase 2 sts", 16: "increase 4 sts", 17: "increase 5 sts", 18: "yo 1 time", 19: "yo 2 times", 20: "yo 3 times", 21: "yo 4 times", 22: "yo 5 times", 23: "ssk", 24: "k2tog", 25: "double decrease", 26: "k3tog", 27: "p2tog tbl", 28: "p2tog", 29: "double purl decrease", 30: "p3tog", 31: "decrease 1 st", 32: "decrease 2 sts", 33: "decrease 3 sts", 34: "decrease 4 sts", 35: "decrease 5 sts", 36: "knit into row below", 37: "purl into row below", 38: "slip st as if to knit", 39: "slip st as if to purl", 40: "slip st with yarn in front", 41: "no stitch", 42: "bobble", 43: "selvage st", 44: "short knit", 45: "short purl"}

def main(button_val):
    f = open("static/text/oldshale.txt")
    text = f.readlines()
    f.close()

    # reverse to "read" from botton of knitting chart
    text.reverse()
    reversed_text = text

    # if the chart contains patterned WS rows: 
    if button_val == "patterned":
        # reverse the even numbered rows
        reversed_rows = reverse_even_rows(reversed_text)
        # change the numbers to the written knitting instructions
        eng_ins = change_to_symbols(reversed_rows)
    else:
        # change the number to written knitting instructions
        eng_ins = change_to_symbols(reversed_text)

    # consoldiate multiple instructions
    compressed_ins = transform_multiples(eng_ins)

    if button_val == "patterned":
        # add row numbers to the instructions
        row_directions = create_knit_rows(compressed_ins)
    else:
        # add row numbers to the instructions
        row_directions = create_knit_even_rows(compressed_ins)

    return row_directions
