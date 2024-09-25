import ply.yacc as yacc
import sys

from lextrabalho import tokens

def p_Programa_Corpo(p):
    "Programa : Corpo"
    parser.codigoprincipal = f'START\n{p[1]}STOP\n'
    p.parser.codigoprincipal=p.parser.codigoprincipal.replace("None", "")

def p_Programa_Glob(p):
    "Programa : Glob"
    parser.codigoprincipal = f'{p[1]}START\nSTOP\n'
    p.parser.codigoprincipal=p.parser.codigoprincipal.replace("None", "")

def p_Programa_Glob_Corpo(p):
    "Programa : Glob Corpo"
    parser.codigoprincipal = f'{p[1]}START\n{p[2]}STOP\n'
    p.parser.codigoprincipal = p.parser.codigoprincipal.replace("None", "")

def p_Glob(p):
    "Glob    : Decl"
    p[0] = f'{p[1]}'

def p_Glob_Recursiva(p):
    "Glob    : Glob Decl"
    p[0] = f'{p[1]}{p[2]}'

def p_Decl_Int(p): # inteiro x
    "Decl     : INT NOME"
    if p[2] not in p.parser.registos:
        p.parser.registos.update({p[2] : p.parser.gp})
        p[0] = f'PUSHI 0\n'
        p.parser.gp += 1
    else:
        print("Erro: Variável já existe.")
        parser.sucess = False

def p_Decl_Int_Atr(p): # inteiro x = 2
    "Decl     : INT NOME ATR NUMERO"
    if p[2] not in p.parser.registos:
        p.parser.registos.update({p[2] : p.parser.gp})
        p[0] = f'PUSHI {p[4]}\n'
        p.parser.gp += 1
    else:
        print("Erro: Variável já existe.")
        parser.sucess = False

def p_Decl_Nome_Atr(p): #inteiro x = y
    "Decl : INT NOME ATR NOME"
    if p[2] not in p.parser.registos:
     if p[4] in p.parser.registos:
            p.parser.registos.update({p[2]: p.parser.gp})
            p[0] = f'PUSHG {p.parser.registos.get(p[4])}\n'
            p.parser.gp += 1
     else:
        print(f"Erro: A Variável {p[4]}  não está definida.")
        parser.sucess = False
    else:
        print(f"Erro: A Variável {p[2]} já existe.")
        parser.sucess = False

def p_Decl_Func_VAR(p): # funcao () ( define funcao ... return x )
    "Decl : Fundecl DEFINE NOME Programa RETURN NOME ')'"
    if p[3] not in p.parser.codigoauxiliar:
        if p[6] in p.parser.registos:
          codigov = p.parser.codigoprincipal.replace("STOP\n", "")
          codigov = codigov + f'PUSHG {p.parser.registos.get(p[6])}\n'+"RETURN\n"
          p.parser.codigoauxiliar.update({p[3] :codigov})
          p.parser.registos.update({p[1] : p.parser.gp})
        else:
          print(f"Erro: A Variável {p[6]} não está definida.")
          parser.sucess = False
    else:
        print("Erro: A função já existe.")
        parser.sucess = False

def p_Decl_Func_Int(p): # funcao () ( define funcao ... return 2 )
    "Decl : Fundecl DEFINE NOME Programa RETURN NUMERO ')'"
    if p[3] not in p.parser.codigoauxiliar:
        codigoi = p.parser.codigoprincipal.replace("STOP\n", "")
        codigoi =codigoi+f'PUSHI {p[6]}\n'+"RETURN\n"
        p.parser.codigoauxiliar.update({p[3] :codigoi})
        p.parser.registos.update({p[1] : p.parser.gp})
    else:
        print("Erro: A função já existe.")
        parser.sucess = False

def p_Decl_Func_Int_vazia(p): # funcao () ( define funcao return 2 )
    "Decl : Fundecl DEFINE NOME RETURN NUMERO ')' "
    if p[3] not in p.parser.codigoauxiliar:
        codigoi =p.parser.codigoprincipal+f'START\nPUSHI {p[5]}\n'+"RETURN\n"
        p.parser.codigoauxiliar.update({p[3] :codigoi})
        p.parser.registos.update({p[1] : p.parser.gp})
    else:
        print("Erro: A função já existe.")
        parser.sucess = False

