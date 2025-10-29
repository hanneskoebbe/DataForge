def on_mousewheel(self, event, canvas):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
