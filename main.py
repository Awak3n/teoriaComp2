import random as rng
import copy
import texttable

#Pega o número de NT desejados e o converte em 'n' NT
def getNumber(msg):
    try:
        while (True):
            nr_nao_terminal = int(input(msg))
            if nr_nao_terminal >= 1 and nr_nao_terminal <= 26:
                break
    except:
        nr_nao_terminal = getNumber(msg)
    return  nr_nao_terminal

def checkGramatica():
    #retorna o tipo de gramática (0 para GI,1 para GSC,2 para GLC,3 para GR)
    #irá verificar se as produções seguem as regras dos tipos de gramática da hierarquia de Chomsky
    type3 = True
    type2 = True
    type1 = True
    for producao in producoes:
        #caso possua mais de um símbolo de entrada ou o mesmo seja um T, não pode ser GLC ou GR
        if (len(producao.entrada) > 1 or producao.entrada[0].tipo == 0):
            type3 = False
            type2 = False
        #caso o tamanho do lado esquerdo seja maior que o lado direito, não pode ser GSC
        if (len(producao.entrada) > len(producao.saida)):
            type1 = False
        #caso não possua somente um NT ou um NT e um T de produção, não pode ser GR
        if ((len(producao.saida) == 1 and producao.saida[0].tipo == 1) or len(producao.saida) >= 2):
            if (producao.saida[0].tipo != 0 or producao.saida[1].tipo != 1):
                type3 = False
        #caso possua símbolo vazio, não pode ser GSC ou GLC
        for simbolo in producao.saida:
            if simbolo.valor == '&':
                type2 = False
                type1 = False
    if type3:
        return [3,"Regular"]
    elif type2:
        return [2,"Livre de Contexto"]
    elif type1:
        return [1,"Sensível ao Contexto"]
    else:
        return [0,"Irrestrita"]

