import PyPDF2
from gtts import gTTS
from appJar import gui
from pathlib import Path
def pdf_to_audio(input_file,output_file):
    pdfFileObj = open(input_file, "rb")
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    mytext = ""

    for pageNum in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(pageNum)

        mytext += pageObj.extractText()
    pdfFileObj.close()

    tts = gTTS(text=mytext, lang='en')
    save=str(output_file)+".mp3"
    tts.save(save)
    if(app.questionBox("File Save", "Output PDF saved. Do you want to quit?")):
        app.stop() 
def validate_inputs(src_file, dest_dir, out_file):

     errors = False
     error_msgs = []
     if (Path(src_file).suffix.upper() != ".PDF"):
        errors = True
        error_msgs.append("Please select a PDF input file")
        
     if not(Path(dest_dir)).exists():
        errors = True
        error_msgs.append("Please Select a valid output directory")

    # Check for a file name
     if len(out_file) < 1:
        errors = True
        error_msgs.append("Please enter a file name")
    
     return(errors, error_msgs)  


def press(button):
    if button=="Process":
        src_file = app.getEntry("Input_File")
        dest_dir = app.getEntry("Output_Directory")
        out_file = app.getEntry("Output_name")
        errors, error_msg = validate_inputs(src_file, dest_dir, out_file)
        if errors:
            app.errorBox("Error", "\n".join(error_msg), parent=None)
        else:
           pdf_to_audio(src_file,Path(dest_dir,out_file))
    else:
        app.stop()


app=gui("PDF To Audio Conversion", useTtk=True)
app.setTtkTheme('alt')
app.setSize(500, 200)

# Add the interactive components
app.addLabel("Choose Source PDF File to convert to audio")
app.addFileEntry("Input_File")

app.addLabel("Select Output Directory")
app.addDirectoryEntry("Output_Directory")

app.addLabel("Output file name")
app.addEntry("Output_name")

app.addButtons(["Process", "Quit"],press)
app.go()
