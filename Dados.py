from datetime import datetime
from datetime import date
import tabula
import PyPDF2
import pandas as pd
import os
import glob

class Dados:

    nome_fornecedor = None
    im_equipamento = 'IM 0000'
    search_word = 'Nº'
    numero_certificado = None
    faixaUtilizacao = str
    nomeFaixa = str
    tituloFaixa = str
    quantidadePontos = int
    data_atual = datetime.today().strftime('%d-%m-%Y')
    hj = date.today()
    data_prevista = date.fromordinal(hj.toordinal()+15).strftime('%d-%m-%Y')
    pontos = None
    unidadeDeMedida = None

    def __init__(self):
        
        self.destino_certificados = 'C:/Users/mathe/OneDrive/Documentos/Certificados'

    def buscaCertificado(self):

        certificados = glob.glob(os.path.join(self.destino_certificados, '*.pdf'))

        for certificado in certificados:
            codigo_certificado = os.path.basename(certificado)
            with open(self.destino_certificados+'/'+codigo_certificado,'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                num_pages = len(pdf_reader.pages)
                page = pdf_reader.pages[1]
                page_text = page.extract_text()
                print(page_text)
                for line in page_text.splitlines():
                    if self.search_word in line:
                        line_words = line.split()
                        numero_certificado = ''.join(line_words[line_words.index(self.search_word)+1:])
                        #print(f'A palavra "{self.search_word}" foi encontrada na página {i+1}, linha: {line}')
                        print("Número do certificado do equipamento {} é: ".format(codigo_certificado[:7]) + numero_certificado)

    def pegaPontos(self):

        lista_tabelas = tabula.read_pdf(r'C:\Users\mathe\OneDrive\Documentos\Certificados\IM 0000.pdf', pages='2')
        tabela = lista_tabelas[0]
        df = tabela
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        quantidadePontos = df.shape[0]
        print(quantidadePontos)
        valor1 = df.loc[1, 'VRef']
        valor2 = df.loc[quantidadePontos, 'VRef']
        nomeFaixa = ("{} a {}".format(valor1, valor2))
        print(nomeFaixa)
        #if df.loc[1, 'Unidade de\rMedida'] == 's':
            #print("É tempo")
            #nomeFaixa = 'Tempo'
        #else:
           # print("Não é unidade para a grandeza de tempo!")
        #print(nomeFaixa)

        self.pontos = []
        for i in range(1, quantidadePontos + 1):
            vref = df.loc[i, 'VRef']
            self.pontos.append(vref)

        print(self.pontos)

    def UnidadeDeMedida(self):
        
        lista_tabelas = tabula.read_pdf(r'C:\Users\mathe\OneDrive\Documentos\Certificados\IM 0000.pdf', pages='2')
        df = lista_tabelas[0]
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        self.unidadeDeMedida =  df.loc[1, 'Unidade de\ Medida']
        print(self.unidadeDeMedida)

        with open('ListaGrandezas', 'r', encoding='UTF-8') as f:
            linhas = f.readlines()

        dicionario = {}
        for linha in linhas:
            partes = linha.strip().split(' - ')
            if len(partes) == 2:
                chave, valor = partes
                dicionario[chave] = valor

        #print(dicionario)

        valor_dic = dicionario.get(self.unidadeDeMedida)
        if valor_dic is not None:
            print(valor_dic)
        else:
            print("A chave {} não existe no dic".format(self.unidadeDeMedida))

    def getPontoValue(self):
        self.pegaPontos()
        return self.pontos
        
    def getUnidadeMedida(self):
        self.UnidadeDeMedida()
        return self.unidadeDeMedida





    # class Dados:
        
    #     nome_fornecedor = 'Trescal'
    #     im_equipamento = 'IM 0000'


    #     data_atual = datetime.today().strftime('%d-%m-%Y')
    #     print("essa é a data atual: ", data_atual)

    #     #pega data + 15 dias

    #     data = datetime.today()
    #     dataPrevista = data.day 
    #     print(dataPrevista)

    #     hj = date.today()
    #     print (hj.toordinal())
    #     734694
    #     teste = date.fromordinal(hj.toordinal()+45).strftime('%d-%m-%YT%H:%M:%S')
    #     print (teste)

    #     data_prevista = date.fromordinal(hj.toordinal()+15).strftime('%d-%m-%Y')

    #     print(data_prevista)

    #     im = 'IM 0000'
    #     codigoIm = im[3:]
    #     print(codigoIm)

    # class lerPdf:
        
    #     faixaUtilizacao = str
    #     ponto = str
    #     nomeFaixa = str
    #     tituloFaixa = str
    #     quantidadePontos = int

    #     nomeFornecedor = 'Trescal'

    #     lista_tabelas = tabula.read_pdf(r'C:\Users\matheus.calvet\Desktop\Python\Ultra_Lims 3.0.0.01\Ultra_Lims 3.0.0.01\Ultra_Lims 3.0\IM1052.pdf', pages='2')

    #     tabela = lista_tabelas[0]
    #     df = tabela
    #     df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    #     print(df)

    #     ponto = 'a'

    #     quantidadePontos = df.shape[0]

    #     valor1 = df.loc[1, 'VI']
    #     valor2 = df.loc[quantidadePontos, 'VI']

    #     nomeFaixa = ("{} a {}".format(valor1, valor2))

    #     print(nomeFaixa)

    #     if df.loc[1, 'Unidade de\rMedida'] == 's':
    #         print("É tempo")
    #         nomeFaixa = 'Tempo'
    #     else:
    #         print("Não é unidade para a grandeza de tempo!")

    #     print(nomeFaixa)

    #     def adicionaPonto(ponto):
    #         print("Ponto adicionado!")
    #         lista = []
    #         lista.append(ponto)
    #         for ponto in lista:
    #             print("Ponto: {}".format(ponto))
            

    #     for i in range(1, len(df) + 1):
    #         vref = df.loc[i, 'VRef']
    #         ponto = vref
    #         adicionaPonto(ponto)

                
    #     print(len(df))
        