def main():
    global nao_terminais, simbolo_inicial, terminais, producoes
    ################################
    # 1. Entrada de gramática          
    ################################

    print('Construindo a gramática:')

    #Não-terminais
    #Gera os não-terminais automáticamente
    nr_nao_terminal = getNumber('Quantos simbolos não-terminais você deseja? (De 1 a 26)\n')
    print('Seus simbolos não-terminais são:')
    string_nao_terminal = ''
    for x in range(nr_nao_terminal):
        nao_terminais.append(Simbolo(nao_terminais_default[x]))
        if x == nr_nao_terminal -1:
            string_nao_terminal += "'" + nao_terminais_default[x] + "'"
        else:
            string_nao_terminal += "'" + nao_terminais_default[x] + "', "
    print(string_nao_terminal)

    #Terminais
    # Gera os terminais automáticamente
    nr_terminal = getNumber('Quantos simbolos terminais você deseja?\n')
    resposta = input("A gramática aceita o símbolo vazio |&|? (S/N)\n")
    resposta = resposta.strip().lower()
    print('Seus simbolos terminais são:')
    string_terminal = ''
    for x in range(nr_terminal):
        terminais.append(Simbolo(terminais_default[x]))
        if x == nr_terminal -1:
            if resposta == "sim" or resposta == "yes" or resposta == "y" or resposta == "s":
                string_terminal += "'" + terminais_default[x] + "', "
                terminais.append(Simbolo('&'))
                string_terminal += "'&'"
            else:
                string_terminal += "'" + terminais_default[x] + "'"
        else:
            string_terminal += "'" + terminais_default[x] + "', "
    print(string_terminal)

    inicializaSLR()

    for terminal in terminais:
        terminais_string_list.append(terminal.valor)
    for nao_terminal in nao_terminais:
        nao_terminais_string_list.append(nao_terminal.valor)

    #Simbolo
    #Pergunta e valida o simbolo inicial
    if len(nao_terminais) == 1:
        print("Seu simbolo inicial será 'A'\n")
        simbolo_inicial = Simbolo('A')
    else:
        while(True):
            s = input('Qual será o símbolo inicial? Escolha entre: %s.\n'%string_nao_terminal)
            s = s.strip().replace("'","").upper()
            if s in string_nao_terminal:
                simbolo_inicial = Simbolo(s)
                break
            else:
                print("O simbolo inicial precisa estar entre os não-terminais determinados")

    #Produções
    #Input e validação inicial das produções
    print("\nAgora as produções: (MÁXIMO 10)")
    contador = 1
    p_left = ''
    p_right = ''
    while len(producoes) < 11:
        sintaxe_error = True
        #Criando a produção do lado esquerdo
        while sintaxe_error:
            if contador > 1:
                p_left = input("Produção %i - Lado esquerdo (0 para parar)\n" % contador)
            else:
                p_left = input("Produção %i - Lado esquerdo\n" % contador)
            if p_left == "0":
                break
            p_left = p_left.replace(' ','')
            sintaxe_error = False
            um_nao_terminal = False
            for letra in p_left:
                #verifica se os simbolos escolhidos abrangem o alfabeto
                if letra not in nao_terminais_default[:nr_nao_terminal]:
                    if letra not in terminais_default[:nr_terminal] and letra != '&': 
                        sintaxe_error = True
                #É preciso verificar se há, pelo menos, um não terminal no lado esquerdo
                else: 
                    um_nao_terminal = True
            if sintaxe_error is True or um_nao_terminal is False:
                sintaxe_error = True
                print("Erro de Sintaxe\n")
                print("Não esqueça que é preciso que haja pelo menos um não-terminal do lado esquerdo\n"
                      "E que os simbolos precisam estar entre %s, %s\n" % (string_nao_terminal,string_terminal))
        if p_left == "0":
            break
        sintaxe_error = True
        # Criando a produção do lado direito
        while sintaxe_error:
            p_right = input("Produção %i - Lado direito\n" % contador)
            p_right = p_right.replace(' ','')
            sintaxe_error = False
            if p_right[0] == '|':
                p_right = p_right[1:]
            if p_right[-1] == '|':
                p_right = p_right[:-1]
            for letra in p_right:
                if letra != '|':
                    if letra not in nao_terminais_default[:nr_nao_terminal]:
                        #verifica se o lado direito abrange o alfabeto
                        if letra not in string_terminal.replace("'",""): 
                            sintaxe_error = True
            if sintaxe_error is True:
                print("Erro de Sintaxe")
                print("Não esqueça que os simbolos precisam estar entre\n%s e %s" % (string_nao_terminal,string_terminal))
        simbolos_entrada = []
        simbolos_saida = []
        for letra in p_left:
            simbolos_entrada.append(Simbolo(letra))
        p_right += '|'
        #Verifica se o símbolo vazio está presente no lado direito
        for letra in p_right:
            if letra == '|':
                if len(simbolos_saida) > 1:
                    for simbolo in simbolos_saida:
                        #caso esteja, remove todos os outros T e NT que a acompanham
                        if simbolo.valor == '&':
                            print("Aviso:")
                            print("A sentença vazia somente pode ser encontrada sozinha no lado direito, demais simbolos foram ignorados\n")
                            simbolos_saida = [Simbolo('&')]
                producoes.append(Producao(simbolos_entrada, simbolos_saida))
                simbolos_saida = []
            else:
                simbolos_saida.append(Simbolo(letra))
        p_right = p_right[:-1]
        contador += 1

    ################################
    # 2. Exibir gramática          
    ################################

    vetor_producoes_esquerdo = []
    vetor_producoes_direito = []
    string_producoes = ""
    for producao in producoes:
        vetor_producoes_direito.append(producao.getValorDireito())
        vetor_producoes_esquerdo.append(producao.getValorEsquerdo())
    for x in range(len(vetor_producoes_esquerdo)):
        for y in range(x):
            if vetor_producoes_esquerdo[x] == vetor_producoes_esquerdo[y] and vetor_producoes_esquerdo[x] != "":
                vetor_producoes_direito[y] += "|" + vetor_producoes_direito[x]
                vetor_producoes_esquerdo[x] = ""
    for x in range(len(vetor_producoes_esquerdo)):
        if vetor_producoes_esquerdo[x] != "":
            string_producoes += vetor_producoes_esquerdo[x] +" => " + vetor_producoes_direito[x] + ", "
    string_producoes = string_producoes[:-2]

    string_nao_terminal = string_nao_terminal.replace("'","")
    string_terminal = string_terminal.replace("'","")
    print("\nGramática resultante:")
    print("({%s},{%s},{%s},%s)\n" % (string_nao_terminal,string_terminal,string_producoes,simbolo_inicial.valor))

    ################################
    # 3. Verificação da gramática          
    ################################
    # Passo 1: Ver se as produções abrangem todo o alfabeto
    # Passo 2: Evitar loopings obvios (quando não há nem sequer uma produção com apenas terminais)
    for simbolo_terminal in terminais:
        abrange_alfabeto = False
        if simbolo_terminal.valor == '&':
            abrange_alfabeto = True
        else:
            for producao in producoes:
                for simbolo_saida in producao.saida:
                    if simbolo_terminal.valor == simbolo_saida.valor:
                        abrange_alfabeto = True
        if abrange_alfabeto is False:
            print("Erro Estrutural")
            print("Cada simbolo terminal precisa aparecer ao menos uma vez, exceto o |&| se houver\n")
            break
    for simbolo_nao_terminal in nao_terminais:
        abrange_alfabeto = False
        contador_p1 = 0
        contador_p2 = 0
        is_a_looping = True
        # se ele é o simbolo inicial, ele automaticamente abrange o alfabeto
        if simbolo_nao_terminal.valor == simbolo_inicial.valor: 
            abrange_alfabeto = True
        for producao in producoes:
            only_terminais = True
            for simbolo_saida in producao.saida:
                # verifica se há apenas terminais no lado direito dessa produção
                if only_terminais is False or simbolo_saida.tipo == 1: 
                    only_terminais = False
                # se achou uma produção do lado direito
                if simbolo_nao_terminal.valor == simbolo_saida.valor: 
                    # procura o simbolo em outra produção do lado esquerdo em outra produção
                    for producao2 in producoes: 
                        for simbolo_entrada in producao2.saida:
                            if contador_p1 != contador_p2 and simbolo_nao_terminal.valor == simbolo_entrada.valor:
                                abrange_alfabeto = True
                            contador_p2 += 1
            contador_p1 += 1
        if only_terminais is True:
            is_a_looping = False
        if abrange_alfabeto is False:
            print("Erro Estrutural")
            print("Cada simbolo nao-terminal precisa aparecer ao menos uma vez\n")
        break

    ################################
    # 4. Identificação da Gramática
    ################################

    tipo_gramatica = checkGramatica()
    print("E é uma Gramática %s.\n" % tipo_gramatica[1])

    ################################
    # 5. Geração de Sentenças
    ################################
    if is_a_looping:
        print("Há problemas na gramática, corrija-os para que saidas possam ser geradas")
    # vetor com os valores das saidas
    vetor_resultante = [] 
    string = simbolo_inicial.valor
    # etapas pelas quais o simbolo inicial passou
    etapas = [string] 
    contador_producoes = 0
    contador_tentativas = 0
    #enquanto não tiver as 3 saidas ou contador de tentativas não passou das 25k...
    while len(vetor_resultante) != 3 and contador_tentativas < 25000: 
        possui_nao_terminal = True
        # verifica se string está com somente não-terminais
        for letra in string: 
            if letra not in nao_terminais_default:
                possui_nao_terminal = False
            else:
                possui_nao_terminal = True
                break
        if possui_nao_terminal is False or string == "":
            # se possui apenas terminais e ainda não encontrou um resultado igual...
            if string not in vetor_resultante and string != "": 
                # salva resultado
                vetor_resultante.append(string)
                etapas.append(simbolo_inicial.valor)
                string = simbolo_inicial.valor
            else:
                etapas[len(vetor_resultante)] = simbolo_inicial.valor
                string = simbolo_inicial.valor
            contador_producoes = 0
        # enquanto ainda numero de produções não passou de 50 e possui não-terminais...
        while possui_nao_terminal is True and contador_producoes < 50: 
            possiveis_producoes = []
            for producao in producoes:
                if producao.getValorEsquerdo() in string:
                    possiveis_producoes.append(producao)
            if len(possiveis_producoes) != 0:
                if len(possiveis_producoes) == 1:
                    if possiveis_producoes[0].getValorDireito() == "&":
                        string = string.replace(possiveis_producoes[0].getValorEsquerdo(),"", 1)
                        etapas[len(vetor_resultante)] += " -> " + string
                    else:
                        string = string.replace(possiveis_producoes[0].getValorEsquerdo(),possiveis_producoes[0].getValorDireito(), 1)
                        etapas[len(vetor_resultante)] += " -> " + string
                else:
                    nr_producao = rng.randint(0,len(possiveis_producoes)-1)
                    if possiveis_producoes[nr_producao].getValorDireito() == "&":
                        string = string.replace(possiveis_producoes[nr_producao].getValorEsquerdo(),"", 1)
                        etapas[len(vetor_resultante)] += " -> " + string
                    else:
                        string = string.replace(possiveis_producoes[nr_producao].getValorEsquerdo(), possiveis_producoes[nr_producao].getValorDireito(), 1)
                        etapas[len(vetor_resultante)] += " -> " + string
            contador_producoes += 1
        contador_tentativas += 1
    contador = 0
    print("Resultados possíveis:")
    for vetor in vetor_resultante:
        contador += 1
        print("Saida %i: %s" % (contador,vetor))
        print("Etapas: %s" % etapas[contador-1])
    
    ################################
    # 6. Autômato Finito          
    ################################

    if tipo_gramatica[0] == 0:
        print("\nA Gramática %s é interpretada por uma Máquina de Turing." % tipo_gramatica[1])
    elif tipo_gramatica[0] == 1:
        print("\nA Gramática %s é interpretada por um Autômato linearmente limitado." % tipo_gramatica[1])
    elif tipo_gramatica[0] == 2:
        print("\nA Gramática %s é interpretada por um Autômato com pilha." % tipo_gramatica[1])
    else: 
        print("\nA Gramática %s é interpretada por um Autômato Finito: " % tipo_gramatica[1])
        
        # símbolo que indica estado final q0
        string_estados = ''
        string_terminal = string_terminal.replace(", ","")
        string_nao_terminal = string_nao_terminal.replace(", ","")
        
        for i in range(0,len(string_nao_terminal)):
            string_estados += 'q'+str(i+1)+', '
        string_estados = string_estados[:-2]

        # exibe o autômato finito
        print("AF: ({%s} U q0 , {%s}, § , %s, q0)" % (string_estados,string_terminal,'q'+str(string_nao_terminal.index(simbolo_inicial.valor)+1)))
        
        # estados será um dicionário de estados com um dicionário de transições para cada T
        estados = {}
        for char in range(0,len(string_nao_terminal)+1):
            key = 'q'+str(char)
            estados[key] = {}
            for index in range(0,len(string_terminal)):
                estados[key][string_terminal[index]] = []

        #Cria uma lista com todas as transições de estados
        for producao in producoes:
            key = 'q'+str(string_nao_terminal.index(producao.entrada[0].valor)+1)
            transicao = producao.saida[0].valor
            if len(producao.saida) == 2:
                #se possuir um T seguido de um NT, irá para o estado NT
                entry = 'q'+str(string_nao_terminal.index(producao.saida[1].valor)+1)
                estados[key][transicao].append(entry)
            else:
                #se possuir apenas um T, irá para o estado final
                entry = 'q0'
                estados[key][transicao].append(entry)
        
        # Exibindo a tabela de transição
        print("\nOnde § terá a seguinte tabela de transição: ")
        for key,value in estados.items():
            if(key == 'q0'):
                print("Estado final:", key)
                print("    Finaliza as transições.")
            else:
                print("Estado:", key)
                for k,v in value.items():
                    print("    Lendo '%s' irá para => %s" % (k,v))
    
    getAllFirst()
    getAllFollow()
    print("\nFirsts:")
    print(firsts)
    print("\nFollows:")
    print(follows)
    print("\nTabela:") # montar isso bonitinho amanhã se sobrar tempo
    tabelaPretty = texttable.Texttable()
    for (keyPilha,keyEntrada) in tabela:
        tabelaPretty.add_rows([["NT na Pilha", "T na Entrada", "Saída"],[keyPilha,keyEntrada,tabela[(keyPilha,keyEntrada)]]])
    print(tabelaPretty.draw() + '\n')

