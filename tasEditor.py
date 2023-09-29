import pickle
import tkinter as tk

import customtkinter as ctk
from CTkListbox import *


def load(file_name):
    lines = pickle.load(open(file_name, "rb"))
    print(lines)

    out = []

    nKB = 0
    nMM = 0

    prev = None

    for line in lines:
        if prev is None:
            prev = line
            out.append((line[0], 0, line[2], line[3]))
            continue

        if line[0] == 0x01 or line[0] == 0x00:
            nKB += 1
        elif line[0] == 0x02:
            nMM += 1

        dur = round(line[1] - prev[1], 4)

        out.append((line[0], dur, line[2], line[3]))
        prev = line

        print(f"line: {line}, dur: {dur}, parsed: {out[-1]}")

    print("Key events: " + str(nKB))
    print("Mouse move events: " + str(nMM))

    return out


class EditableListbox:
    def __init__(self, f_name="out.pkl"):
        self.editItemIndex = None
        self.f_name = f_name
        self.root = ctk.CTk()
        self.lb = CTkListbox(self.root)
        self.lb.pack(side="left", fill="both", expand=True)
        for i in load(f_name):
            self.lb.insert("end", i)

        self.upB = ctk.CTkButton(self.root, text="/\\", command=self.moveUp, width=10)
        self.upB.pack(side="top", fill="x")
        self.downB = ctk.CTkButton(self.root, text="\\/", command=self.moveDown, width=10)
        self.downB.pack(side="top", fill="x")

        self.editB = ctk.CTkButton(self.root, text="Edit", command=self.startEdit, width=10)
        self.editB.pack(side="top", fill="x")

        # save on close
        # self.root.protocol("WM_DELETE_WINDOW", self.save)

    def moveUp(self):
        sel_ind = self.lb.curselection()
        if sel_ind == 0:
            return

        sel_n = f"END{sel_ind}"

        # swap ind and ind - 1
        curr = self.lb.buttons[sel_n]
        cText = curr.cget("text")
        prev = self.lb.buttons[f"END{sel_ind - 1}"]
        pText = prev.cget("text")

        curr.configure(text=pText)
        prev.configure(text=cText)

        # select the new item
        self.lb.deselect(sel_ind)
        self.lb.select(f"END{sel_ind - 1}")

    def moveDown(self):
        sel_ind = self.lb.curselection()
        if sel_ind == self.lb.size() - 1:
            return

        sel_n = f"END{sel_ind}"

        # swap ind and ind + 1
        curr = self.lb.buttons[sel_n]
        cText = curr.cget("text")
        prev = self.lb.buttons[f"END{sel_ind + 1}"]
        pText = prev.cget("text")

        curr.configure(text=pText)
        prev.configure(text=cText)

        # select the new item
        self.lb.deselect(sel_ind)
        self.lb.select(f"END{sel_ind + 1}")

    def startEdit(self):
        index = self.lb.curselection()

        self._start_edit(index)
        return

    def _start_edit(self, index):
        self.editItemIndex = index
        text = self.lb.get(index)
        y0 = self.lb.bbox(index)[1]
        entry = tk.Entry(self.root, borderwidth=0, highlightthickness=1)

        entry.bind("<Return>", self.accept_edit)
        entry.bind("<Escape>", self.cancel_edit)
        entry.insert(0, text)
        entry.selection_from(0)
        entry.selection_to("end")
        entry.place(relx=0, y=y0, relwidth=1, width=-20)
        entry.focus_set()
        entry.grab_set()

    @staticmethod
    def cancel_edit(event):
        event.widget.destroy()

    def accept_edit(self, event):
        new_data = event.widget.get().split(" ")

        event.widget.destroy()
        self.lb.buttons['END' + str(self.editItemIndex)].configure(text=new_data)

    def runGUI(self):
        self.root.mainloop()

    def save(self):
        lines = []
        t = 0
        for i, b in self.lb.buttons.items():
            text = b.cget("text")
            t += float(text[1])

            print(f"t: {t}, text: {text}")

            lines.append((
                int(text[0]),
                t,
                int(text[2]),
                int(text[3])
            ))

        pickle.dump(lines, open(self.f_name, "wb"))


if __name__ == "__main__":
    flc_app = EditableListbox("captures/out.pkl")
    flc_app.runGUI()
