from main_window import MainAPP, Gui, Events, Core
import gui
import core
import events


def main():
    # gui = Gui(
    #     widgets=gui_.widgets,
    #     select_dir=gui_.select_dir
    #     )

    # events = Events(
    #     on_closing=events.on_closing,
    #     on_mousewheel=events.on_mousewheel,
    #     on_import=events.on_import,
    #     on_export=events.on_export,
    #     on_add_par=events.on_add_par
    # )

    # core = Core(
    #     gen_raw_import_data=core.gen_raw_import_data,
    #     gen_import_data=core.gen_import_data,
    #     gen_all_data=core.gen_all_data,
    #     get_temp=core.get_temp,
    #     get_data=core.get_data,
    #     temp_to_data=core.temp_to_data,
    #     convert_seperator=core.convert_seperator,
    #     plot_to_pdf=core.plot_to_pdf
    # )

    app = MainAPP(gui, events, core, data_store)
    app.run()


if __name__ == "__main__":
    main()
