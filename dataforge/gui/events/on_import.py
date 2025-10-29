from tkinter import messagebox


def on_import(self):
    import_dir = self.select_dir()
    if not import_dir:
        messagebox.showinfo("Abbruch", "Kein Ordner ausgewählt.")
        return

    self.raw_excel_data = self.gen_raw_excel_data(import_dir)

    if not self.raw_excel_data:
        messagebox.showwarning(
            "Keine Daten", "Keine gültigen Excel-Dateien gefunden."
        )
        return

    self.import_data = self.gen_import_data(self.raw_excel_data)

    self.gen_all_data()

    self.widget()
