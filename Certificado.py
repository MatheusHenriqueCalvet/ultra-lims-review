import tabula
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
from PyPDF2 import PdfReader


class Certificado:

    def __init__(self, equipment_name=None):

        # self.validation_data = validation_data
        # self.certificate_number = certificate_number
        self.equipment_name = equipment_name
        # self.calibration_table = calibration_table
        # self.certificate_type = certificate_type

    def read_certificate(self):

        root = tk.Tk()

        root.withdraw()

        ask = int(
            input("Você deseja abrir uma pasta ou selecionar um arquivo específico? "))

        if ask == 1:
            folder_path = filedialog.askopenfilename()
            print("O arquivo selecionado foi: ", folder_path)
            filename = os.path.basename(folder_path)
            self.equipment_name = filename[:-4]
            print(filename)
            self.open_certificate(folder_path)
        else:
            folder_path = filedialog.askdirectory()
            print("O diretório selecionado foi: ", folder_path)
            files = os.listdir(folder_path)
            for file in files:
                print(file)
                filename = os.path.basename(file)
                self.equipment_name = filename[:-4]
                self.open_certificate(folder_path + "/" + filename)

    def open_certificate(self, diretorio):

        self.search_certificate(diretorio)

        lista_tabelas = tabula.read_pdf(diretorio, pages='all')

        tabela = lista_tabelas[0]

        tabela = tabela.iloc[:, :-2]

        teste = tabela.rename(columns=tabela.iloc[0]).drop(tabela.index[0])

        for column in teste.columns:
            # print("coluna: ", column)
            if '\r' in column:
                # print("Nome com quebra-libra")
                novo_nome = column.replace('\r', '')
                teste = teste.rename(columns={column: novo_nome})
            # else:
                # print("Nome sem quebra-linha")

        print(teste)

    def search_certificate(self, diretorio):
        with open(diretorio, 'rb') as f:
            pdf = PdfReader(f)
            for page in pdf.pages:
                page_text = page.extract_text()
                if 'recebimento' in page_text.lower():
                    print("Achou o Recebimento")
                    for line in page_text.split('\n'):
                        if 'recebimento' in line.lower():
                            print("Data de calibração: ", line[65:76])

                if 'CERTIFICADO' in page_text:
                    print("Achou o certificado")
                    for line in page_text.split('\n'):
                        if 'CERTIFICADO' in line:
                            print("certificado: ", line[82:91])

        return True


balaco = Certificado()
balaco.read_certificate()
