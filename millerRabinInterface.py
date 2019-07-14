import tkinter as tk  # utilizado para criar a interface do usuario
from math import log10
from random import randrange  # retorna um numero aleatorio
from tkinter import *
from tkinter import ttk


def MillerRabin(n, t):  # Realiza o Teste de Fermat t vezes para o numero n
    if t > n - 3:  # o numero de tentativas nao pode exceder n-3
        t = n - 3
    s = 0
    m = n - 1
    div = divmod(m, 2)
    while div[1] == 0:  # encontra r e s de n-1= (2^s)m
        m = div[0]
        div = divmod(m, 2)
        s += 1

    r = []  # será a lista com os os restos da divisao sucessiva de m por 2
    while m > 0:  # encontra os r_1 de da conversao para base 2
        divisao = divmod(m, 2)
        m = divisao[0]  # faz m igual ao quaciente da divisão de m por 2
        r.append(divisao[1])  # adiciona m mod 2 na lista r

    bases = []
    j = 0
    while j < t:  # cria uma lista com t numeros inteiros distintos petencentes ao intervalo  [2,n-1[
        a_i = randrange(2, n - 1)
        if a_i not in bases:
            bases.append(a_i)
            j += 1
    for a in bases:
        e = a  # para nao alterar o valo de a, usei outra variavel com seu valor
        y = a  # como m é impar, r[0] sempre é 1, sendo descencessario fazer e**r[0]
        for expoente in r[1:]:  # calcula a^k mod n pelo algoritmo da reducao de custo de a^c mod n
            e = e * e % n  # é mais rápido calcular uma multiplicação do que uma potencia
            if expoente == 1:
                y = y * e % n
        if y != 1 and y != n - 1:
            i = 1
            while i <= s - 1 and y != n - 1:
                y = y * y % n
                if y == 1:
                    return "composto"
                i += 1
            if y != n - 1:
                return "composto"
    return "primo"  # se ao final de t testes, n não for como composto, dizemos que ele é primo


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.numero = Entry()
        self.tentativas = Entry(width=5)
        self.lbTentativas = Label(text="Tentativas")
        self.lbNumero = Label(text="Numero")
        self.btMillerRabin = ttk.Button(text="Miller-Rabin", style="C.TButton")
        self.btBuscar = ttk.Button(text="buscar primo", style="C.TButton")
        self.style = ttk.Style()
        self.lbresultado = Label(text="")
        self.metodos = Label(text="Click no Método")
        self.QUIT = ttk.Button(text="SAIR", style="C.TButton",
                               command=root.destroy)
        self.pack()
        self.createWidgets()

    def teste_de_MillerRabin(self):
        n = self.numero.get()
        t = self.tentativas.get()
        if n.isnumeric() and t.isnumeric():
            n = int(n)
            t = int(t)

            if n > 3:
                resultado = MillerRabin(n, t)

                if resultado == "composto":
                    self.lbresultado["text"] = "composto"
                elif resultado == "primo":
                    if t < 27:
                        confiabilidade = 100 - 100 / 4 ** t
                        self.lbresultado["text"] = "Primo com " + str(confiabilidade) + "%" + " de confiança"
                    else:
                        confiabilidade = -log10(4) * t
                        self.lbresultado["text"] = "Primo com menos que 10 elevado a" + str(
                            confiabilidade) + "%\n" + " de chance de erro"
            elif int(self.numero.get()) == 2 or int(self.numero.get()) == 3:
                self.lbresultado["text"] = "Primo"
                return
            else:
                self.lbresultado["text"] = "Digite um numero maior que 1"
                return

        else:
            self.lbresultado["text"] = "Digite numeros inteiros positivos"

    def encontrar_primo(self):
        n = str(self.numero.get())
        t = str(self.tentativas.get())
        if n.isnumeric() and t.isnumeric():
            n = int(n)
            t = int(t)
            if n > 3:
                confiabilidade = 100 - 100 / pow(4, t)
                if n % 2 == 0:
                    frente = n + 1
                    atras = n - 1
                else:
                    frente = n
                    atras = n - 2
                while True:
                    if MillerRabin(frente, t) == "primo":
                        if t < 27:
                            confiabilidade = 100 - 100 / 4 ** t
                            self.lbresultado["text"] = "Um numero primo proximo de " + str(n) + " é: " + str(frente) +"\n com " + str(confiabilidade) + "%" + " de confiança"
                        else:
                            confiabilidade = -log10(4) * t
                            self.lbresultado["text"] = "Um numero primo proximo de " + str(n) + " é: " + str(frente) + "\n" + "com menos que 10 elevado a" + str(confiabilidade) + "%\n" + " de chance de erro"
                        break
                    elif MillerRabin(atras, t) == "primo":
                        if t < 27:
                            confiabilidade = 100 - 100 / 4 ** t
                            self.lbresultado["text"] = "Um numero primo proximo de " + str(n) + " é: " + str(atras) + "\n com " + str(confiabilidade) + "%" + " de confiança"
                        else:
                            confiabilidade = -log10(4) * t
                            self.lbresultado["text"] = "Um numero primo proximo de " + str(n) + " é: " + str(atras) + "\n" + "com menos que 10 elevado a" + str(confiabilidade) + "%\n" + " de chance de erro"
                        break
                    frente += 2
                    atras -= 2

            elif int(self.numero.get()) == 2:
                self.lbresultado["text"] = "3"
                return
            elif int(self.numero.get()) == 3:
                self.lbresultado["text"] = "2"
            else:
                self.lbresultado["text"] = "Digite um numero maior que 1"
                return

        else:
            self.lbresultado["text"] = "Digite numeros inteiros positivos"

    def createWidgets(self):
        self.style.map("C.TButton",
                       foreground=[('pressed', 'red'), ('active', 'blue')],
                       background=[('pressed', '!disabled', 'black'), ('active', 'white')]
                       )
        self.lbNumero.place(x=40, y=60)
        self.numero.place(x=100, y=60)

        self.lbTentativas.place(x=40, y=80)
        self.tentativas.place(x=100, y=80)

        x = 100
        y = 110
        self.btMillerRabin.place(x=x, y=y)
        self.btMillerRabin["command"] = self.teste_de_MillerRabin

        self.btBuscar.place(x=x, y=y + 30)
        self.btBuscar["command"] = self.encontrar_primo

        self.metodos.place(x=100, y=y + 70)

        self.lbresultado.place(x=10, y=y + 90)

        self.QUIT.place(x=20, y=250)


root = tk.Tk()
root.title("Teste de primalidade")
root.geometry("300x300+500+200")
app = Application(master=root)
app.mainloop()
