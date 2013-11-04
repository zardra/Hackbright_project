Project plan

Basic idea:
1. User takes photo of knitting chart with phone or computer camera.
2. Program runs image through OCR.
3. Process converted imaged to interpret symbols into English directions.
    *Problem area: what about pattern repeats?
4. Generate usable written directions for the user.

What is needed:
1. Code to interact with camera
    *Different for phone versus computer?
        *Chris might be good resource for phone interaction
        *Ask Katie about that camera code she mentioned before
    *Some possibilities for the computer:
        *Gstreamer
        *SimpleCV
        *OpenCV
        *Pygames
2. OCR software
    *Probably Tesseract since it can learn new languages
    *There is an API
3. Symbol library
    *Start with freeware knitting symbol dictionaries
        *http://www.knittingfool.com/Reference/KF_Symbols.aspx
        *http://www.knittinguniverse.com/downloads/KFont/
        *http://www.craftyarncouncil.com/chart_knit.html
4. Code to take in knitting symbols, process it into English, and print them out
    *What would be the best format?
        *PDF for printability?
        *Or just plain text?

