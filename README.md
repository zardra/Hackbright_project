Project plan

Basic idea:
1. User takes photo of knitting chart with phone or computer camera.
2. Program runs image through OCR.
3. Process converted imaged to interpret symbols into English directions.
    *Problem area: what about pattern repeats?
4. Generate usable written directions for the user.

What is needed:
1. Code to interact with camera
    *WebRTC
    *toDataURL
2. OCR software
    *Will need to make my own?
3. Symbol library
    *Start with freeware knitting symbol dictionaries
        *http://home.earthlink.net/~ardesign/knitfont.htm
        *http://www.knittingfool.com/Reference/KF_Symbols.aspx
        *http://www.knittinguniverse.com/downloads/KFont/
        *http://www.craftyarncouncil.com/chart_knit.html
    *Problem area: how to handle symbols that have similar meaning
4. Code to take in knitting symbols, process it into English, and print them out
    *What would be the best format?
        *PDF for printability?
        *Or just plain text?


Transformation steps
--------------------
1. Open text file.
2. Read it in by line (.readlines()).
3. Reverse list order because instructions read from bottom of chart up.
4. How to differentiate between charts with patterning on all rows and those that knit plain on WS?
5. Create empty list? Or change the list in place? In place would make keeping the rows separate easier.
6. Either before running the list through the symbol key or after (which would be better?), need to reverse the order of the patterned WS rows (i.e., in relation to #4).
7. Send each row through a function that will consolidate multiple instructions (i.e., "knit, knit, knit" vs. "knit 3 times").
8. Add row numbers.
9. Print out instructions.