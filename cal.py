from tkinter import *
import math

# Cores
cor1 = "#3b3b3b"  # Preto
cor2 = "#feffff"  # Branco
cor3 = "#38576b"  # Azul (display)
cor4 = "#7d7c7c"  # Cinza (botões normais)
cor5 = "#FFAB40"  # Laranja (operadores / =)
cor6 = "#2a6496"  # Azul escuro (botões científicos)
cor7 = "#5a5a5a"  # Cinza médio

janela = Tk()
janela.title("Calculadora Científica")
janela.geometry("320x500")
janela.config(bg=cor1)
janela.resizable(False, False)

# Variáveis de estado, aqui serão armazenadas as informações sobre o que esta acontecendo no programa.
expressao    = ""
modo_graus   = True
segundo_modo = False

# Display
frame_tela = Frame(janela, width=320, height=80, bg=cor3)
frame_tela.grid(row=0, column=0, sticky="ew")
frame_tela.grid_propagate(False)

display_expr = StringVar(value="")
display_res  = StringVar(value="0")

lbl_expr = Label(frame_tela, textvariable=display_expr,
                 font=("Courier", 11), bg=cor3, fg="#aac8d8", anchor="e")
lbl_expr.place(x=0, y=6, width=314, height=18)

lbl_res = Label(frame_tela, textvariable=display_res,
                font=("Courier", 28, "bold"), bg=cor3, fg=cor2, anchor="e")
lbl_res.place(x=0, y=28, width=314, height=46)

def ajustar_fonte(texto):
    n = len(str(texto))
    if   n <= 9:  tam = 28
    elif n <= 13: tam = 22
    elif n <= 18: tam = 16
    elif n <= 24: tam = 12
    else:         tam = 9
    lbl_res.config(font=("Courier", tam, "bold"))

MAX_CHARS = 32   # limite de caracteres

# Lógica
def adicionar(simbolo):
    global expressao
    if len(expressao) >= MAX_CHARS:
        return                          # bloqueia após 32 chars
    expressao += str(simbolo)
    display_expr.set(expressao)
    display_res.set(expressao)          # mostra tudo, sem cortar
    ajustar_fonte(expressao)

def limpar():
    global expressao
    expressao = ""
    display_expr.set("")
    display_res.set("0")
    ajustar_fonte("0")

def apagar():
    global expressao
    expressao = expressao[:-1]
    display_expr.set(expressao)
    val = expressao if expressao else "0"
    display_res.set(val)
    ajustar_fonte(val)

def calcular():
    global expressao
    try:
        resultado = eval(expressao)
        if isinstance(resultado, float) and resultado.is_integer():
            resultado = int(resultado)
        s = str(resultado)
        display_expr.set(expressao + " =")
        display_res.set(s)
        ajustar_fonte(s)
        expressao = s
    except ZeroDivisionError:
        display_res.set("Div/0!")
        ajustar_fonte("Div/0!")
        expressao = ""
    except Exception:
        display_res.set("Erro")
        ajustar_fonte("Erro")
        expressao = ""

def _angulo(x):
    return math.radians(x) if modo_graus else x

def _de_rad(x):
    return math.degrees(x) if modo_graus else x

def aplicar_func(func_nome):
    global expressao
    try:
        val = float(eval(expressao)) if expressao else 0.0
        if   func_nome == "sin":  r = math.sin(_angulo(val))
        elif func_nome == "cos":  r = math.cos(_angulo(val))
        elif func_nome == "tan":  r = math.tan(_angulo(val))
        elif func_nome == "asin": r = _de_rad(math.asin(val))
        elif func_nome == "acos": r = _de_rad(math.acos(val))
        elif func_nome == "atan": r = _de_rad(math.atan(val))
        elif func_nome == "log":  r = math.log10(val)
        elif func_nome == "ln":   r = math.log(val)
        elif func_nome == "sqrt": r = math.sqrt(val)
        elif func_nome == "x2":   r = val ** 2
        elif func_nome == "x3":   r = val ** 3
        elif func_nome == "inv":  r = 1 / val
        elif func_nome == "exp":  r = math.exp(val)
        elif func_nome == "abs":  r = abs(val)
        elif func_nome == "fat":  r = math.factorial(int(val))
        elif func_nome == "10x":  r = 10 ** val
        else: return
        if isinstance(r, float) and r.is_integer():
            r = int(r)
        s = str(round(float(r), 10))
        if '.' in s:
            s = s.rstrip('0').rstrip('.')
        display_expr.set(f"{func_nome}({expressao}) =")
        display_res.set(s)
        ajustar_fonte(s)
        expressao = s
    except Exception:
        display_res.set("Erro")
        ajustar_fonte("Erro")
        expressao = ""

