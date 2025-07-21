# app/workers/report_worker.py

from datetime import datetime, timedelta
from celery import shared_task
from app.db.database import SessionLocal
from app.db.crud import report_schedule as report_crud
from app.services import report_engine
import logging
logging.getLogger("asyncua").setLevel(logging.WARNING)

@shared_task
def scheduled_report_runner():
    db = SessionLocal()
    try:
        schedules = report_crud.get_all_report_schedules(db)
        now = datetime.now()
        for sched in schedules:
            if not sched.is_enabled:
                continue

            last_run = sched.last_run_timestamp or datetime.min
            due = False

            if sched.schedule_type == "Daily" and (now.date() > last_run.date()):
                due = True
            elif sched.schedule_type == "Weekly" and (now - last_run).days >= 7:
                due = True
            elif sched.schedule_type == "Monthly" and now.month != last_run.month:
                due = True

            if due:
                start_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
                end_dt = now
                if sched.report_format.lower() == "pdf":
                    report_engine.generate_pdf_report(sched, start_dt, end_dt)
                else:
                    report_engine.generate_excel_report(sched, start_dt, end_dt)

                report_crud.update_report_last_run(db, sched.id, now)
                logging.info(f"Generated {sched.report_format.upper()} report for {sched.name}")
    except Exception as e:
        logging.error(f"Scheduled report task failed: {e}")
    finally:
        db.close()

@shared_task(name="app.workers.report_worker.run_report_task")
def run_report_task(schedule_id: int):
    db = SessionLocal()
    try:
        sched = report_crud.get_schedule_by_id(db, schedule_id)
        if not sched:
            logging.error(f"Report ID {schedule_id} not found")
            return

        now = datetime.now()
        start_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_dt = now

        if sched.report_format.lower() == "pdf":
            report_engine.generate_pdf_report(sched, start_dt, end_dt)
        else:
            report_engine.generate_excel_report(sched, start_dt, end_dt)

        report_crud.update_report_last_run(db, sched.id, now)
        logging.info(f"Manually generated {sched.report_format.upper()} report for {sched.name}")
    except Exception as e:
        logging.error(f"Failed to manually run report {schedule_id}: {e}")
    finally:
        db.close()
