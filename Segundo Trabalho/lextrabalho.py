import ply.lex as lex
import sys

tokens = (
    'NOME',
    'INT',
    'MAIOR',
    'MENOR',
    'IGUAL',
    'MAIORI',
    'MENORI',
    'NIGUAL',
    'NEG',
    'E',
    'OU',
    'ATR',
    'LER',
    'ESCREVER',
    'SE',
    'ENTAO',
    'SENAO',
    'ENQUANTO',
    'FAZ',
    'FIM',
    'VIRG',
    'DEFINE',
    'RETURN',
    'NUMERO',
    'PRINT'
)

t_VIRG = r','
literals = ['(', ')','+','-','*','/','%']

def t_DEFINE(t):
    r'(?i:define)'
    return t

def t_RETURN(t):
    r'(?i:return)'
    return t

def t_PRINT(t):
    r'(?i:print)'
    return t

def t_NUMERO(t):
    r'\d+'
    return t

def t_INT(t):
    r'(?i:inteiro)'
    return t

def t_LER (t):
    r'<<'
    return t

def t_ESCREVER (t):
    r'>>'
    return t

def t_MAIORI(t):
    r'>='
    return t

def t_MAIOR(t):
    r'\>'
    return t

def t_MENORI(t):
    r'\<='
    return t

def t_MENOR(t):
    r'\<'
    return t

def t_IGUAL(t):
    r'=='
    return t

def t_NIGUAL(t):
    r'~='
    return t

def t_NEG (t):
    r'~'
    return t

def t_OU (t):
    r'\|\|'
    return t

def t_ATR (t):
    r'='
    return t

def t_ENTAO(t):
    r'(?i:then)'
    return t

def t_SENAO(t):
    r'(?i:else)'
    return t

def t_SE (t):
    r'(?i:if)'
    return t

def t_ENQUANTO(t):
    r'(?i:while)'
    return t

def t_FAZ(t):
    r'(?i:do)'
    return t

def t_FIM(t):
    r'(?i:end)'
    return t

def t_E (t):
    r'&&'
    return t

def t_NOME(t):
    r'[a-z]\w*'
    return t

t_ignore = ' \r\t\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

