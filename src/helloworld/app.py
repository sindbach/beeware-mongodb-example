"""
My first application
"""
import toga
import pymongo
from random import seed 
from random import randint
from random import choice

from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class HelloWorld(toga.App):

    def startup(self):
        client = pymongo.MongoClient()
        database = client["beeware"]
        self.collection = database["orders"]

        self.choices = ["John", "Jane", "Jack", "Jill", "Jonas", "Jessica", "Jayden", "Jaime", "Julia", "Jasmine"] 
        seed(10)

        main_box = toga.Box(style=Pack(direction=COLUMN))

        button = toga.Button(
            'Create A Document',
            on_press=self.insert_random_document,
            style=Pack(padding=5)
        )

        display_label = toga.Label(
            'Documents: ',
            style=Pack(padding=(0, 5))
        )
        self.table = toga.Table(
            ['ID', 'Name', 'Order'], 
            missing_value="", 
            style=Pack(padding=5, height=300))
        self.populate_table()

        display_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        display_box.add(display_label)
        display_box.add(self.table)

        main_box.add(button)
        main_box.add(display_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def populate_table(self): 
        self.table.data = []
        cursor = self.collection.find().limit(20).sort("_id", -1)
        for document in cursor:
            self.table.data.append(document["_id"], document["name"], document["order"])
        return 

    def insert_random_document(self, widget):
        document = {"name": choice(self.choices), "order":randint(1, 1000)}
        result = self.collection.insert_one(document)        
        print("Inserted %s" % result.inserted_id)
        self.populate_table()
        return 

def main():
    return HelloWorld()