def transformacaoGLC():
    '''Método contendo todas as transformações, para debbuging'''
    fatoracao()
    recursaoAEsquerda()

def fatoracao():
    '''Realiza a fatoração'''
    global producoes, nao_terminais, simbolo_inicial
    # exemplo 4.1
    # terminais = [Simbolo('a'), Simbolo('b')]  # Lista de Simbolos terminais
    # nao_terminais = [Simbolo('A'), Simbolo('B'), Simbolo('C')]  # Lista de Simbolos nao terminais
    # producoes = [Producao([Simbolo('A')], [Simbolo('a'), Simbolo('A')]), Producao([Simbolo('A')], [Simbolo('a')]),
    #              Producao([Simbolo('B')], [Simbolo('b')]), Producao([Simbolo('C')], [Simbolo('a'), Simbolo('A')]),
    #              Producao([Simbolo('C')], [Simbolo('a'), Simbolo('B')])]  # Produções
    # simbolo_inicial = Simbolo('C')  # Símbolo Inicial da Gramática

    # exemplo 4.2
    # terminais = [Simbolo('a'),Simbolo('b')] # Lista de Simbolos terminais
    # nao_terminais = [Simbolo('A'),Simbolo('B'),Simbolo('C')] # Lista de Simbolos nao terminais
    # producoes = [Producao([Simbolo('A')],[Simbolo('B'),Simbolo('b')]),Producao([Simbolo('A')],[Simbolo('a'),Simbolo('B')]),Producao([Simbolo('B')],[Simbolo('a')]),Producao([Simbolo('C')],[Simbolo('b')]), Producao([Simbolo('C')],[Simbolo('a'),Simbolo('B')])] # Produções
    # simbolo_inicial = Simbolo('A') # Símbolo Inicial da Gramática
    print("\nEntrando na Fatoração\n")

    print("\nProduções Iniciais: ", producoes, '\n')

    print("\nProduções pronta para a fatoração: ", producoes, '\n')

    # procurando produções que possuam ambiguidade
    terminais_found = {}  # terminais encontrados para cada símbolo
    for simbolo in nao_terminais:
        terminais_found[simbolo] = {}
        for t in terminais:
            terminais_found[simbolo][t.valor] = 0
        for producao in producoes:
            if producao.entrada[0].valor == simbolo.valor:
                # começa a verificar
                if producao.saida[0].tipo == 0:
                    terminais_found[simbolo][producao.saida[0].valor] += 1
                    # removendo ambiguidade e adicionando novos não terminais
    for simbolo in terminais_found:
        for terminal in terminais_found[simbolo]:
            current = terminais_found[simbolo][terminal]
            # se ambiguidade for encontrada
            if current >= 2:
                print("Ambiguidade encontrada: Símbolo %s -> Terminal %s" % (simbolo, terminal))
                producoes.append(
                    Producao([insereNovoNaoTerminal(simbolo, terminal)],
                             [Simbolo(terminal), simbolo]))
    print("\nProduções Resultantes: ", producoes, '\n')

