# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

def get_date(today):

    weekday = days[today.weekday()]
    month = today.strftime('%b')
    day = today.day
    return (weekday, month, day)

def print_tasks(choice):
    today = datetime.today()
    if choice == '1':
        date = get_date(today)
        print("Today {} {}:".format(date[1], date[2]))
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if not len(rows):
            print("Nothing to do!\n")
        else:
            for i,row in enumerate(rows):
                print("{}. {}".format(i + 1, row.task))
            #print(rows)
    elif choice == "2":
        for counter in range(0, 7):
            date = get_date(today)
            print("{} {} {}:".format(date[0], date[1], date[2]))
            rows = session.query(Table).filter(Table.deadline == today.date()).all()
            if not len(rows):
                print("Nothing to do!\n")
            else:
                for i,row in enumerate(rows):
                    print("{}. {}".format(i + 1, row.task))
            print()
            today = today + timedelta(days=1)
        print()
    else:
        rows = session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        if not len(rows):
            print("Nothing to do!\n")
        else:
            for i,row in enumerate(rows):
                print("{}. {}. {} {}".format(i + 1, row.task, row.deadline.day, row.deadline.strftime('%b')))



#print_tasks()
while True:
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
    choice = input()
    if choice == '0':
        print("Bye!")
        break
    elif choice == '5':
        print("\nEnter task")
        task = input()
        print("Enter deadline")
        deadline = input()
        deadline = datetime.strptime(deadline, '%Y-%m-%d')
        new_row = Table(task=task, deadline=deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!\n")
    elif choice == "4":
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
        print("Missed tasks:")
        if not len(rows):
            print("Nothing is missed!\n")
        else:
            for i, row in enumerate(rows):
                print("{}. {}. {} {}".format(i + 1, row.task, row.deadline.day, row.deadline.strftime('%b')))
        print()
    elif choice == "6":
        rows = session.query(Table).order_by(Table.deadline).all()
        if not len(rows):
            print("Nothing to delete\n")
        else:
            print("Chose the number of the task you want to delete:")
            for i, row in enumerate(rows):
                print("{}. {}. {} {}".format(i + 1, row.task, row.deadline.day, row.deadline.strftime('%b')))
            task_no = int(input())
            deleted_row = rows[task_no - 1]
            session.delete(deleted_row)
            session.commit()
            print("The task has been deleted!\n")
    else:
        print_tasks(choice)

