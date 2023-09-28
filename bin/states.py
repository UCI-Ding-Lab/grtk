from main import GUI
            
class on_draw():
    def __init__(self, app) -> None:
        self.app: GUI = app
    def __call__(self, func):
        self.app.container.on_draw_job.append(func)

class on_change_color():
    def __init__(self, app) -> None:
        self.app: GUI = app
    def __call__(self, func):
        self.app.pref.on_change_color_job.append(func)
        
class on_closed():
    pass