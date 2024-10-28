from urlhlib import *
import urlhlib
import tkinter as tk
from tkinter import ttk
import os
#win32com.client as win32

class URLHausUploader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("URLHaus Uploader")
        self.geometry("400x300")

        # Create the main frame
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

        # Create the option buttons
        option_label = ttk.Label(main_frame, text="Choose an option:")
        option_label.grid(row=0, column=0, sticky=tk.W)

        self.selected_option = tk.StringVar()
        option_1 = ttk.Radiobutton(main_frame, text="Start the automated URLHaus uploader",
                                  variable=self.selected_option, value="1")
        option_2 = ttk.Radiobutton(main_frame, text="Choose a custom list to upload",
                                  variable=self.selected_option, value="2")
        option_3 = ttk.Radiobutton(main_frame, text="Manually add a single URL",
                                  variable=self.selected_option, value="3")
        option_1.grid(row=1, column=0, sticky=tk.W)
        option_2.grid(row=2, column=0, sticky=tk.W)
        option_3.grid(row=3, column=0, sticky=tk.W)

        # Create the action button
        action_button = ttk.Button(main_frame, text="Proceed", command=self.handle_option)
        action_button.grid(row=4, column=0, sticky=tk.E, pady=10)
def handle_option(self):
        option = self.selected_option.get()
        if option == '1':
            automatic()
            autoupload('uploadlist.txt')

        elif option == '2':
            filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            comment =  simpledialog.askstring("Enter Comment", "Enter content date (in YYMMDD format) and source (i.e. 220719 HISAC email)")
            fileupload(filename, comment)

        elif option == '3':
            url = simpledialog.askstring("Enter URL", "What is the URL you would like to upload?")
            comment = simpledialog.askstring("Enter Comment", "Enter comments (Source and date in YYDDMM format).")
            urlhlib.manual(url, comment)
#        elif optional =='4':
#            print("Not functional yet./n Goodbye.")
if __name__ == "__main__":
    app = URLHausUploader()
    app.mainloop()