import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
from datetime import date


def plot_to_pdf(export_data, output_path, tool_number):
    idx = "pos. nr."
    name = f"{date.today().isoformat()}_{tool_number}_evaluation.pdf"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with PdfPages(os.path.join(output_path, name)) as pdf:
        for param, df_dict in export_data.items():
            # page 1: Plot
            plt.figure(figsize=(10, 6))
            plt.plot(
                df_dict.get(idx, []),
                [float(str(x).replace(",", "."))
                    for x in df_dict.get("actual", [])],
                label="actual", marker="o"
            )
            plt.plot(
                df_dict.get(idx, []),
                [float(str(x).replace(",", "."))
                    for x in df_dict.get("nominal", [])],
                label="nominal", linestyle="-", color="green"
            )
            plt.plot(
                df_dict.get(idx, []),
                [n + u for n, u in zip(
                    [float(str(x).replace(",", "."))
                        for x in df_dict.get("nominal", [])],
                    [float(str(x).replace(",", "."))
                        for x in df_dict.get("upper tol.", [])]
                    )],
                label="upper tol.", linestyle="-", color="red"
            )
            plt.plot(
                df_dict.get(idx, []),
                [n + l for n, l in zip(
                    [float(str(x).replace(",", "."))
                        for x in df_dict.get("nominal", [])],
                    [float(str(x).replace(",", "."))
                        for x in df_dict.get("lower tol.", [])]
                    )],
                label="lower tol.", linestyle="-", color="red"
            )
            plt.title(f"chart: {param}")
            plt.xlabel("pos. nr.")
            plt.ylabel("value")
            plt.legend()
            plt.grid(True)
            plt.xticks(df_dict.get(idx, []), rotation=45)
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            # page 2: Rohdaten-Tabelle
            df_export = pd.DataFrame(df_dict).T  # DataFrame aus den Series
            _, ax = plt.subplots(figsize=(10, len(df_export) * 0.5 + 1))
            ax.axis('off')
            table = ax.table(cellText=df_export.values,
                             rowLabels=df_export.index,
                             loc='center',
                             cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(1.2, 1.2)
            plt.title(f"raw data: {param}")
            plt.tight_layout()
            pdf.savefig()
            plt.close()
