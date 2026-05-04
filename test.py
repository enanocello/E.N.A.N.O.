from pathlib import Path
from utils.terminal import clear
import services.connectService as connectService
import services.courseService as courseService
import utils.prompts as prompts

BASE_DIR = Path(__file__).resolve().parent
dbPath = BASE_DIR / "data" / "enano.db"
conn = connectService.connect(dbPath)
cursor = connectService.getCursor(conn)

#clear()
courses = courseService.getCourse("2026-1",cursor,"courseCode")
print(courses)

courseService.addCourse("2026-1","HOLA","Hola",cursor,conn)