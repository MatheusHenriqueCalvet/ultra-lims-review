
import tabula
import tkinter as tk
from tkinter import filedialog
import os
from PyPDF2 import PdfReader
import pandas as pd


class Certificado:

    def __init__(self, equipment_name=None):

        # self.validation_data = validation_data
        # self.certificate_number = certificate_number
        self.equipment_name = equipment_name
        # self.calibration_table = calibration_table
        # self.certificate_type = certificate_type
        self.certificate = {
            "Valor de referência": [],
            "Valor de indicação": [],
            "Erro": [],
            "Incerteza expandida": [],
            "Unidade de medida": [],
            "Nome do equipamento": "",
            "Data de calibração": "",
            "Número do certificado": ""
        }

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
            print(f'O código do equipamento é {self.equipment_name}')
            self.certificate["Nome do equipamento"] = self.equipment_name
            self.open_certificate(folder_path)
        else:
            folder_path = filedialog.askdirectory()
            print("O diretório selecionado foi: ", folder_path)
            files = os.listdir(folder_path)
            for file in files:
                print(file)
                filename = os.path.basename(file)
                self.equipment_name = filename[:-4]
                self.certificate = ["Nome do equipamento"].append(
                    self.equipment_name)
                print(f'O código do equipamento é {self.equipment_name}')
                self.certificate["Nome do equipamento"] = self.equipment_name
                self.open_certificate(folder_path + "/" + filename)

    def open_certificate(self, diretorio):

        self.search_certificate(diretorio)

        # print("Número de páginas no open_certificate", self.num_pages)
        # print(type(self.num_pages))

        tables = tabula.read_pdf(diretorio, pages='all')

        new_table = None

        for table in tables:
            if isinstance(table, pd.DataFrame) and len(table.columns) >= 4:
                print(
                    f'O tamanho de colunas na tabela é: {len(table.columns)}')
                table.iloc[:, :-2]
                table = table.rename(
                    columns=table.iloc[0]).drop(table.index[0])
                for column in table.columns:
                    if '\r' in column:
                        novo_nome = column.replace('\r', ' ')
                        new_table = table.rename(columns={column: novo_nome})
                print(new_table)  # irá printar a tabela

            if new_table is not None:
                for column in table.columns:
                    if new_table.columns.str.contains("VRef").any():
                        if "VRef" in column:
                            print("Existe uma coluna com o nome 'VRef'")
                            # for valor in new_table["VRef"]:
                            #     self.certificate["Valor de referência"].append(valor)
                            self.certificate["Valor de referência"].extend(
                                new_table[column].to_list())
                        if "VI" in column:
                            print("Existe uma coluna com o nome 'VI'")
                            self.certificate["Valor de indicação"].extend(
                                new_table[column].to_list())
                        if "Erro" in column:
                            print("Existe uma coluna com o nome 'VI'")
                            self.certificate["Erro"].extend(
                                new_table[column].to_list())
                        if "Incerteza" in column:
                            print("Existe uma coluna com o nome 'VI'")
                            self.certificate["Incerteza expandida"].extend(
                                new_table[column].to_list())
                        # if "Unidade" in column:
                        #     print("Existe uma coluna com o nome 'VI'")
                        #     self.certificate["Unidade de medida"].extend(
                        #         new_table[column].to_list())
            else:
                print("Tabela não encontrada")
        print(self.certificate)

    def search_certificate(self, diretorio):

        exist_validate = False
        exist_certificate = False

        with open(diretorio, 'rb') as f:
            pdf = PdfReader(f)
            self.num_pages = len(pdf.pages)
            print(f'O arquivo tem {self.num_pages} de páginas!')
            for page in pdf.pages:
                page_text = page.extract_text()

                if 'recebimento' in page_text.lower():
                    if exist_validate is not True:
                        for line in page_text.split('\n'):
                            if 'recebimento' in line.lower():
                                print("Data de calibração: ", line[65:76])
                                self.validation_data = line[65:76]
                                self.certificate["Data de calibração"] = self.validation_data
                                exist_validate = True

                if 'CERTIFICADO' in page_text:
                    if exist_certificate is not True:
                        for line in page_text.split('\n'):
                            if 'CERTIFICADO' in line:
                                print("O código do certificado é: ",
                                      line[82:91])
                                self.certificate_number = line[82:91]
                                self.certificate["Número do certificado"] = self.certificate_number
                                exist_certificate = True

        return True


balaco = Certificado()
balaco.read_certificate()