def insereNovoNaoTerminal(simbolo, terminal):
    '''Insere um novo NT, recebendo de parâmetro as produções, a lista de NT, o símbolo vítima e o terminal a ser destruído'''
    novo_simbolo = Simbolo(nao_terminais_default[len(nao_terminais)])
    nao_terminais.append(novo_simbolo)
    for producao in producoes:
        if producao.entrada[0].valor == simbolo.valor:
            if producao.entrada[0].valor == simbolo_inicial.valor:
                simbolo_inicial.valor = novo_simbolo.valor
            for elem in producao.saida:
                if elem.valor == terminal:
                    producao.saida.remove(elem)
            if len(producao.saida) == 0:
                producao.saida.append(Simbolo('&'))
    return novo_simbolo

def recursaoAEsquerda():
    '''Remove recursão geral à esquerda'''
    global producoes, nao_terminais, terminais

    print("\nEntrando na Remoção de Recursão à Esquerda\n")
    print("\nProduções Iniciais: ", producoes, '\n')
    #s_nt - itera os simbolos NT
    #p_nt - itera as producoes NT
    for s_nt in range(len(nao_terminais)):
        for p_nt in range(int(s_nt+1)):
            recursoesImediatas = []
            p = 0
            while p < len(producoes):
                if producoes[p].entrada[0].valor == nao_terminais[s_nt].valor and producoes[p].saida[0].valor == nao_terminais[p_nt].valor:
                    if producoes[p].saida[0].valor == nao_terminais[s_nt].valor:
                        recursoesImediatas.append(producoes[p])
                        del(producoes[p])
                        p -= 1
                    else:
                        producaoExcluida = copy.deepcopy(producoes[p])
                        producaoExcluida.saida = producaoExcluida.saida[1:]
                        for producao in producoes:
                            if producao.entrada[0].valor == nao_terminais[p_nt].valor:
                                aux = copy.deepcopy(producao.saida)
                                aux.extend(producaoExcluida.saida)
                                producoes.append(Producao([Simbolo(nao_terminais[s_nt].valor)],aux))
                        del(producoes[p])
                        p -= 1
                p += 1
            #remove recursoes imediatas
            if recursoesImediatas:
                novo_simbolo = Simbolo(nao_terminais_default[len(nao_terminais)])
                nao_terminais.append(novo_simbolo)
                if '&' not in terminais_string_list:
                    terminais.append(Simbolo('&'))
                    terminais_string_list.append('&')
                for producao in producoes:
                    if producao.entrada[0].valor == nao_terminais[s_nt].valor:
                        producao.saida.append(novo_simbolo)
                for producao in recursoesImediatas:
                    producao.entrada = [novo_simbolo]
                    nova_saida = producao.saida[1:]
                    nova_saida.append(novo_simbolo)
                    producao.saida = nova_saida
                    producoes.append(producao)
                producoes.append(Producao([novo_simbolo],[Simbolo('&')]))

    print("\nProduções Resultantes: ", producoes, '\n')

