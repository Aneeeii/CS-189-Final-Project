import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import global_alignment as GA
class Body:

    def __init__(self):
        self._root, self.frame = None, None
        self.text, self.menu = None, None
        self.top_sequence, self.bot_sequence = None, None
        self.match, self.mismatch, self.gap = None, None, None
        self.label, self.score_frame = [], None
        self.to_destroy = []
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
        self.delete_frame()
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
    
    def data_collection(self, name):
        self.clear_text()
        collect = Sequences(self._root, name)
        condition = False
        try:
            self.top_sequence = list(collect.top_sequence)
            self.bot_sequence = list(collect.bot_sequence)
            if self.top_sequence == [] or self.bot_sequence == []:
                raise TypeError
            condition = True
        except TypeError:
            message = "Please fill in both sequences"
            messagebox.showerror("Error", message)
            self.view_instructions()
        if condition:
            matching = Match_Info(self._root, "Matching Information")
            self.match = matching.match_score
            self.mismatch = matching.mismatch_score
            self.gap = matching.gap_score
            try:
                self.match = int(self.match)
                self.mismatch = int(self.mismatch)
                self.gap = int(self.gap)
            except (ValueError, TypeError):
                message = "Please fill in all scores with integers."
                messagebox.showerror("error", message)
    
    def delete_frame(self):
        for i in self.to_destroy:
            if i is not None:
                i.destroy()

    
    def global_aligning(self):
        self.delete_frame()
        self.data_collection("Global Alignment")
        final, scores = GA.run(self.top_sequence, self.bot_sequence,
                       (self.match, self.mismatch, self.gap))
        self.score_frame = tk.Frame(self._root, bd=2, relief=tk.GROOVE)
        self.score_frame.pack(padx=10, pady=10)
        self.score_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.to_destroy.append(self.score_frame)
        for index, row in enumerate(scores):
            label_row = []
            for index2, num in enumerate(row):
                label = tk.Label(self.score_frame, text=num, width=7, height=4, 
                                 anchor = "center",relief=tk.RIDGE)
                label.grid(row=index, column=index2, padx=10, pady=10)
                label_row.append(label)
            self.label.append(label_row)
        top, bottom = final
        top = " ".join(top)
        bottom = " ".join(bottom)
        self.result_label = tk.Label(self.frame, text=top + "\n" + bottom)
        self.result_label.pack(side=tk.BOTTOM, anchor="center", pady = (0,10))
        self.to_destroy.append(self.result_label)




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


class Match_Info(tk.simpledialog.Dialog):

    def __init__(self, root, title=None):
        self.root = root
        self.match_score = None
        self.mismatch_score = None
        self.gap_score = None
        super().__init__(root, title)

    def body(self, frame):
        self.match = tk.Label(frame, width=30, text="Match Score")
        self.match.pack()
        self.match_entry = tk.Entry(frame, width=30)
        self.match_entry.pack()

        self.mismatch = tk.Label(frame, width=30, text="Mismatch Score")
        self.mismatch.pack()
        self.mismatch_entry = tk.Entry(frame, width=30)
        self.mismatch_entry.pack()

        self.gap = tk.Label(frame, width=30, text="Gap Score")
        self.gap.pack()
        self.gap_entry = tk.Entry(frame, width=30)
        self.gap_entry.pack()

    def apply(self):
        self.match_score = self.match_entry.get()
        self.mismatch_score = self.mismatch_entry.get()
        self.gap_score = self.gap_entry.get()
    

        


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
# main()

# def main():
#     root = tk.Tk()
#     root.title("Table with Numbers")
    
#     # Define your table data (example)
#     table_data = [
#         [1, 2, 3],
#         [4, 5, 6],
#         [7, 8, 9]
#     ]
    
#     # Create labels in a grid to represent the table
#     for i, row in enumerate(table_data):
#         for j, value in enumerate(row):
#             label = tk.Label(root, text=value, width=5, height=2, relief=tk.RIDGE)
#             label.grid(row=i, column=j, padx=5, pady=5)
    
#     root.mainloop()

main()