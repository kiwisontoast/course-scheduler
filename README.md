# Course Scheduler
The Course Registration System is a user-friendly application designed to manage and schedule courses. It allows users to add courses with specific time slots and categories, ensuring that there are no conflicts in the schedule.
THIS PROGRAM WAS MADE SPECIFICALLY TO WORK WITH THE SCHEDULING PROGRAM OF THE UNIVERSITY OF TEXAS AT AUSTIN (MAY OR MAY NOT WORK WITH YOUR OWN UNIVERSITY PROGRAM)

## Key Features
Course Management: Add courses with multiple time slots and categories
Time Conflict Detection: Automatically detects and prevents scheduling conflicts between courses
User-Friendly Interface: Easy-to-use GUI for adding courses and generating schedules including light/dark mode toggle
Real-Time Schedule Updates: Displays the current schedule and updates it dynamically
Clipboard Integration: Copies course numbers to the clipboard automatically for easy reference

## Dependencies
- This project requires:
  ~ tkinter
  ~ sv_ttk
  ~ pyperclip

## Usage
Start the Application: Run the coursetester.py file to start the application.
1. Add a Course:
  Enter the category and course number.
  Specify the days and times for the course (e.g., MWF, 8:00am-9:00am, TTH, 1:00pm-2:00pm).
  Click the "Add Course" button.
(It might be faster to add courses directly into the text file at scale)

3. Generate Schedule:
  Click the "Generate Schedule" button to process courses and create a schedule.
  The application will prompt for confirmation before adding each course to the schedule.

View Schedule:
   The current schedule is displayed in the text box at the bottom of the application window.

## Warnings
   **Operating Systems**
   This is optimized for Windows. While it may run on other operating systems, 
   some visual elements and GUI components might behave differently.
   **Default Values**
   - No courses by default unless you use the sample course text file
   - Default theme is set to "Dark Mode"
   **Data Retrieval**
   - Course Data: Course data is loaded from the courses.txt file. If the file does not exist, it will be created automatically
   - Invalid Data: Invalid course data may result in errors when generating the schedule. Ensure that the data is correctly formatted


## Authors
- Dev Shroff





