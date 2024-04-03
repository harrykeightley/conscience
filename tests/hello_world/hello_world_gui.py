import tkinter as tk


def setup_display(root: tk.Toplevel):
    text = tk.Label(root, text="Hello World")
    text.pack()


def main() -> None:
    """Entry point"""
    root = tk.Tk()
    setup_display(root)
    root.mainloop()


if __name__ == "__main__":
    main()
