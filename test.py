# this file is for test scripting relating to the sudoku solver file titled sudoku.py

import numpy as np
import sys




SUDOKU_INPUT = "000607095809000207006009300600020409100000020000006000010000940000830000002900150"




def initialize_grid(sudoku_input):
    all_ = [1,2,3,4,5,6,7,8,9]

    string_list = list(map(int, list(sudoku_input))) # convert input to a list of strings and then change all of those string numbers to ints
    arr_1d = np.array(string_list) # convert to numpy array
    sudoku = np.reshape(arr_1d, (9,9)) # convert to 9x9 array

    solutions = np.zeros((9,9), dtype = object) # create an array of lists to assign possible solutions to later

    del(string_list, arr_1d) # delete what we don't need ( not sure if this is necessary, will Google it)

    # assign a label to the numbers that were present at the beginning of the puzzle aka GRID #'s
    for row_index, row in enumerate(sudoku):
        for column_index, num in enumerate(row):
            if num in all_: # find the numbers that are part of the initial grid
                solutions[row_index, column_index] = ["GRID #"]
            else: # determine possible initial solutions to quicken algorithm
                sol = find_solutions(sudoku, row_index, column_index, solutions)

                if len(sol) == 1: # if only one solution, fill in grid with it in a different color ############################
                    solutions[row_index, column_index] = ["GRID #"]
                    sudoku[row_index, column_index] = sol[0]
                else:
                    solutions[row_index, column_index] = sol

    row_start = 0
    column_start = 0
    forward = True

    return sudoku, solutions, row_start, column_start, forward


def move(row_index, column_index, forward):
    # GOING FORWARD
    if forward == True: 
        if column_index == 8 and row_index == 8:
            pass # SUCCESS, I think
        elif 0 <= column_index < 8: # increment column index before end of row
            column_index += 1
        elif column_index == 8: # increment row and restart column index
            column_index = 0 
            row_index += 1
        else:
            sys.exit("Within move(forward=True) function, something went wrong. DEBUG.")
        return row_index, column_index, forward
    # GOING BACKWARD
    elif forward == False:
        if column_index <= 0 and row_index <= 0:
            sys.exit("Went backwards to or past the 0th index. DEBUG.")
        elif 0 < column_index <= 8: # decrement column index before end of row
            column_index -= 1
        elif column_index == 0 and row_index != 0: # decrement row and restart column index
            column_index = 8 
            row_index -= 1
        else:
            sys.exit("Within move(forward=False) function, something went wrong. DEBUG.")
        return row_index, column_index, forward
    # SOMETHING ELSE
    else: 
         sys.exit("Wrong parameter, move(forward=???) function. DEBUG.")


def find_solutions(sudoku, row_index, column_index, solutions): # fxn to find possible sudoku solutions at the current location in the grid
    all_ = [1,2,3,4,5,6,7,8,9]
    
    horz_and_vert = np.append(sudoku[row_index,:], sudoku[:,column_index]) # combine horizontal and vertical elements into one list
    flattened_box = sudoku[row_index-row_index % 3:row_index-row_index % 3 + 3, column_index-column_index % 3:column_index-column_index % 3 + 3].flatten() # flatten the 3x3 local box    
    all_checks = np.append(horz_and_vert, flattened_box) # all of the numbers that can't be solutions to  current index
    sol = [n for n in all_ if n not in all_checks] # check for what possible numbers could be

    return sol


# Load and initialize the grid. Also, label GRID #'s in the solution array
s, sols, r_i, c_i, forward = initialize_grid(sudoku_input = SUDOKU_INPUT)
print(sols)


while True:
    num = s[r_i, c_i]
    
    print(r_i, c_i, num)
    print(s)

    if sols[r_i, c_i] == ["GRID #"]: # SKIP GRID #'s
        r_i, c_i, forward = move(r_i, c_i, forward)
    elif sols[r_i, c_i] != ["GRID #"]: # MOVING FORWARD
        for num in sols[r_i, c_i]:
            solution_check = find_solutions(s, r_i, c_i, sols)

            if len(solution_check) == 0: # need to go backwards because there are no solutions left
                r_i, c_i, forward = move(r_i, c_i, forward = False)
                break           
            elif len(sols[r_i, c_i]) == 1: # only solution
                s[r_i, c_i] = sols[r_i, c_i][0] # assign new value to the sudoku grid solution
                r_i, c_i, forward = move(r_i, c_i, forward = True)
                # UPDATE UI/UX HERE
            else: # there is more than one possible solution
                s[r_i, c_i] = sols[r_i, c_i][-1]
                sols[r_i, c_i].pop()
                r_i, c_i, forward = move(r_i, c_i, forward = True)
                break

    elif forward == False and sols[r_i, c_i] != ["GRID #"]: # JUST MOVED BACKWARDS
        pass
    elif r_i == 8 and c_i == 8: # SUCCESS!
        pass




