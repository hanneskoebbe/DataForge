from scripts.select_dir import select_dir
from scripts.import_data import import_data
from scripts.extract_params import extract_params
from scripts.tool_number import tool_number
from scripts.gen_temp_data import gen_temp_data
from scripts.gen_import_data import gen_import_data
from scripts.plot_to_pdf import plot_to_pdf
from gui.create_gui import AppGUI

# Starte die GUI als Klasse
AppGUI(
    select_dir,
    import_data,
    extract_params,
    tool_number,
    gen_temp_data,
    gen_import_data,
    plot_to_pdf
)