def getAllFirst():
    '''Faz as chamadas de funções para calcular os firsts de todos os nao terminais'''
    for nao_terminal in nao_terminais:
        getFirstByNaoTerminal(nao_terminal)

def firstRecursivo(posicao_da_producao, producao, resultado):
    """Caso o Nao Terminal tenha um nao terminal como first calcula o first do nao terminal"""
    global firsts
    temVazio = None
    for first in firsts:
        try:
            if producao.saida[posicao_da_producao] == first.nao_terminal:
                temVazio = False
                for producao_first in first.valor:
                    if producao_first.valor == '&':
                        temVazio = True
                if not temVazio:
                    string_resultado_list = []
                    for r in resultado:
                        string_resultado_list.append(r.valor)
                    for f in first:
                        if f.valor not in string_resultado_list:
                            resultado.append(f)
                    tabela[producao.entrada[0].valor, producao_first.valor] = producao
                else:
                    firstRecursivo(posicao_da_producao + 1, producao, first)
        except:
            pass
    if temVazio is None:
        first = getFirstByNaoTerminal(producao.saida[posicao_da_producao])
        string_resultado_list = []
        for r in resultado:
            string_resultado_list.append(r.valor)
        for f in first:
            if f.valor not in string_resultado_list:
                resultado.append(f)
    return resultado

