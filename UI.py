import tkinter as tk
from tkinter import ttk, filedialog, messagebox
class Body:

    def __init__(self):
        self._root = None
        self.frame = None
        self.text = None
        self.menu = None
        self.top_sequence = None
        self.bot_sequence = None
        self.create()

    def create_bar(self):
        self.menu = tk.Menu(self._root)
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Global Alignment", command=self.global_aligning)
        file_menu.add_command(label="Local Alignment", command=None)

        self.menu.add_cascade(label="Alignment Options", menu=file_menu)
        
        other = tk.Menu(self.menu, tearoff=0)
        other.add_command(label="View Instructions", command=self.view_instructions)
        other.add_command(label="Exit", command=self._root.quit)
        
        self.menu.add_cascade(label="Other", menu=other)
        self._root.config(menu=self.menu)

    def view_instructions(self):
        self.clear_text()
        line1 = "How to Use:\n\n"
        line2 = "1. Choose which alignment method you would like to use in the Alignment pulldown.\n\n"
        line3 = "2. You can return to instructions or exit in the Other pulldown."
        self.text.insert(tk.END, line1)
        self.text.insert(tk.END, line2)
        self.text.insert(tk.END, line3)

    def clear_text(self):
        self.text.delete("1.0", tk.END)

    def create(self):
        self._root = tk.Tk()
        self._root.geometry("700x600")
        self.frame = tk.Frame(self._root, bd=2, relief=None, padx=10, pady=10)
        title_label = tk.Label(self.frame, text="Welcome to the Alignment Tool!", 
                               font=("Courier New", 16))
        title_label.pack()
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.text = tk.Text(self.frame, width=70, height=28, font=("Arial", 12))
        self.view_instructions()
        self.text.pack(expand=True, fill="both")
        self.create_bar()
    
    def return_root(self):
        return self._root
    
    def data_collection(self):
        self.clear_text()
        collect = Sequences(self._root, "Global Alignment")
        try:
            self.top_sequence = list(collect.top_sequence)
            self.bot_sequence = list(collect.bot_sequence)
            if self.top_sequence == [] or self.bot_sequence == []:
                raise TypeError
        except TypeError:
            message = "Please fill in both sequences"
            messagebox.showerror("Error", message)
            self.view_instructions()
    
    def global_aligning(self):
        self.data_collection()



class Sequences(tk.simpledialog.Dialog):

    def __init__(self, root, title=None):
        self.root = root
        self.top_sequence = None
        self.bottom_sequence = None
        super().__init__(root, title)

    def body(self, frame):
        self.top = tk.Label(frame, width=30, text="Sequence 1")
        self.top.pack()
        self.top_entry = tk.Entry(frame, width=30)
        self.top_entry.pack()

        self.bot = tk.Label(frame, width=30, text="Sequence 2")
        self.bot.pack()
        self.bot_entry = tk.Entry(frame, width=30)
        self.bot_entry.pack()

    def apply(self):
        self.top_sequence = self.top_entry.get()
        self.bot_sequence = self.bot_entry.get()
        


# def view_instructions(frame):
#     line = instruction_info()

    
#     instructions = tk.Label(frame, text=instruction_info(), font=("Arial", 12))
#     instructions.place(relx=0.5, y=30, anchor="center")
#     instructions.pack()




# Create a label to act as the title inside the box





# Create a menubar

def main():
    body = Body()
    root = body.return_root()
    root.mainloop()
    

    # Create a frame to act as the box
    
    
    
    
    
    # view_instructions(frame)
    # create_bar(root, frame)

    # Run the application
main()