def inserir_constante(c):
    global expressao
    if len(expressao) >= MAX_CHARS:
        return
    expressao += c
    display_expr.set(expressao)
    display_res.set(expressao)
    ajustar_fonte(expressao)

def toggle_graus():
    global modo_graus
    modo_graus = not modo_graus
    btn_deg.config(text="DEG" if modo_graus else "RAD",
                   bg=cor6 if modo_graus else "#c0392b")

def toggle_2nd():
    global segundo_modo
    segundo_modo = not segundo_modo
    if segundo_modo:
        btn_sin.config(text="asin")
        btn_cos.config(text="acos")
        btn_tan.config(text="atan")
        btn_2nd.config(bg=cor5)        # laranja = ativo
    else:
        btn_sin.config(text="sin")
        btn_cos.config(text="cos")
        btn_tan.config(text="tan")
        btn_2nd.config(bg=cor6)        # azul = inativo

def trig():     return "asin" if segundo_modo else "sin"
def trig_cos(): return "acos" if segundo_modo else "cos"
def trig_tan(): return "atan" if segundo_modo else "tan"

    # TECLADO NUMÉRICO
def tecla(event):
    k    = event.keysym
    char = event.char
    # Dígitos e operadores do teclado principal
    if char in "0123456789":    adicionar(char)
    elif char == ".":           adicionar(".")
    elif char == "+":           adicionar("+")
    elif char == "-":           adicionar("-")
    elif char == "*":           adicionar("*")
    elif char == "/":           adicionar("/")
    elif char == "%":           adicionar("%")
    elif char == "(":           adicionar("(")
    elif char == ")":           adicionar(")")
    # Teclado numérico (KP = KeyPad)
    elif k == "KP_0":           adicionar("0")
    elif k == "KP_1":           adicionar("1")
    elif k == "KP_2":           adicionar("2")
    elif k == "KP_3":           adicionar("3")
    elif k == "KP_4":           adicionar("4")
    elif k == "KP_5":           adicionar("5")
    elif k == "KP_6":           adicionar("6")
    elif k == "KP_7":           adicionar("7")
    elif k == "KP_8":           adicionar("8")
    elif k == "KP_9":           adicionar("9")
    elif k == "KP_Decimal":     adicionar(".")
    elif k == "KP_Add":         adicionar("+")
    elif k == "KP_Subtract":    adicionar("-")
    elif k == "KP_Multiply":    adicionar("*")
    elif k == "KP_Divide":      adicionar("/")
    elif k in ("Return", "KP_Enter"):  calcular()
    elif k == "BackSpace":      apagar()
    elif k == "Escape":         limpar()

janela.bind("<Key>", tecla)

# Construtor de botões 
def btn(parent, texto, linha, col, cmd,
        cspan=1, rspan=1, bg=cor4, fg=cor2):
    b = Button(parent, text=texto, bg=bg, fg=fg,
               font=("Ivy", 11, "bold"),
               relief=FLAT, overrelief=RIDGE,
               command=cmd, cursor="hand2",
               bd=1, highlightthickness=0)
    b.grid(row=linha, column=col, columnspan=cspan, rowspan=rspan,
           padx=1, pady=1, sticky="nsew")
    return b

# Frame dos botões 
frame_corpo = Frame(janela, bg=cor1, width=320, height=420)
frame_corpo.grid(row=1, column=0, sticky="nsew")
frame_corpo.grid_propagate(False)

for i in range(7):
    frame_corpo.rowconfigure(i, weight=1)
for j in range(5):
    frame_corpo.columnconfigure(j, weight=1)