def getFirstByNaoTerminal(nao_terminal):
    """Obtem o first com base no nao terminal passado como parametro"""
    global firsts, tabela
    first = []
    for producao in producoes:
        if producao.entrada[0].valor == nao_terminal.valor:
            if producao.saida[0].valor in terminais_string_list:
                first.append(producao.saida[0])
                tabela[producao.entrada[0].valor,producao.saida[0].valor] = producao
            elif producao.saida[0].valor in nao_terminais_string_list:
                first = firstRecursivo(0, producao, first)
                for f in first:
                    tabela[producao.entrada[0].valor,f.valor] = producao
    jaFoiAdiconado = False
    for f in firsts:
        if nao_terminal.valor == f.nao_terminal.valor:
            jaFoiAdiconado = True
    if not jaFoiAdiconado:
        firsts.append(FirstOrFollow(nao_terminal, first))
    return first

def getAllFollow():
    """Faz as chamadas de funções para calcular os follows de todos os nao terminais"""
    global follows
    cont = 0
    for nao_terminal in nao_terminais:
        follow = []
        if cont == 0:
            follow.append(Simbolo('$'))
        for producao in producoes:
            if nao_terminal.valor in producao.getValorDireito():
                for simbolo in range(len(producao.saida)):
                    if producao.saida[simbolo].valor == nao_terminal.valor:
                        if simbolo + 1 == len(producao.saida):
                            for f in follows:
                                if producao.entrada[0].valor == f.nao_terminal.valor:
                                    follow.extend(f.valor)
                        else:
                            if producao.saida[simbolo + 1].valor in terminais_string_list and producao.saida[simbolo + 1].valor != '&':
                                follow.append(producao.saida[simbolo + 1])
                            elif producao.saida[simbolo + 1].valor in nao_terminais_string_list:
                                for f in firsts:
                                    if producao.saida[simbolo + 1].valor == f.nao_terminal.valor:
                                        follow.extend(f.valor)
                                if derivaVazio(producao.saida[simbolo + 1]):
                                    for f in follows:
                                        if producao.entrada[0].valor == f.nao_terminal.valor:
                                            follow.extend(f.valor)
        # limpa vazios e valores repetidos
        follow_list = []
        f = 0
        while f < len(follow):
            if follow[f].valor == '&' or follow[f].valor in follow_list:
                follow.remove(follow[f])
            else:
                follow_list.append(follow[f].valor)
                f += 1
        follows.append(FirstOrFollow(nao_terminal, follow))
        if derivaVazio(nao_terminal):
            for simbolo in follow:
                tabela[nao_terminal.valor,simbolo.valor] = Producao([Simbolo(nao_terminal.valor)], [Simbolo('&')])
        cont += 1

