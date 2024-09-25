import re

inputFromUser=input(">> ")

# Função que executa as operações;
# Recebe o nome da operação
# Devolve uma lista com [ 1 caso o resultado seja um valor ou 0 caso o resultado seja uma lista , resultado da operação ]
def func(nome,lista):
    if nome == 'sum':
        return [1,sum(lista)]
    elif nome == 'soma':
        return [1,sum(lista)]
    elif nome == 'media':
        return [1,sum(lista)/len(lista)]
    elif nome == 'ord':
        return[0,lista.sort()]
    elif nome == 'min':
        return [1,min(lista)]
    elif nome == 'max':
        return [1,max(lista)]
    elif nome == 'moda':
        ocorr = {}
        for m in lista:
            ocorr[m] = lista.count(m)
        return [1,max(ocorr)]
    elif nome == "mediana":
        lista.sort()
        if len(lista)%2 == 1:
            return [1,lista[int(len(lista)/2)]]
        else:
            return [1,(lista[int(len(lista)/2)]+lista[(int(len(lista)/2))-1])/2]

# Função que passa lista de valores e a função para string
# Recebe o nome do da lista de valores, a operação a executar e a lista de valores (ex: escreve(Notas,sum,[12,13,14])
# Devolve o texto formatado
def escreve(m,funcao,valores):
    if not funcao:
        return "\t\t\"" + m.group(1) + "\": " + "[" + ','.join(map(str,valores)) + "]\n"
    else:
        string = "\t\t\"" + m.group(1) + "_" + funcao.group(1) + "\": "
        resposta = func(funcao.group(1), valores)
        if resposta[0] == 1:
            string += str(resposta[1]) + "\n"
        else:
            string += "[" + ','.join(map(str, valores)) + "]\n"
        return string


if inputFromUser!="":

   #Abrir o ficheiro quando o input é do tipo:<nome_do_ficheiro> <expressão regular> ou do tipo <nome_do_ficheiro> <nome_do_campo> <valor_que_está_nesse_campo>
   if re.search(r'\s', inputFromUser):
    ficheiro=re.search(r'([^\s]*)\s',inputFromUser)
    f = open(str(ficheiro.group(1))+".csv", "r")

   #Abrir o ficheiro quando o input é do tipo:<nome_do_ficheiro>
   else:
    f = open(inputFromUser+".csv", "r")

   lista = {}
   i = 0
   verifica=[[]]
   for linha in f:

     #Substituir vírgulas dentro de chavetas por pontos de exclamação (ex: {3,5} -> {3!5})
     linha2 = re.sub(r'({[\d]+),([\d]+})', r'\1!\2', linha)

     #Fazer split dos dados do ficheiro .csv usando as vírgulas
     if i==0:
        lista[i] = (re.split(r',', linha2))
        i += 1
     else:
     #Quando um input é do tipo <nome_do_ficheiro> <expressão regular>
      if len(re.findall(r'\s',inputFromUser))==1:
       k = re.search(r'[\s]+([^\s]*)', inputFromUser)
       if re.search(str(k.group(1)),linha2):
        lista[i] = (re.split(r',', linha2))
        i += 1
      #Quando um input é do tipo <nome_do_ficheiro> <nome_do_campo> <valor_que_está_nesse_campo>
      elif len(re.findall(r'\s',inputFromUser))==2:
       ok = re.search(r'[\s]+([^\s]*)[\s]([^\s]*)', inputFromUser)
       if ok.group(2) and str(ok.group(1)) in lista[0] and re.search("(?<=[,])"+str(ok.group(2))+"(?=[,])",linha2):
              verifica[0] = (re.split(r',', linha2))
              if lista[0].index(str(ok.group(1))) == verifica[0].index(str(ok.group(2))):
                  lista[i] = (re.split(r',', linha2))
                  i += 1
      #Quando o input é do tipo:<nome_do_ficheiro>
      else:
         lista[i] = (re.split(r',', linha2))
         i += 1

   f.close()

   #Criar o ficheiro .json quando o input é do tipo:<nome_do_ficheiro> <expressão regular>
   if re.search(r'\s', inputFromUser):
       f = open(str(ficheiro.group(1)) +".json", "w")

   #Criar o ficheiro quando o input é do tipo:<nome_do_ficheiro>
   else:
       f = open(inputFromUser+".json", "w")

   texto = "[\n"
   #Percorrer os dados guardados
   for j in range(1, i):
      valores = []
      texto += "\t{\n"
      for x in range(len(lista[j]) - 1):
       if re.search(r'([a-zA-Z]+){([\d]+)(![\d]+)?}',lista[0][x]) :

         #A variável m encontra um padrão que nos diz o nome da variável e os números mínimo e máximo de argumentos
         m = re.search(r'([a-zA-Z]+){([\d]+)(![\d]+)?}',lista[0][x])
         funcao = re.search(r'::([a-z]+)', lista[0][x])
         valores.append(int(re.sub(r'([0-9]+)\n',r'\1',lista[j][x])))
         z=x+1
         t=0

         #Se houver número máximo de argumentos
         if(m.group(3)):
          nmax = re.sub(r'!','',m.group(3))
          for t in range(0,int(nmax)):
             if z<len(lista[j]) and lista[j][z]!="\n" and lista[j][z]:
                 l=re.sub(r'([0-9]+)\n',r'\1',lista[j][z])
                 valores.append(int(l))
             z+=1

         #Se não houver número máximo de argumentos
         else:
          for t in range(0, int(m.group(2))):
             if z < len(lista[j]) and lista[j][z] != "\n" and lista[j][z]:
                  l = re.sub(r'([0-9]+)\n', r'\1', lista[j][z])
                  valores.append(int(l))
             z += 1
         texto+=escreve(m,funcao,valores)
       elif lista[0][x] == "": pass
       else:
             texto += "\t\t\"" + lista[0][x] + "\": \"" + lista[j][x] + "\",\n"
      texto += "\t},\n"

   texto += "]\n"
   f.write(texto)