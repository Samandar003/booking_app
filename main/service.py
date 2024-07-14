from .models import ScheduleModel, InstitutionModel, PostInstitModel, WorkingHoursModel
from datetime import datetime, timedelta

def show_available_hours(instit_obj, day):
    working_day_obj=WorkingHoursModel.objects.filter(day=day, institution=instit_obj).first()
    start_time=working_day_obj.open_time
    end_time=working_day_obj.close_time
    schedule_objs=ScheduleModel.objects.filter(day=day, institution=instit_obj).order_by("created_at")
    schedule_list=[]
    if len(schedule_objs)>0:
        if schedule_objs[0].start_time>start_time+timedelta(minutes=10):
            schedule_list.append([start_time, schedule_objs[0].start_time])
        for x in range(len(schedule_objs)-1):
            x_end=schedule_objs[x].end_time
            next_x_start=schedule_objs[x+1].start_time
            if x_end+timedelta(minutes=10)<next_x_start:
                schedule_list.append([x_end, next_x_start])
            
        if schedule_objs.last().end_time+timedelta(minutes=10)<end_time:
            schedule_list.append([schedule_objs.last().end_time, end_time])
    else:
        schedule_list.append([start_time.time(), end_time.time()])
    return schedule_list


def calculate_perhour(inst_obj, start_time, end_time):
    duration=end_time.time-start_time
    total_seconds=duration.total_seconds()
    hour=total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    total_hours=(minutes*0.1)+hour
    price=inst_obj.price_hour*total_hours
    return price, total_hours

# inst_obj=InstitutionModel.objects.all().first()
# print(show_available_hours(instit_obj=inst_obj, day="firday"))

