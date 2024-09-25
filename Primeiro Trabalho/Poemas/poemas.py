import re

inputFromUser=input(">> ")

if inputFromUser!="":
    resultado=""
    texto=""
    f = open(inputFromUser + ".txt", "r")
    #passar de ficheiro para uma variavel com o texto
    for linha in f:
        texto+=linha
    Estrofes=len(re.findall("\n\n",texto))+1
    #Todas as palavras
    Palavras=re.findall(r'([a-zA-Zz-ý]+)',texto)  #z-Ý tem no seu intervalo todos os caracteres com acento Á á Ó õ etc exceto o ã q temos de meter
    resultado += "Numero de Palavras: " + str(len(Palavras)) + "\n\n"
    #Palavra que teve mais ocorrências
    palocr={}
    for palavra in Palavras:
        if palavra not in palocr:
            palocr[palavra]=len(re.findall('(?<![a-zA-Zz-ý])'+palavra+'(?![a-zA-Zz-ý])',texto))
    maior=""
    for palavra in palocr:
        if palocr[palavra]==max(list(palocr.values())):
            maior=palavra
    resultado+="Palavra que ocorreu mais: "+maior+" com " +str(palocr[maior])+" ocorrências.\n\n"
    if Estrofes>1:
        #Tipo (Poema
        resultado += "Tipo do texto: Poema\n\n"
        # Numero de estrofes
        resultado += "Numero de Estrofes: " + str(Estrofes)+"\n\n"
        #Tipo de Estrofes
        estrofes = re.split(r'\n\n', texto)
        tiposquadra=["Nada","Monóstico","Dístico","Terceto","Quarteto","Quintilha","Sextilha","Septilha"]
        l=1
        for a in estrofes:
                numero=0
                numero=len(re.split(r'\n',a))
                resultado +=str(l)+"ª estrofe: "+tiposquadra[numero]+"\n\n"
                l+=1
        #Verifica se é um Soneto
        if Estrofes==4 and re.search(r'1[ª :a-z]+Q',resultado) and re.search(r'2[ª :a-z]+Q',resultado) and re.search(r'3[ª :a-z]+T',resultado)and re.search(r'4[ª :a-z]+T',resultado) :
            resultado+="Este Poema é um Soneto.\n\n"
        #Rimas
        linhas = re.split(r'\n', texto)
        rimas = {}
        array = []
        ns = 0
        #Cria um array com com os digitos equivalente a cada rima, para depois inserir no inicio de cada verso
        for i in linhas:
            i+='\n'
            rima = re.search(r'[a-zA-Zz-ý]*([a-zA-Zz-ý]{2})[!,.?;]*\n', i)
            if rima and rima.group(1) not in rimas:
                rimas[rima.group(1)] = ns
                ns += 1
                array.append(rimas[rima.group(1)])
            elif rima:
                array.append(rimas[rima.group(1)])
        x=0
        texto=""
        ultima=[]
        #Guarda a ultima palavra de cada linha, atualiza o array com todas as linhas, colocando o \n no fim de cada linha e o digito correspondente a cada rima.
        #Além disso também reconstroi o poema de forma a que seja possivel imprimi-lo no fim com os padrões das rimas
        for t in range(0,len(linhas)):
          if linhas[t]:
              linhas[t]+= '\n'
              texto += str(array[x]) + "- " + linhas[t]
              linhas[t]= str(array[x]) + "- " + linhas[t]
              x += 1
              ultima.append(re.search(r' ([a-zA-Zz-ý]*)[!,.?;]*\n', linhas[t]).group(1))
          else:
              texto += "\n"
              ultima.append("vazio")
        #Tipos de Rimas
        RimEmp=[]
        RimEnc=[]
        SemRima=[]
        RimAlt=[]
        RimInt=[]
        numlinha=1
        for x in range(0,len(linhas)):
            if linhas[x]:
                linhax=int(re.search(r'([0-9])+\- ', linhas[x]).group(1))
                #Rima Emparelhada
                if x<len(linhas)-1 and linhas[x+1]:
                    linhax1= int(re.search(r'([0-9])+\- ', linhas[x + 1]).group(1))
                    if linhax==linhax1:
                      RimEmp.append(ultima[x]+" (linha "+str(numlinha)+") - "+ultima[x+1]+" (linha "+str(numlinha+1)+")")
                #Rima Encadeadas
                if x<len(linhas)-2 and linhas[x+2] and linhas[x+1]:
                    linhax2= int(re.search(r'([0-9])+\- ', linhas[x + 2]).group(1))
                    if linhax==linhax2:
                      RimEnc.append(ultima[x]+" (linha "+str(numlinha)+") - "+ultima[x+2]+" (linha "+str(numlinha+2)+")")
                #Rima Alternada
                if x<len(linhas)-3 and linhas[x+1] and linhas[x+2] and linhas[x+3]:
                    linhax1= int(re.search(r'([0-9])+\- ', linhas[x + 1]).group(1))
                    linhax2= int(re.search(r'([0-9])+\- ', linhas[x + 2]).group(1))
                    linhax3= int(re.search(r'([0-9])+\- ', linhas[x + 3]).group(1))
                    if linhax==linhax2 and linhax!=linhax1 and linhax1==linhax3 and linhax1!=linhax2 and linhax2!=linhax3:
                      RimAlt.append(ultima[x] + " (linha " + str(numlinha) + ") - " + ultima[x + 2] + " (linha " + str(numlinha + 2)+") / "+ ultima[x+1]+" (linha "+str(numlinha+1)+") - "+ultima[x+3]+" (linha "+str(numlinha+3)+")")
                #Rima Interpolada
                if x<len(linhas)-3 and linhas[x+1] and linhas[x+2] and linhas[x+3]:
                    linhax1= int(re.search(r'([0-9])+\- ', linhas[x + 1]).group(1))
                    linhax2= int(re.search(r'([0-9])+\- ', linhas[x + 2]).group(1))
                    linhax3= int(re.search(r'([0-9])+\- ', linhas[x + 3]).group(1))
                    if linhax==linhax3 and linhax!=linhax1 and linhax1==linhax2 and linhax2!=linhax3:
                      RimInt.append(ultima[x] + " (linha " + str(numlinha) + ") - " + ultima[x + 3] + " (linha " + str(numlinha + 3)+") / "+ ultima[x+1]+" (linha "+str(numlinha+1)+") - "+ultima[x+2]+" (linha "+str(numlinha+2)+")")
                #Sem Rima
                if not re.search(ultima[x],','.join(map(str, RimEmp))) and not re.search(ultima[x],','.join(map(str, RimEnc)))and not re.search(ultima[x],','.join(map(str, RimAlt)))and not re.search(ultima[x],','.join(map(str, RimInt))):
                     SemRima.append(ultima[x]+" (linha "+str(numlinha)+")")
            numlinha+=1

        #Adiciona á mensagem final os tipos de Rima
        resultado+="Tipos de Rimas: \n\nRimas Emparelhadas: "+str(len(RimEmp))+"\n"+'\n'.join(map(str,RimEmp))+"\n\n"
        resultado+="Rimas Encadeadas: "+str(len(RimEnc))+"\n"+'\n'.join(map(str,RimEnc))+"\n\n"
        resultado+="Rimas Alternadas: "+ str(len(RimAlt))+ "\n" + '\n'.join(map(str, RimAlt)) + "\n\n"
        resultado+="Rimas Interpoladas: " + str(len(RimInt)) + "\n" + '\n'.join(map(str, RimInt)) + "\n\n"
        resultado+="Sem Rima: " + str(len(SemRima)) +"\n"+ '\n'.join(map(str, SemRima)) + "\n\n"
    else:
        resultado += "Tipo do texto: Prosa\n"
    f.close()
    f = open("Resultado.txt", "w")
    f.write(texto+"\n\n"+resultado)