def ecrire_plan(path_plan, directions):
    with open(path_plan, 'w') as f:
    # Write the Python code to the file
    for i in range(len(directions)):
        if directions[0] == 'GO':
            f.write(f'GO {directions[1]}\n')
        elif directions[0] == 'TURN':
            f.write(f'STOP\n')
            f.write(f'TURN {directions[1]}\n')
        elif directions[0] == 'FINISH':
            f.write(f'STOP\n')
            f.write(f'FINISH')


def 