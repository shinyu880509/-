from flask_script import Manager
import catStock
from app import app

manager = Manager(app)

@manager.command
def refresh():
    catStock.catStock()

@manager.command
def test():
    print('test')

if __name__ == "__main__":
    manager.run()