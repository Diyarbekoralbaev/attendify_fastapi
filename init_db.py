from database import Base,engine
from models import EmployeeModel, DepartmentModel, EmployeeAttendanceModel, ClientsModel, ClientVisitHistoryModel

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized")
    return