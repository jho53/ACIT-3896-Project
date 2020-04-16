import timetable_ga as tbga
from threading import Thread

pure_ga1 = Thread(target=tbga.generate_data, args=(100, False))
pure_ga2 = Thread(target=tbga.generate_data, args=(500, False))
ids_ga1 = Thread(target=tbga.generate_data, args=(100, True))
ids_ga2 = Thread(target=tbga.generate_data, args=(500, True))

pure_ga1.start()
pure_ga2.start()
ids_ga1.start()
ids_ga2.start()