# Linha 0: 2nd | DEG | π | C | ⌫ 
btn_2nd = btn(frame_corpo, "2nd", 0, 0, toggle_2nd,                     bg=cor6)
btn_deg = btn(frame_corpo, "DEG", 0, 1, toggle_graus,                   bg=cor6)
btn(frame_corpo, "π",   0, 2, lambda: inserir_constante(str(math.pi)),  bg=cor6)
btn(frame_corpo, "C",   0, 3, limpar,                                   bg=cor4)
btn(frame_corpo, "⌫",   0, 4, apagar,                                  bg="#c0392b")

# Linha 1: x² | 1/x | |x| | exp | mod 
btn(frame_corpo, "x²",  1, 0, lambda: aplicar_func("x2"),   bg=cor6)
btn(frame_corpo, "1/x", 1, 1, lambda: aplicar_func("inv"),  bg=cor6)
btn(frame_corpo, "|x|", 1, 2, lambda: aplicar_func("abs"),  bg=cor6)
btn(frame_corpo, "exp", 1, 3, lambda: aplicar_func("exp"),  bg=cor6)
btn(frame_corpo, "mod", 1, 4, lambda: adicionar("%"),       bg=cor6)

# Linha 2: sin | cos | tan | n! | ÷ 
btn_sin = btn(frame_corpo, "sin", 2, 0, lambda: aplicar_func(trig()),     bg=cor6)
btn_cos = btn(frame_corpo, "cos", 2, 1, lambda: aplicar_func(trig_cos()), bg=cor6)
btn_tan = btn(frame_corpo, "tan", 2, 2, lambda: aplicar_func(trig_tan()), bg=cor6)
btn(frame_corpo, "n!",  2, 3, lambda: aplicar_func("fat"),                bg=cor6)
btn(frame_corpo, "÷",   2, 4, lambda: adicionar("/"),                     bg=cor5)

# Linha 3: xʸ | 7 | 8 | 9 | × 
btn(frame_corpo, "xʸ",  3, 0, lambda: adicionar("**"),      bg=cor6)
btn(frame_corpo, "7",   3, 1, lambda: adicionar("7"),       bg=cor4)
btn(frame_corpo, "8",   3, 2, lambda: adicionar("8"),       bg=cor4)
btn(frame_corpo, "9",   3, 3, lambda: adicionar("9"),       bg=cor4)
btn(frame_corpo, "×",   3, 4, lambda: adicionar("*"),       bg=cor5)

# Linha 4: 10ˣ | 4 | 5 | 6 | − 
btn(frame_corpo, "10ˣ", 4, 0, lambda: aplicar_func("10x"),  bg=cor6)
btn(frame_corpo, "4",   4, 1, lambda: adicionar("4"),       bg=cor4)
btn(frame_corpo, "5",   4, 2, lambda: adicionar("5"),       bg=cor4)
btn(frame_corpo, "6",   4, 3, lambda: adicionar("6"),       bg=cor4)
btn(frame_corpo, "−",   4, 4, lambda: adicionar("-"),       bg=cor5)

# Linha 5: log | 1 | 2 | 3 | + 
btn(frame_corpo, "log", 5, 0, lambda: aplicar_func("log"),   bg=cor6)
btn(frame_corpo, "1",   5, 1, lambda: adicionar("1"),        bg=cor4)
btn(frame_corpo, "2",   5, 2, lambda: adicionar("2"),        bg=cor4)
btn(frame_corpo, "3",   5, 3, lambda: adicionar("3"),        bg=cor4)
btn(frame_corpo, "+",   5, 4, lambda: adicionar("+"),        bg=cor5)

# Linha 6: ln | ± | 0 | . | = 
btn(frame_corpo, "ln",  6, 0, lambda: aplicar_func("ln"),     bg=cor6)
btn(frame_corpo, "±",   6, 1, lambda: adicionar("*-1"),       bg=cor4)
btn(frame_corpo, "0",   6, 2, lambda: adicionar("0"),         bg=cor4)
btn(frame_corpo, ".",   6, 3, lambda: adicionar("."),         bg=cor4)
btn(frame_corpo, "=",   6, 4, calcular,                       bg=cor5)

janela.mainloop()