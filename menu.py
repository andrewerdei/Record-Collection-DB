
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import pandas as pd


class DiscogsApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Discogs Collection Manager")
        self.root.geometry("800x600")
        self.sort_directions = {}

        # CSV columns to extract
        self.columns = [
            "Catalog#",
            "Artist",
            "Title",
            "Label",
            "Format",
            "Rating",
            "Released",
            "release_id",
            "CollectionFolder",
            "Date Added",
            "Collection Media Condition",
            "Collection Sleeve Condition",
            "Collection Notes"
        ]

        # Find the discogs folder
        discogs_folder = Path.cwd() /"discogs"

        # Check whether the folder exists
        if not discogs_folder.exists():
            messagebox.showerror(
                "Folder Not Found",
                f"Could not find folder: {discogs_folder}"
            )
            return

        # Search for CSV files in the folder
        csv_files = list(discogs_folder.glob("*.csv"))

        if not csv_files:
            messagebox.showerror(
                "CSV Not Found",
                "No CSV files were found in the discogs folder."
            )
            return

        # Load the first CSV file found
        csv_file = csv_files[0]

        try:
            # Load only the specified columns into a DataFrame
            self.df = pd.read_csv(
                csv_file,
                usecols=self.columns
            )

            print(f"Loaded file: {csv_file}")
            print(self.df.head())

        except Exception as e:
            messagebox.showerror(
                "CSV Loading Error",
                str(e)
            )
            return

        # Display basic information in the Tkinter window
        self.label = tk.Label(
            root,
            text=f"Loaded {len(self.df)} records from {csv_file.name}",
            font=("Arial", 14)
        )
        self.label.pack(pady=20)

        # Display the DataFrame column names
        self.columns_label = tk.Label(
            root,
            text="Columns loaded:\n" + ",\n".join(self.df.columns),
            wraplength=750,
            justify="left"
        )
        self.columns_label.pack(padx=10, pady=10)

        self.table = tk.Toplevel(root)
        self.table.title("Data Table")
        self.table.geometry("1000x600")

        def fit_width(column):
            max_width = max(
                [len(str(column))] + [len(str(value)) for value in self.df[column]]
            )
            return max_width * 8

        self.tree = ttk.Treeview(
            self.table,
            columns=list(self.df.columns),
            show="headings"
        )
        self.tree.tag_configure("oddrow", background="white")
        self.tree.tag_configure("evenrow", background="#E8E8E8")
        scrollbar = ttk.Scrollbar(self.table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        for column in self.df.columns:
            self.tree.heading(column, text=column, command=lambda col=column: self.sort_by(col))
            self.tree.column(column, width=fit_width(column), anchor="w")

        for i, row in enumerate(self.df.itertuples(index=False, name=None)):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=row, tags=(tag,))

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")



    def sort_by(self, column):
        # Get current sort direction (default ascending)
        ascending = self.sort_directions.get(column, True)

        # Sort the DataFrame
        self.df = self.df.sort_values(
            by=column,
            ascending=ascending
        )

        # Toggle sort direction for next click
        self.sort_directions[column] = not ascending

        for col in self.df.columns:
            if col == column:
                arrow = " \\/ " if ascending else " /\\ "
                self.tree.heading(
                    col,
                    text=f"{col}{arrow}"
                )
            else:
                # Remove arrows from previously selected columns
                self.tree.heading(col, text=col)

        # Clear existing Treeview rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert sorted rows with alternating colors
        for i, row in enumerate(self.df.itertuples(index=False, name=None)):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=row, tags=(tag,))


if __name__ == "__main__":
    root = tk.Tk()
    app = DiscogsApp(root)
    root.mainloop()
