from multiapp import MultiApp
from my_apps import page1,page2

app = MultiApp()

app.add_app("Records joueurs", page1.app)
app.add_app("Resulats du jour", page2.app)

app.run()