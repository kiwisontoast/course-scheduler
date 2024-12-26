import tkinter as tk
from tkinter import ttk
import sv_ttk
from tkinter import messagebox

class TimeSlot:
    def __init__(self, days, start_time, end_time):
        self.days = days
        self.start_time = start_time
        self.end_time = end_time

    def has_time_conflict(self, other):
        for day in self.days:
            if day in other.days:
                if not (self.end_time <= other.start_time or self.start_time >= other.end_time):
                    return True
        return False

class Course:
    def __init__(self, course_number):
        self.course_number = course_number
        self.time_slots = []

    def add_time_slot(self, days, start_time, end_time):
        self.time_slots.append(TimeSlot(days, start_time, end_time))

    def has_time_conflict(self, other):
        for my_slot in self.time_slots:
            for other_slot in other.time_slots:
                if my_slot.has_time_conflict(other_slot):
                    return True
        return False

class CourseRegistration:
    def __init__(self, root):
        self.root = root
        self.courses = {}
        self.schedule = []
        self.create_ui()

    def generate_schedule(self):
        self.schedule = []
        self.load_courses_from_file()
        categories = list(self.courses.keys())  # Use a list to maintain order
        self.process_courses(categories)

    def process_courses(self, categories):
        for category in categories:
            if category in self.courses:
                for course in self.courses[category]:
                    if not self.has_conflict_with_schedule(course):
                        time_slots_str = "\n".join(
                            f"  {time_slot.days} {format_time(time_slot.start_time)}-{format_time(time_slot.end_time)}"
                            for time_slot in course.time_slots
                        )
                        response = messagebox.askyesnocancel(
                            f"Accept {category} Course",
                            f"Accept course {course.course_number} in {category}?\n{time_slots_str}",
                            default=messagebox.YES
                        )
                        if response is None:
                            return
                        elif response:
                            self.schedule.append(course)
                            break
                        else:
                            continue

        self.display_schedule()



    def has_conflict_with_schedule(self, course):
        for scheduled_course in self.schedule:
            if course.has_time_conflict(scheduled_course):
                return True
        return False

    def display_schedule(self):
        self.schedule_text.delete(1.0, tk.END)
        for course in self.schedule:
            self.schedule_text.insert(tk.END, f"Course {course.course_number}:\n")
            for time_slot in course.time_slots:
                self.schedule_text.insert(tk.END, f"  {time_slot.days} {format_time(time_slot.start_time)}-{format_time(time_slot.end_time)}\n")

    def clear_entries(self):
        self.category_entry.delete(0, tk.END)
        self.course_number_entry.delete(0, tk.END)
        self.days_entry.delete(0, tk.END)

    def create_ui(self):
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)

        self.category_label = ttk.Label(self.frame, text="Category:")
        self.category_label.grid(row=0, column=0, padx=(0, 10))
        self.category_entry = ttk.Entry(self.frame)
        self.category_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        self.course_number_label = ttk.Label(self.frame, text="Course Number:")
        self.course_number_label.grid(row=1, column=0, padx=(0, 10))
        self.course_number_entry = ttk.Entry(self.frame)
        self.course_number_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        self.days_label = ttk.Label(self.frame, text="Days and Times (e.g., MWF, 8:00am-9:00am, TTH, 1:00pm-2:00pm):")
        self.days_label.grid(row=2, column=0, columnspan=2, padx=(0, 10))
        self.days_entry = ttk.Entry(self.frame)
        self.days_entry.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

        self.add_button = ttk.Button(self.frame, text="Add Course", command=self.add_course)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        self.generate_button = ttk.Button(self.frame, text="Generate Schedule", command=self.generate_schedule)
        self.generate_button.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        self.schedule_text = tk.Text(self.frame, height=10)
        self.schedule_text.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

    def add_course(self):
        category = self.category_entry.get()
        course_number = self.course_number_entry.get()
        days_times = self.days_entry.get()
        # Parse days and times
        days_times_list = days_times.split(", ")
        time_slots = []
        for i in range(0, len(days_times_list), 2):
            days = days_times_list[i]
            times = days_times_list[i+1]
            start_time, end_time = times.split("-")
            start_time = convert_time_to_float(start_time)
            end_time = convert_time_to_float(end_time)
            time_slots.append((days, start_time, end_time))

        if category not in self.courses:
            self.courses[category] = []

        course = Course(course_number)
        for days, start_time, end_time in time_slots:
            course.add_time_slot(days, start_time, end_time)
        self.courses[category].append(course)

        # Write course data to file
        with open("courses.txt", "a") as file:
            file.write(f"Category: {category}\n")
            file.write(f"Course Number: {course_number}\n")
            for time_slot in course.time_slots:
                file.write(f"  {time_slot.days} {format_time(time_slot.start_time)}-{format_time(time_slot.end_time)}\n")
            file.write("\n")

        self.clear_entries()

    def load_courses_from_file(self):
        try:
            with open("courses.txt", "r") as file:
                lines = file.readlines()
                category = None
                course_number = None
                course = None
                for line in lines:
                    line = line.strip()
                    if line.startswith("Category:"):
                        category = line.split(": ")[1]
                        if category not in self.courses:
                            self.courses[category] = []
                    elif line.startswith("Course Number:"):
                        course_number = line.split(": ")[1]
                        course = Course(course_number)
                    elif line.startswith("  "):
                        days, times = line[2:].split(" ", 1)
                        start_time, end_time = times.split("-")
                        start_time = convert_time_to_float(start_time)
                        end_time = convert_time_to_float(end_time)
                        course.add_time_slot(days, start_time, end_time)
                    elif line == "":
                        self.courses[category].append(course)
        except FileNotFoundError:
            pass

def __init__(self, root):
    self.root = root
    self.courses = {}
    self.schedule = []
    self.load_courses_from_file()
    self.create_ui()


    # Prompt for additional courses
    response = messagebox.askyesnocancel("Add Another Course", "Add another course in the same category?", default=messagebox.YES)
    if response is None:
        return
    elif response:
        self.category_entry.insert(0, category)
    else:
        self.category_entry.delete(0, tk.END)
        self.category_entry.focus_set()





def convert_time_to_float(time_str):
    time_str = time_str.lower()
    if "am" in time_str:
        time_str = time_str.replace("am", "")
        hour, minute = map(int, time_str.split(":"))
        if hour == 12:
            hour = 0
    elif "pm" in time_str:
        time_str = time_str.replace("pm", "")
        hour, minute = map(int, time_str.split(":"))
        if hour != 12:
            hour += 12
    else:
        raise ValueError("Invalid time format. Use AM/PM.")
    return hour + minute / 60

def format_time(time_float):
    hour = int(time_float)
    minute = int((time_float % 1) * 60)
    am_pm = "AM" if hour < 12 else "PM"
    if hour == 0:
        hour = 12
    elif hour > 12:
        hour -= 12
    return f"{hour}:{minute:02d}{am_pm}"

def main():
    root = tk.Tk()
    root.title("Course Registration")
    sv_ttk.set_theme("dark")
    app = CourseRegistration(root)
    root.mainloop()

if __name__ == "__main__":
    main()
