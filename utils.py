def getAveragePB( PBDAY : dict[ str, int ]) -> dict[ str, int] :
    '''
    Returns the average PB of more than one PB of a specific day
    Returns it as dict[ str, int] to use directly just like the other PBs of that day
    '''

    listOfRawPB : list[int] = [ val for key, val in PBDAY.items() ] # making a list of all the attempts of that specific day
    add : int = 0   # initializing the value of the result of addition
    for pb in listOfRawPB:
        if pb != None:      # means its an actual number
            add += pb   # adding every attempt to the add variable
        else:
            return np.nan   # making it a NaN value (an empty value, so it dont show up as a pint at the final plot)

    averagepb : int = add // ( len(PBDAY) )  # average personal best = the addition of them all devided by the total number of personal bests in the current day (for now, floats are not supported yet!)

    return averagepb