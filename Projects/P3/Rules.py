def is_ok(table, n):
    ''' Checks for violations of either of the three rules '''
    
    cc = check_count(table, n)
    cs = check_same(table, n)
    cd = check_duplicate(table, n)

    return cc and cs and cd


def check_count(table, n):
    ''' Checks rule #1 for violations'''

    def check_balance(row):
        count_1 = sum([1 for item in row if item == '1'])
        count_0 = sum([1 for item in row if item == '0'])

        return False if ((count_1 > n // 2) or (count_0 > n // 2)) else True

    for i in range(n):
        row = table[i]
        col = [row[i] for row in table]

        if not (check_balance(row) and check_balance(col)):
            return False

    # Return if there are more than one distinct values
    return True


def check_same(table, n):
    ''' Checks rule #2 for violations'''

    row_joint_entries, col_joint_entries = [], []

    # Calc rows
    for i in range(n):
        row = table[i]
        row_joint_entries.append(''.join(row))

    # Calc columns
    for i in range(n):
        col = [row[i] for row in table]        
        col_joint_entries.append(''.join(col))

    return (len(set(row_joint_entries)) == len(row_joint_entries)) and (len(set(col_joint_entries)) == len(col_joint_entries))


def check_duplicate(table, n):
    ''' Checks rule #3 for violations'''

    for i in range(n):
        row = table[i]
        col = [row[i] for row in table]
  
        # checking the conditions for rows and columns
        for j in range(n - 2):
            if (row[j] == row[j + 1] and row[j + 1] == row[j + 2] and row[j] != '-') or (col[j] == col[j + 1] and col[j + 1] == col[j + 2] and col[j] != '-'):
                return False
    return True