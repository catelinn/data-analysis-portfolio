# Question:
# Create a function that opens the flowers.txt, 
# reads every line in it, and saves it as a dictionary. 
# The main (separate) function should take user input (user's first name and last name) 
# and parse the user input to identify the first letter of the first name. It should then 
# use it to print the flower name with the same first letter (from dictionary created in 
# the first function).

# Write your code here
# HINT: create a dictionary from flowers.txt
def create_flowerdict(fname):
    f_dict = {}
    with open(fname) as f:
        for line in f:
            key=line.split(': ')[0].upper()
            value=line.split(': ')[1].strip()
            f_dict[key]=value
    return f_dict

# HINT: create a function to ask for user's first and last name
# when the script is run, this main function will be called
def main():
    flowers_dict = create_flowerdict("flowers.txt")
    name = input("Enter your First [space] Last name only: ")
    print("Unique flower name with the first letter: {}".format(flowers_dict[name[0].upper()]))

if __name__ == "__main__":
    main()
