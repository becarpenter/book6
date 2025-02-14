from tkinter import (Tk, Frame, BooleanVar, Text,
                     Checkbutton, Label, Button,
                     StringVar, Entry, Scrollbar,
                     END)
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
import os
import run


class SelectFrame(Frame):
    def __init__(self, parent, controller):
        # default dir
        Frame.__init__(self, parent)

        self.controller = controller

        default_book_dir = os.path.dirname(
            os.path.dirname(
                os.path.realpath(__file__)
            )
        )
        # Variables
        self.do_bake_book = BooleanVar(value=True)
        self.printing = BooleanVar()
        self.book_dir = StringVar(value=default_book_dir)

        # Labels
        self.tasks_label = Label(self, text="Tasks to be performed:")
        self.debug_label = Label(self, text="Debug options:")

        # Buttons
        self.bake_book_check_button = Checkbutton(self,
                                                  text="Bake book",
                                                  variable=self.do_bake_book,
                                                  onvalue=True, offvalue=False)
        self.printing_button = Checkbutton(self,
                                           text="Enable diagnostic printing",
                                           variable=self.printing,
                                           onvalue=True, offvalue=False)
        self.change_book_dir = Button(self,
                                      text="Change book dir",
                                      command=self.change_dir)
        self.start_button = Button(self,
                                   text="Start selected jobs",
                                   command=self.start_jobs)

        # Text
        self.book_path_text = Entry(self,
                                    wrap=None,
                                    textvariable=self.book_dir
                                    )
        self.book_path_text.xview_moveto(1)

        self.tasks_label.pack()
        self.bake_book_check_button.pack()
        self.book_path_text.pack()
        self.change_book_dir.pack()
        self.debug_label.pack()
        self.printing_button.pack()
        self.start_button.pack()

    def start_jobs(self):
        # checking that the selected dir exists
        if not os.path.isdir(self.book_dir.get()):
            showinfo(title="Error",
                     message="The selected dir doesn't exist !")
            return

        steps = []

        if self.do_bake_book.get():
            steps.append("BakeBookStep")

        self.controller.start_jobs(steps,
                                   self.book_dir.get(),
                                   self.printing.get())

    def change_dir(self):
        _book_dir = askdirectory(
            initialdir=self.book_dir.get(),
            title="Select the book directory")
        self.book_dir.set(_book_dir)


class JobStep(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        self.main_label = Label(self)
        self.main_label.pack()

        self.printing_text = None

    def add_printing(self, text):
        if self.printing_text is None:
            self.printing_text = Text(self, height=100)
            scroll = Scrollbar(self)
            self.printing_text.configure(yscrollcommand=scroll.set)
            self.printing_text.pack()
        self.printing_text.insert(END, f"\n{text}")
        self.printing_text.see("end")
        self.update()


class BakeBookStep(JobStep):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.main_label.config(
            text="Will read current book6 text.\n"
            "Touch no files until done!"
        )


class Window(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Adding a title to the window
        self.title("Book6 utilities")
        self.geometry('500x200')
        self.resizable(False, False)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.current_frame = None

        self.frames = {}
        for F in (SelectFrame, BakeBookStep):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SelectFrame")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        self.current_frame = frame
        frame.tkraise()
        self.update()

    def print_info(self, message):
        self.current_frame.add_printing(message)

    def start_jobs(self, steps, book_dir, printing):
        for step in steps:
            if step == "BakeBookStep":
                self.show_frame("BakeBookStep")
                run.bake_book(
                           book_dir,
                           printing,
                           self)
                showinfo(title="Bake book",
                         message="Bake book step complete")
        showinfo(title="Finished",
                 message="All task are done")
        self.show_frame("SelectFrame")


if __name__ == "__main__":
    window = Window()
    window.mainloop()


