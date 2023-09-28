from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import GUI

class p_sample1():
    def __init__(self, app: "GUI") -> None:
        self.id = "sample1"
        self.log = f"[{self.id}] "
        print(self.log+"loaded!")

        @app.on_draw
        def print_hello():
            print(self.log+"line drew!")

        @app.on_change_color
        def indicate():
            print(self.log+"color changed!")