def derivaVazio(simbolo):
    deriva = False
    for producao in producoes:
        if producao.entrada[0].valor == simbolo.valor:
            if producao.saida[0].valor == '&':
                deriva = True
    return deriva

def listaToStr(lista):
    listaStr = ''
    for l in lista:
        listaStr += l
    return listaStr

def geraGramaticaAumentada():
    global nao_terminais, producoes
    nao_terminais.append(Simbolo('Z'))
    producoes.insert(0, Producao([Simbolo('Z')],[simbolo_inicial]))

def numeraProducoes():
    global producoes
    ordem = 0
    for producao in producoes:
        ordem += 1
        producao.number = ordem

def geraCanonicos():
    global producoes
    for producao in producoes:
        producao.saida.insert(0, Simbolo('.'))

def inicializaSLR():
    numeraProducoes()
    geraGramaticaAumentada()


terminais_default = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','&','(',')','[',']','+','*']
nao_terminais_default = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y']
terminais = [] # Lista de Simbolos terminais
nao_terminais = [] # Lista de Simbolos nao terminais
nao_terminais_string_list = []
terminais_string_list = []
producoes = [] # Produções
simbolo_inicial = None # Símbolo Inicial da Gramática
firsts = [] # Firsts
follows = [] # Follows
tabela = {} # Tabela de Análise

class Simbolo(object):
    def __init__(self, valor=None):
        self.valor = valor
        # tipo 0 terminais tipo 1 nao_terminais
        if valor in terminais_default:  # não alterar a condição
            self.tipo = 0
        elif valor is None or valor == '$':
            self.tipo = None
        elif valor == '.':
            self.tipo == 2
        else:
            self.tipo = 1
    def __repr__(self):
        return self.valor

class FirstOrFollow(object):
    def __init__(self, nao_terminal, valor):
        self.nao_terminal = nao_terminal
        self.valor = valor #valor é um vetor de simbolos terminais
    def __repr__(self):
        return str(self.nao_terminal) + " -> " + str(self.valor)

class Producao(object):
    # A saida e a entrada serão um vetor simbolos
    def __init__(self, entrada, saida=[Simbolo('&')], number=None):
        self.entrada = entrada
        self.saida = saida
        self.number = number

    def getValorEsquerdo(self):
        """Retorna o valor esquerdo da produção"""
        string = ""
        for simbolo in self.entrada:
            string += simbolo.valor
        return string

    def getValorDireito(self):
        """Retorna o valor direito da produção"""
        string = ""
        for simbolo in self.saida:
            string += simbolo.valor
        return string
    
    def __repr__(self):
         return str(self.entrada)+' -> '+str(self.saida)

def mainTeste():
    global terminais, nao_terminais, producoes, simbolo_inicial, tabela
    terminais = [Simbolo('a'), Simbolo('b'), Simbolo('&')]  # Lista de Simbolos terminais
    nao_terminais = [Simbolo('A'), Simbolo('B'), Simbolo('C')]  # Lista de Simbolos nao terminais
    producoes = [Producao([Simbolo('A')], [Simbolo('C'), Simbolo('B')]), Producao([Simbolo('B')], [Simbolo('b'), Simbolo('C'), Simbolo('B')]),
                 Producao([Simbolo('B')], [Simbolo('&')]), Producao([Simbolo('C')], [Simbolo('a')])]  # Produções
    for terminal in terminais:
        terminais_string_list.append(terminal.valor)
    for nao_terminal in nao_terminais:
        nao_terminais_string_list.append(nao_terminal.valor)

    simbolo_inicial = Simbolo('A')  # Símbolo Inicial da Gramática
    getAllFirst()
    getAllFollow()
    print("Firsts:")
    print(firsts)
    print("Follows:")
    print(follows)