def p_Fundecl(p):
    "Fundecl : NOME '(' ')' '('"
    p[0]=f'{p[1]}{p[2]}{p[3]}'

def p_Corpo(p):
    "Corpo    : Ope"
    p[0] = p[1]

def p_Corpo_Recursiva(p):
    "Corpo    : Corpo Ope"
    p[0] = f'{p[1]}{p[2]}'

def p_Ope_Atrib(p):
    "Ope     : Atrib"
    p[0] = p[1]

def p_Ope_Escrever(p):
    "Ope     : Escrever"
    p[0] = p[1]

def p_Ope_Se(p):
    "Ope     : Se"
    p[0] = p[1]

def p_Ope_Enquanto(p):
    "Ope     : Enquanto"
    p[0] = p[1]

def p_Ope_PRINT(p):
    "Ope : PRINT '(' Frase ')' "
    p[0] = f'PUSHS "{p[3]}"\nWRITES\n'

def p_Frase_nome(p):
    "Frase : NOME"
    p[0] = p[1]

def p_Frase(p):
    "Frase : Frase NOME"
    p[0] = f'{p[1]} {p[2]}'

def p_Se(p):
    "Se       : SE Cond ENTAO Corpo FIM"
    p[0] = f'{p[2]}JZ l{p.parser.labels}\n{p[4]}l{p.parser.labels}: NOP\n'
    p.parser.labels += 1

def p_Se_Senao(p):
    "Se       : SE Cond ENTAO Corpo SENAO Corpo FIM"
    p[0] = f'{p[2]}JZ l{p.parser.labels}\n{p[4]}JUMP l{p.parser.labels}f\nl{p.parser.labels}: NOP\n{p[6]}l{p.parser.labels}f: NOP\n'
    p.parser.labels += 1

def p_Enquanto(p):
    "Enquanto : ENQUANTO Cond FAZ Corpo FIM"
    p[0] = f'l{p.parser.labels}c: NOP\n{p[2]}JZ l{p.parser.labels}f\n{p[4]}JUMP l{p.parser.labels}c\nl{p.parser.labels}f: NOP\n'
    p.parser.labels += 1

def p_Atrib_expr_Int(p):
    "Atrib    : NOME ATR Expr"
    if p[1] in p.parser.registos:
            p[0] = f'{p[3]}STOREG {p.parser.registos.get(p[1])}\n'
    else:
        print("Erro: Variável não definida.")
        parser.sucess = False

def p_Atrib_Ler(p):
    "Atrib    : NOME ATR LER"
    if p[1] in p.parser.registos:
        p[0] = f'READ\nATOI\nSTOREG {p.parser.registos.get(p[1])}\n'
    else:
        print("Erro: Variável  não definida.")
        parser.sucess = False

def p_Escrever(p):
    "Escrever : ESCREVER Expr"
    p[0] = f'{p[2]}WRITEI\nPUSHS "\\n"\nWRITES\n'

def p_Expr_P(p):
    "Expr     : '(' Expr ')'"
    p[0] = p[2]

def p_Expr_Func(p):
    "Expr : NOME '(' ')'"
    nomefunc=p[1]+p[2]+p[3]
    if nomefunc in p.parser.registos:
        p[0] = f'PUSHA {p[1]}\nCALL\n'
    else:
        print("Erro: Função não está definida.")
        parser.sucess = False

def p_Expr_Var(p):
    "Expr     : Var"
    p[0] = p[1]
def p_Expr_NUMERO(p):
    "Expr     : NUMERO"
    p[0] = f'PUSHI {p[1]}\n'

def p_Expr_soma(p):
    "Expr     : '+' '(' Expr VIRG Expr ')' "
    p[0] = f'{p[3]}{p[5]}ADD\n'

