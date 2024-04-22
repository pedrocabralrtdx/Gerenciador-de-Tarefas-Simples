import PySimpleGUI as sg
import sqlite3


def criar_banco_dados():
    conexao = sqlite3.connect('tarefas.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY,
            descricao TEXT
        )
    ''')
    conexao.commit()
    conexao.close()


def adicionar_tarefa(descricao):
    conexao = sqlite3.connect('tarefas.db')
    cursor = conexao.cursor()
    cursor.execute('INSERT INTO tarefas (descricao) VALUES (?)', (descricao,))
    conexao.commit()
    conexao.close()

def exibir_tarefas():
    conexao = sqlite3.connect('tarefas.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM tarefas')
    tarefas = cursor.fetchall()
    conexao.close()
    return tarefas

def excluir_tarefas():
    conexao = sqlite3.connect('tarefas.db')
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM tarefas')
    conexao.commit()
    conexao.close()

layout = [
    [sg.Text('Descrição da Tarefa:'), sg.InputText(key='descricao')],
    [sg.Button('Adicionar Tarefa'), sg.Button('Mostrar Tarefas'), sg.Button('Excluir Todas as Tarefas')],
    [sg.Text(size=(40, 10), key='output')]
]

janela = sg.Window('Gerenciador de Tarefas').Layout(layout)

criar_banco_dados()

while True:
    evento, valores = janela.Read()
    if evento == sg.WINDOW_CLOSED:
        break
    elif evento == 'Adicionar Tarefa':
        descricao = valores['descricao']
        adicionar_tarefa(descricao)
        sg.popup('Tarefa adicionada com sucesso!')
    elif evento == 'Mostrar Tarefas':
        tarefas = exibir_tarefas()
        output_text = ''
        for tarefa in tarefas:
            output_text += f'Tarefa {tarefa[0]}: {tarefa[1]}\n'
        janela['output'].update(output_text)
    elif evento == 'Excluir Todas as Tarefas':
        excluir_tarefas()
        janela['output'].update('')
        sg.popup('Todas as tarefas foram excluídas!')

janela.close()