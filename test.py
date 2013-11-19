def reverse_even_rows(text): 
    """if chart contains both patterned right-side (RS) and wrong-side (WS) rows,
    this will reverse the direction of the WS rows so they read in the correct direction."""
    i = 0
    l = []
    
    while i < len(text):
        if i%2 != 0:
            l = text[i].split()
            l.reverse()
            text[i] = (" ").join(l)
        i += 1
    
    return text


def transform_multiple(words):
    i = 0
    for word in words:
        if words[i] == words[i+1]:



symbols = {1: "knit", 2: "purl", 3: "ktbl", 4: "ptbl", 5: "bind off", 6: "yo", 
            7: "M1", 8: "make eyelet", 9: "right-leaning increase", 10: "left-leaning increase", 
            11: "double increase", 12: "triple increase", 13: "triple purl increase", 14: "increase 1 st", 
            15: "increase 2 sts", 16: "increase 4 sts", 17: "increase 5 sts", 18: "yo 1 time", 
            19: "yo 2 times", 20: "yo 3 times", 21: "yo 4 times", 22: "yo 5 times", 23: "ssk", 
            24: "k2tog", 25: "double decrease", 26: "k3tog", 27: "p2tog tbl", 28: "p2tog", 
            29: "double purl decrease", 30: "p3tog", 31: "decrease 1 st", 32: "decrease 2 sts", 
            33: "decrease 3 sts", 34: "decrease 4 sts", 35: "decrease 5 sts", 36: "knit into row below", 
            37: "purl into row below", 38: "slip st as if to knit", 39: "slip st as if to purl", 
            40: "slip st with yarn in front", 41: "no stitch", 42: "bobble", 43: "selvage st", 
            44: "short knit", 45: "short purl"}

f = open("static/text/oldshale.txt")
text = f.readlines()
f.close()

text.reverse()
"""If the chart contains patterned WS rows call reverse_even_rows() on the text"""

# instructions = []
# i = 1

# for line in text:
#     row = line.split()
#     row_num = "\nRow %d:" % (i)        
#     instructions.append(row_num)
#     i += 1
#     for number in row:
#         words = []
#         number = int(number)
#         # words.append(symbols[number])
#         # converted = transform_multiple(words)
#         instructions.append(symbols[number])