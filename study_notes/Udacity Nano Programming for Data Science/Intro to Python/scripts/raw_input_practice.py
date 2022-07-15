"""
you're a teacher who needs to send a message to each of your students 
reminding them of their missing assignments and grade in the class. 
You have each of their names, number of missing assignments, and grades 
on a spreadsheet and just have to insert them into placeholders in the 
message you have drafted.
"""

# get and process input for a list of names
names =  input("Enter names seperated by commas: ").title().split(',')

# get and process input for a list of the number of assignments
assignments =  input("Enter assignment counts seperated by commas: ").split(',')

# get and process input for a list of grades
grades =  input("Enter grades seperated by commas: ").split(',')

# message string to be used for each student
# HINT: use .format() with this string in your for loop
message = "Hi {},\n\nThis is a reminder that you have {} assignments left to \
submit before you can graduate. You're current grade is {} and can increase \
to {} if you submit all assignments before the due date.\n\n"

# write a for loop that iterates through each set of names, assignments, and grades to print each student's message
for n, a, g in zip(names, assignments, grades):
    print(message.format(n, a, g, str(int(g)+2*int(a))))

