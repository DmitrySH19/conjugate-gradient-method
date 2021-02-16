import numpy as np
from numpy import linalg as LA
import PySimpleGUI as sg


def is_pos_def(x):
    """check if a matrix is symmetric positive definite"""
    return np.all(np.linalg.eigvals(x) > 0)

def conjugate_gradient(A, b):
    a = A
    A = (a.T).dot(A)

    b = (a.T).dot(b)
    if (is_pos_def(A) == False) and (A == A.T).any():
        return ('Matrix A needs to be symmetric positive definite (SPD)')
    r = b
    k = 0
    x = np.zeros(A.shape[-1])
    while LA.norm(r) > 1e-10 :
        if k == 0:
            p = r
        else:
            gamma = - (p @ A @ r)/(p @ A @ p)
            p = r + gamma * p
        alpha = (p @ r) / (p @ A @ p)
        x = x + alpha * p
        r = r - alpha * (A @ p)
        k =+ 1
    return x

if __name__ == '__main__':

    cell_size = (5, 2)
    matrix = []

    col = 0
    row = 0
    random = True
    show = True
    input_layout = [
        [sg.Text('Enter the dimension of the matrix:'), ],
        [sg.Text('Colomns:'), sg.InputText('5',justification='center', size=cell_size, key='col'), ],
        [sg.Text('Rows:',), sg.InputText('5',justification='center', size=cell_size, key='row'), ],
        [sg.Checkbox('Randomize matrix',key= 'random', default=True),],
        [sg.Button(button_text='Enter', key='-IN-'), sg.Button('Exit',), ],
    ]
    window_input = sg.Window('Matrix dimension', input_layout, font='Helvetica 14', element_justification='r')
    window = window_input

    while True:  # The Event Loop
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-IN-':
            if values['col'] != '' and values['row'] != 0:

                window.close()
                layout = []
                colomn = []
                col = int(values['col'])
                row = int(values['row'])
                random = bool(values['random'])

                layout.append([sg.Text('A ({} x {})'.format(col,row),justification='left', size=(15,2)),sg.Text('b',justification='r', size=(10,2)) ])
                if random:
                    if col == row:
                        a = np.random.randint(-100, 100, size=[col,row])
                        matrix = np.tril(a) + np.tril(a, -1).T
                        b = np.random.randint(-100, 100,  size=col)
                    else:
                        matrix = np.random.randint(-100, 100, size=[col, row])
                        b = np.random.randint(-100, 100, size=col)

                    for i in range(col):
                        colomn.append([])
                        for j in range(row):
                            colomn[i].append(
                                sg.InputText(matrix[i][j], justification='center', size=cell_size,background_color='yellow', key= str(i) +' '+ str(j)))
                        colomn[i].append(sg.Input(b[i],justification='center', size=cell_size, key='b' + str(i),background_color='red'))



                    layout.append([sg.Column(colomn, scrollable=True, size= (500,300)),])
                    layout.append([sg.Multiline(visible=False,key='Output',size=(45,10),)])
                    layout.append([sg.Button(button_text='solve', key='solve'),sg.Button('New matrix', key='new'), sg.Button('Exit', ),])
                    window = sg.Window('Solve', layout, font='Helvetica 14', element_justification='c')
                else:
                    for i in range(col):
                        colomn.append([])
                        for j in range(row):
                            colomn[i].append(
                                sg.InputText('0', justification='center', size=cell_size,
                                             background_color='yellow', key=str(i) +' '+ str(j)))
                        colomn[i].append(sg.Input('0', justification='center', size=cell_size, key='b' + str(i),
                                                  background_color='red'))

                    layout.append([sg.Column(colomn, scrollable=True, size=(500, 300)), ])
                    layout.append([sg.Multiline(visible=False, key='Output', size=(45, 10))])
                    layout.append([sg.Button(button_text='solve', key='solve'),sg.Button('New matrix', key='new'), sg.Button('Exit', ), ])
                    window = sg.Window('Solve', layout, font='Helvetica 14', element_justification='c')

                # for i in range(col):
                #     layout.append([])
                #     for j in range(row):
                #         layout[i].append(sg.InputText('0',justification='center',size=cell_size, key=str(i)+str(j)))
                # layout.append([sg.Button(button_text='solve', key='-solve-'), sg.Button('Exit',)])
                # window = sg.Window('Draw spline', layout, font='Helvetica 14', finalize=True)
            else:
                sg.Popup('Colomns or Rows are empty')

        if event == 'new':
            window.close()
            new_layout= [
                [sg.Text('Enter the dimension of the matrix:'), ],
                [sg.Text('Colomns:'), sg.InputText('5', justification='center', size=cell_size, key='col'), ],
                [sg.Text('Rows:', ), sg.InputText('5', justification='center', size=cell_size, key='row'), ],
                [sg.Checkbox('Randomize matrix', key='random', default=True), ],
                [sg.Button(button_text='Enter', key='-IN-'), sg.Button('Exit', ), ],
            ]
            window = sg.Window('Matrix dimension', new_layout, font='Helvetica 14', element_justification='r')
        if event == 'solve':
            A = []
            b = []
            for i in range(col):
                A.append([])
                for j in range(row):
                    if values[str(i)+' '+str(j)] != '':
                        t = np.float64(values[str(i)+' '+str(j)])
                        A[i].append(t)
                    else:
                        sg.Popup('cell at index '+ str(i+1)+' '+str(j+1) + ' filled in incorrectly')
            matrix = np.array(A)

            for i in range(col):
                b.append(np.float64(values['b'+ str(i)]))
            b = np.array(b)
            window.FindElement('Output').Update(visible=True)
            x = (conjugate_gradient(matrix, b))
            if str(x) != 'Matrix A needs to be symmetric positive definite (SPD)':
                output_str = ''
                for i in range(len(x)) :
                    output_str += 'x' + str(i) + ': ' + str(x[i]) + '\n'
                window.FindElement('Output').Update(output_str)
            else:
                window.FindElement('Output').Update('Matrix A needs to be symmetric positive definite (SPD)')