def mainExemplo():
    global terminais, nao_terminais, producoes, simbolo_inicial
    # Gramática 1
    # A => CB
    # B => bCB | &
    # C => a
    # codificado:
    terminais = [Simbolo('a'), Simbolo('b'), Simbolo('&')]  # Lista de Simbolos terminais
    nao_terminais = [Simbolo('A'), Simbolo('B'), Simbolo('C')]  # Lista de Simbolos nao terminais
    producoes = [Producao([Simbolo('A')], [Simbolo('C'), Simbolo('B')]), Producao([Simbolo('B')], [Simbolo('b'), Simbolo('C'), Simbolo('B')]),
                Producao([Simbolo('B')], [Simbolo('&')]), Producao([Simbolo('C')], [Simbolo('a')])]  # Produções
    simbolo_inicial = Simbolo('A')  # Símbolo Inicial da Gramática
    # Gramática 2
    # E = TG
    # G = +TG | &
    # T = FU
    # U = *FU | &
    # F = (E) | x
    # codificado
    # terminais = [Simbolo('x'), Simbolo('+'), Simbolo('*'), Simbolo('('), Simbolo(')'), Simbolo('&')]  # Lista de Simbolos terminais
    # nao_terminais = [Simbolo('E'), Simbolo('G'), Simbolo('T'), Simbolo('U'), Simbolo('F'),]  # Lista de Simbolos nao terminais
    # producoes = [Producao([Simbolo('E')], [Simbolo('T'), Simbolo('G')]), Producao([Simbolo('G')], [Simbolo('+'), Simbolo('T'), Simbolo('G')]), Producao([Simbolo('G')], [Simbolo('&')]),
    #            Producao([Simbolo('T')], [Simbolo('F'), Simbolo('U')]), Producao([Simbolo('U')], [Simbolo('*'), Simbolo('F'), Simbolo('U')]), Producao([Simbolo('U')], [Simbolo('&')]),
    #            Producao([Simbolo('F')], [Simbolo('('), Simbolo('E'), Simbolo(')')]), Producao([Simbolo('F')], [Simbolo('x')])]  # Produções
    # simbolo_inicial = Simbolo('E')  # Símbolo Inicial da Gramática
    # Gramática 3
    # A = Ca | Bd
    # B = Aa | Ce
    # C = A | B | f
    # codificado
    # terminais = [Simbolo('a'), Simbolo('d'), Simbolo('e'), Simbolo('f')]  # Lista de Simbolos terminais
    # nao_terminais = [Simbolo('A'), Simbolo('B'), Simbolo('C')]  # Lista de Simbolos nao terminais
    # producoes = [Producao([Simbolo('A')], [Simbolo('C'), Simbolo('a')]), Producao([Simbolo('A')], [Simbolo('B'), Simbolo('d')]),
    #           Producao([Simbolo('B')], [Simbolo('A'),Simbolo('a')]), Producao([Simbolo('B')], [Simbolo('C'), Simbolo('e')]),
    #           Producao([Simbolo('C')], [Simbolo('A')]), Producao([Simbolo('C')], [Simbolo('B')]),
    #           Producao([Simbolo('C')], [Simbolo('f')])]
    # simbolo_inicial = Simbolo('A')  # Símbolo Inicial da Gramática

    inicializaSLR()

    for terminal in terminais:
        terminais_string_list.append(terminal.valor)
    for nao_terminal in nao_terminais:
        nao_terminais_string_list.append(nao_terminal.valor)
    
    transformacaoGLC()
    getAllFirst()
    getAllFollow()
    print("\nFirsts:")
    print(firsts)
    print("\nFollows:")
    print(follows)
    print("\nTabela:") # montar isso bonitinho amanhã se sobrar tempo
    tabelaPretty = texttable.Texttable()
    for (keyPilha,keyEntrada) in tabela:
        tabelaPretty.add_rows([["NT na Pilha", "T na Entrada", "Saída"],[keyPilha,keyEntrada,tabela[(keyPilha,keyEntrada)]]])
    print(tabelaPretty.draw() + '\n')

#main()
mainExemplo()