from app.db.database import Base, engine
from app.db.models import server, group, tag, log, report_schedule

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Done.")

