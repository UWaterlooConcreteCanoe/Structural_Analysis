import matplotlib.pyplot as plt


# Example 1: Text

# Some code here...
final_result = 12345

# print() is replaced by a function returning the string
def TextResult():
    
    return "The final result is: " + str(final_result)



# Example 2: Graph

# We only send the arrays and plot properties through the function
# Use the order (x array, y array, title, xlabel, ylabel)
def Graph1():
    # Some code here...
    x = [1, 2, 3, 4, 5]
    y = [13, 15, 2, 14, 12]
    
    return x, y, "Graph Title", "X Label", "Y Label"



# Example 3: Graph with input

# We only send the arrays and plot properties through the function
# Use the order (x array, y array, title, xlabel, ylabel)

# BECAUSE we are taking inputs into the function, we want to make sure the y array we have in the function depends
# on the inputs of the FUNCTION, not whatever is defined in the script. That is why the y array in this example is re-defined
# using the function inputs when we return it.
def Graph2(in1, in2, in3):
    
    # Some code here...
    x1 = [1, 2, 3, 4, 5, 6, 7]
    y1 = [0, in1, 0, in2, 0, in3, 0]
    
    x2 = [1, 2, 3, 4, 5, 6, 7]
    y2 = [50, in1, 50, in2, 50, in3, 50]
    
    # Return a list of each of the x, y pairs you want to graph!
    return [x1, x2], [y1, y2], "Graph Title", "X Label", "Y Label"
