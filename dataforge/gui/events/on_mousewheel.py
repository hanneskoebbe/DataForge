def on_mousewheel(self, event):
    self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
