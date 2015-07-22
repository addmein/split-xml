from Tkinter import *
import tkFileDialog, tkMessageBox, os
from xml.dom.minidom import parse

class App(Frame):
    def  __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        
        msg = Text(master)
        
        class infoMessage():
            def write(self, s):
                msg.insert(END, s)
                msg.yview_pickplace("end")
                msg.update_idletasks()
                
        Label(master, text="").grid(row=4)
        msg.config(bg="azure")
        msg.place(x=5, y=170, height=155, width=530)
        
        sys.stdout = infoMessage()
        
        self.file_options = options = {}
        options['defaultextension'] = '.xml'
        options["filetypes"] = [("xml files", ".xml")]
        options["initialdir"] = "B:\\DTP DEPARTMENT\\_Projects MOCA"
        options['parent'] = master
        options['title'] = 'XML Split v1'
    
    def create_widgets(self):
        about = Label(master, text="\n\
                This app will split a .xml file.\n\n")
        w = Label(master, text="          File Path:    ")
        var = StringVar()
        e = Entry(master, textvariable=var, width=52)
        b = Button(master, text="Browse", command=lambda:var.set(tkFileDialog.askopenfilename(**self.file_options)))
        
        about.grid(row=0, column=1, columnspan=5)
        w.grid(row=1, column=1)
        e.grid(row=1, column=2, columnspan=3)
        b.grid(row=1, column=5)
        
        Label(master, text="").grid(row=2)
        
        def for_proof(np, file, md):
            xmldoc = parse(file)
            nodes =  xmldoc.getElementsByTagName("servcatype")
            
            for node in nodes:
                parent = node.parentNode
                parent.removeChild(node)
                
            f = open(os.path.join(np, '%s_VVV_00.xml'%md), 'w')
            xmldoc.writexml(f, encoding="UTF-8")
            f.close()
            
        def clean_lines(np, md):
            clean_lines =[]
            with open(os.path.join(np, '%s_VVV_00.xml'%md), 'r') as f:
                lines = f.readlines()
                clean_lines = [l.strip() for l in lines if l.strip()]
                
            with open(os.path.join(np, '%s_VVV_00.xml'%md), 'w') as f:
                f.writelines('\n'.join(clean_lines))
        
        def split(path):
            np = os.path.split(path)[0]
            print np
            try:
                xmldoc = parse(path)
            except:
                tkMessageBox.showwarning("ERROR", "ERROR: \nPlease choose a .xml file.\nThe application will now quit.")
                print "Please choose a .xml file."
                quit()
            
            servcatype = xmldoc.getElementsByTagName("servcatype")
            modeldesc = xmldoc.getElementsByTagName("modeldesc")
            md = "".join(t.nodeValue for t in modeldesc[0].childNodes if t.nodeType == t.TEXT_NODE)
#            print (md)
            str = md.split('-')
#            print str
            prj = np.split('/')[4].split(" ")
            print prj
            if prj[0] == "DTP":
                prj = np.split('/')[7].split(" ")
            elif prj == "English":
                prj = np.split('/')[6].split(" ")
            print prj
            try:
                code = ''.join([prj[3][2:-11], prj[3][12:-1]])
            except:
                code = "ZZZ"
            print code
            try:
                nn = "%s-%s-%s" %(prj[1], prj[2], code)
            except:
                nn = prj[0]
            print nn
            
            i = 0           
            for servcatype in servcatype:        
                i += 1     
                if i <10:
                    f = open(os.path.join(np, '%s_VVV_0%d.xml'% (nn, i)), 'w')
                else:
                    f = open(os.path.join(np, '%s_VVV_%d.xml'% (nn, i)), 'w')
                f.write(servcatype.toxml())
                f.close()
            
            for_proof(np, path, nn)
            clean_lines(np, nn)
            
            print ('\nTASK COMPLETED')
            tkMessageBox.showwarning("TASK COMPLETED", "The .xml file is splitted. \nYou can now close the application.")
        
        def confirm_path():
            path = var.get()
            if path != "":
                if tkMessageBox.askyesno("Working Folder", "The selected file for splitting is: \n\n" + path + "\n\nIs this correct?"):
                    print ("Splitting file... \nPlease wait until you see the message TASK COMPLETED.\n")
#                    print (path)
                    split(path)
            else:
                print "Please try again!"
            
        start = Button(master, text="         Start         ", command=confirm_path)
        start.grid(row=3, column=3, columnspan=1)
            
            
if __name__ == "__main__":        
    master = Tk()
    master.title("XML Split v1")
    master.geometry("540x330")
    master.resizable(width=FALSE, height=FALSE)
    
    app = App(master)
    master.mainloop()