def p_Expr_Sub(p):
    "Expr     : '-' '(' Expr VIRG Expr ')'"
    p[0] = f'{p[3]}{p[5]}SUB\n'

def p_Expr_Mult(p):
    "Expr     : '*' '(' Expr VIRG Expr ')'"
    p[0] = f'{p[3]}{p[5]}MUL\n'

def p_Expr_Div(p):
    "Expr     : '/' '(' Expr VIRG Expr ')'"
    p[0] = f'{p[3]}{p[5]}DIV\n'

def p_Expr_Mod(p):
    "Expr     : '%' '(' Expr VIRG Expr ')'"
    p[0] = f'{p[3]}{p[5]}MOD\n'

def p_Expr_Cond(p):
    "Expr     : Cond"
    p[0] = p[1]

def p_Cond_P(p):
    "Cond     : '(' Cond ')'"
    p[0] = p[2]

def p_Cond_Maior(p):
    "Cond     : MAIOR '(' Expr VIRG Expr ')'"
    p[0] = f'{p[3]}{p[5]}SUP\n'

def p_Cond_Menor(p):
    "Cond     : MENOR '(' Expr VIRG Expr ')'"
    p[0] = f'{p[3]}{p[5]}INF\n'

def p_Cond_Maiori(p):
    "Cond     : MAIORI '(' Expr VIRG Expr ')'"
    p[0] = f'{p[3]}{p[5]}SUPEQ\n'

def p_Cond_Menori(p):
    "Cond     : MENORI '(' Expr VIRG Expr ')'"
    p[0] = f'{p[3]}{p[5]}INFEQ\n'

def p_Cond_Igual(p):
    "Cond     : IGUAL '(' Expr VIRG Expr ')'"
    p[0] = f'{p[3]}{p[5]}EQUAL\n'

def p_Cond_Nigual(p):
    "Cond     : NIGUAL '(' Expr VIRG Expr ')'"
    p[0] = f'{p[3]}{p[5]}EQUAL\nNOT\n'

def p_Cond_E(p):
    "Cond     : E '(' Cond VIRG Cond ')'"
    p[0] = f'{p[3]}{p[5]}ADD\nPUSHI 2\nEQUAL\n'

def p_Cond_Ou(p):
    "Cond     : OU '(' Cond VIRG Cond ')'"
    p[0] = f'{p[3]}{p[5]}ADD\nPUSHI 1\nSUPEQ\n'

def p_Cond_Neg(p):
    "Cond     : NEG '(' Cond ')'"
    p[0] = f'{p[3]}NOT\n'

def p_Var_Int(p):
    "Var      : NOME"
    if p[1] in p.parser.registos:
            p[0] = f'PUSHG {p.parser.registos.get(p[1])}\n'
    else:
        print("Erro: Variável não definida.")
        parser.sucess = False

#Erro
def p_error(p):
    print('Syntax error: ', p)
    parser.sucess = False



#Inicio do Parser
parser = yacc.yacc()

parser.sucess = True
parser.registos = {}
parser.labels = 0
parser.gp = 0
parser.codigoprincipal = ""
parser.codigoauxiliar ={}



if len(sys.argv) > 1:
    with open(sys.argv[1],'r') as file:
        input = file.read()
        parser.parse(input)
        if parser.sucess:
            if len(sys.argv) > 2:
                with open(sys.argv[2], 'w') as output:
                    for t in parser.codigoauxiliar:
                        parser.codigoprincipal=parser.codigoprincipal+"\n"+t+":\n"+parser.codigoauxiliar.get(t)
                    output.write(parser.codigoprincipal)
                    print(f"\nO ficheiro {sys.argv[1]} foi compilado com sucesso.\n\nO output ficou guardado em {sys.argv[2]}.\n")
            else:
                for t in parser.codigoauxiliar:
                    parser.codigoprincipal = parser.codigoprincipal +"\n"+ t + ":\n" + parser.codigoauxiliar.get(t)
                print(parser.codigoprincipal)
        else:
            print("\nErro ao compilar.\n")

