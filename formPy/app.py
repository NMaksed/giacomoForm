import pdfplumber
import pandas as pd
import re
import json
import os
import logging
from flask import Flask, render_template, request

root_dir = os.path.abspath(os.path.dirname(__file__))

# Define o caminho absoluto para a pasta de templates
template_dir = os.path.join(root_dir, 'templates')

# Cria a aplicação Flask
app = Flask(__name__, template_folder=template_dir) 

qtd_cnc_8 = 0
qtd_ser_corte = 0
qtd_cnc_35 = 0
qtd_usi_rebaixo_4 = 0
qtd_usi_rasgo_7 = 0
qtd_servs_lam_est = 0
qtd_servs_lam_lar = 0
qtd_serv_lam_topo = 0 
qtd_ser_corte_lam_45 = 0
qtd_cnc_20 = 0
qtd_cnc_10 = 0 
qtd_cnc_3 = 0
qtd_cnc_15 = 0
qtd_cnc_1 = 0
qtd_cnc_5 = 0


# Função para extrair e somar números de uma string
def extrair_e_somar_numeros(texto):
    numeros = re.findall(r'\d+', texto)
    return sum(int(numero) for numero in numeros)

@app.route('/processar_pdf', methods=['POST'])
def processar_pdf():
    logging.info("processar_pdf chamado")
    global qtd_cnc_8, qtd_ser_corte, qtd_cnc_35, qtd_usi_rebaixo_4, qtd_usi_rasgo_7, qtd_servs_lam_est, qtd_servs_lam_lar
    global qtd_serv_lam_topo, qtd_ser_corte_lam_45, qtd_cnc_20, qtd_cnc_10, qtd_cnc_3, qtd_cnc_15, qtd_cnc_1, qtd_cnc_5
    if 'pdfFile' not in request.files:
        logging.error("Nenhum arquivo enviado")
        return 'Nenhum arquivo enviado', 400
    tabelas = []
    pdf_file = request.files['pdfFile']
    
    total_cnc_8 = 0
    total_cnc_5 = 0
    total_cnc_1 = 0
    total_cnc_15 = 0
    total_cnc_35 = 0
    total_cnc_3 = 0
    total_cnc_10 = 0
    total_cnc_20 = 0
    total_servs_corte_perf = 0
    total_servs_lam_est = 0
    total_servs_lam_lar = 0
    total_serv_lam_topo = 0
    total_ser_corte_lam_45 = 0
    total_usi_rasgo_4 = 0
    total_usi_rasgo_7 = 0
    total_usi_rebaixo_4 = 0
    total_usi_rasgo_7 = 0
    total_usi_cnt = 0
    total_ser_usi_mod = 0
    total_ser_usi_lin = 0
    total_ser_corte = 0
    total_serv_corte_bar = 0
    total_serv_corte_ins = 0
    total_ser_lam_topo = 0
    total_ser_corte_lam_45 = 0

    with pdfplumber.open(pdf_file) as pdf:
        for i, page in enumerate(pdf.pages):
            tabelas_na_pagina = page.extract_tables()
            for tabela in tabelas_na_pagina:
                df = pd.DataFrame(tabela)
                tabelas.append(df)  # Adiciona o DataFrame à lista de tabelas
    # Após iterar por todas as páginas e tabelas, faz a concatenação final
    df_final = pd.concat(tabelas, ignore_index=True)

    #print("Todas as tabelas concatenadas:")

    cnc_8 = df_final[df_final.isin(['furo_cnc_8mm_015']).any(axis=1)]
    if not cnc_8.empty:
        total_cnc_8 = extrair_e_somar_numeros(cnc_8.iloc[0].iloc[1])

    
    cnc_5 = df_final[df_final.isin(['furo_cnc_5mm_015']).any(axis=1)]
    if not cnc_5.empty:
        total_cnc_5 = extrair_e_somar_numeros(cnc_5.iloc[0].iloc[1])

    cnc_1 = df_final[df_final.isin(['furo_cnc_1mm_015']).any(axis=1)]
    if not cnc_1.empty:
        total_cnc_1 = extrair_e_somar_numeros(cnc_1.iloc[0].iloc[1])

    cnc_15 = df_final[df_final.isin(['furo_cnc_15mm_015']).any(axis=1)]
    if not cnc_15.empty:
        total_cnc_15 = extrair_e_somar_numeros(cnc_15.iloc[0].iloc[1])
        
    cnc_35 = df_final[df_final.isin(['furo_cnc_35mm_015']).any(axis=1)]
    if not cnc_35.empty:
        total_cnc_35 = extrair_e_somar_numeros(cnc_35.iloc[0].iloc[1])
        
    cnc_3 = df_final[df_final.isin(['furo_cnc_3mm_015']).any(axis=1)]
    if not cnc_3.empty:
        total_cnc_3 = extrair_e_somar_numeros(cnc_3.iloc[0].iloc[1])
        
    cnc_10 = df_final[df_final.isin(['furo_cnc_10mm_015']).any(axis=1)]
    if not cnc_10.empty:
        qtd_cnc_10 = extrair_e_somar_numeros(cnc_10.iloc[0].iloc[1])
        
    cnc_20 = df_final[df_final.isin(['furo_cnc_20mm_015']).any(axis=1)]
    if not cnc_20.empty:
        total_cnc_20 = extrair_e_somar_numeros(cnc_20.iloc[0].iloc[1])
        
    servs_corte_perf = df_final[df_final.isin(['servico_corte_perfil_015']).any(axis=1)]
    if not servs_corte_perf.empty:
        qtd_servs_corte_perf = extrair_e_somar_numeros(servs_corte_perf.iloc[0].iloc[1])
        
    serv_lam_est = df_final[df_final.isin(['ser_lam_est_015']).any(axis=1)]
    if not serv_lam_est.empty:
        total_servs_lam_est = extrair_e_somar_numeros(serv_lam_est.iloc[0].iloc[1])
        
    serv_lam_lar = df_final[df_final.isin(['ser_lam_lar_015']).any(axis=1)]
    if not serv_lam_lar.empty:
        total_servs_lam_lar = extrair_e_somar_numeros(serv_lam_lar.iloc[0].iloc[1])
        
    usi_rasgo_4 = df_final[df_final.isin(['usi_rasgo_4mm_015']).any(axis=1)]
    if not usi_rasgo_4.empty:
        qtd_usi_rasgo_4 = extrair_e_somar_numeros(usi_rasgo_4.iloc[0].iloc[1])

    usi_rasgo_7 = df_final[df_final.isin(['usi_rasgo_7mm_015']).any(axis=1)]
    if not usi_rasgo_7.empty:
        total_usi_rasgo_7 = extrair_e_somar_numeros(usi_rasgo_7.iloc[0].iloc[1])

    usi_rebaixo_4 = df_final[df_final.isin(['usi_rasgo_4mm_015']).any(axis=1)]
    if not usi_rebaixo_4.empty:
        total_usi_rebaixo_4 = extrair_e_somar_numeros(usi_rebaixo_4.iloc[0].iloc[1])

    usi_rebaixo_7 = df_final[df_final.isin(['usi_rebaixo_7mm_015']).any(axis=1)]
    if not usi_rebaixo_7.empty:
        qtd_usi_rebaixo_7 = extrair_e_somar_numeros(usi_rebaixo_7.iloc[0].iloc[1])

    usi_cnt = df_final[df_final.isin(['usi_cnt_l_015']).any(axis=1)]
    if not usi_cnt.empty:
        qtd_usi_cnt = extrair_e_somar_numeros(usi_cnt.iloc[0].iloc[1])

    ser_usi_mod = df_final[df_final.isin(['ser_usinagem_modelada_015']).any(axis=1)]
    if not ser_usi_mod.empty:
        qtd_ser_usi_mod = extrair_e_somar_numeros(ser_usi_mod.iloc[0].iloc[1])

    ser_usi_lin = df_final[df_final.isin(['ser_usinagem_linear_015']).any(axis=1)]
    if not ser_usi_lin.empty:
        qtd_ser_usi_lin = extrair_e_somar_numeros(ser_usi_lin.iloc[0].iloc[1])

    ser_corte = df_final[df_final.isin(['ser_corte_015']).any(axis=1)]
    if not ser_corte.empty:
        total_ser_corte = extrair_e_somar_numeros(ser_corte.iloc[0].iloc[1])

    #ser_corte_45 = df[df.isin(['ser_corte_45g_015']).any(axis=1)]
    #if not ser_corte_45.empty:
    #    qtd_ser_corte_45 = extrair_e_somar_numeros(ser_corte_45.iloc[0].iloc[1])
    #else:
    #    qtd_ser_corte_45 = 0
        
    serv_corte_bar = df_final[df_final.isin(['servico_corte_barra_015']).any(axis=1)]
    if not serv_corte_bar.empty:
        qtd_serv_corte_bar = extrair_e_somar_numeros(serv_corte_bar.iloc[0].iloc[1])

    serv_corte_ins = df_final[df_final.isin(['servico_instal_perfil_015']).any(axis=1)]
    if not serv_corte_ins.empty:
        qtd_serv_corte_ins = extrair_e_somar_numeros(serv_corte_ins.iloc[0].iloc[1])

    ser_lam_topo = df_final[df_final.isin(['lam_topo_015']).any(axis=1)]
    if not ser_lam_topo.empty:
        total_serv_lam_topo = extrair_e_somar_numeros(ser_lam_topo.iloc[0].iloc[1])
    
    ser_corte_lam_45 = df_final[df_final.isin(['ser_cor_lam_45g_015']).any(axis=1)]
    if not ser_corte_lam_45.empty:
        total_ser_corte_lam_45 = extrair_e_somar_numeros(ser_corte_lam_45.iloc[0].iloc[1])
 
    #ser_dup_pai = df[df.isin(['ser_dup_paineis_015']).any(axis=1)]
    #if not ser_dup_pai.empty:
    #    qtd_ser_dup_pai = extrair_e_somar_numeros(ser_dup_pai.iloc[0].iloc[1])
    #else:
    #    qtd_ser_dup_pai = 0
        
    #ser_eng_pai = df[df.isin(['ser_eng_paineis_015']).any(axis=1)]
    #if not ser_eng_pai.empty:
    #    qtd_ser_eng_pai = extrair_e_somar_numeros(ser_eng_pai.iloc[0].iloc[1])
    #else:
    #    qtd_ser_eng_pai = 0
        
    qtd_cnc_8 = total_cnc_8
    qtd_ser_corte = total_ser_corte
    qtd_cnc_35 = total_cnc_35
    qtd_usi_rebaixo_4 = total_usi_rebaixo_4
    qtd_usi_rasgo_7 = total_usi_rasgo_7
    qtd_servs_lam_est = total_servs_lam_est
    qtd_servs_lam_lar = total_servs_lam_lar
    qtd_serv_lam_topo = total_serv_lam_topo
    qtd_ser_corte_lam_45 = total_ser_corte_lam_45
    qtd_cnc_20 = total_cnc_20
    qtd_cnc_10 = total_cnc_10
    qtd_cnc_3 = total_cnc_3
    qtd_cnc_15 = total_cnc_15
    qtd_cnc_1 = total_cnc_1
    qtd_cnc_5 = total_cnc_5
    
    
    
    corte = qtd_ser_corte
    furo_dob = qtd_cnc_35
    canal = qtd_usi_rebaixo_4 + qtd_usi_rasgo_7
    fitagem = qtd_servs_lam_est + qtd_servs_lam_lar + qtd_serv_lam_topo + qtd_ser_corte_lam_45
    furos_cnc = qtd_cnc_15 + qtd_cnc_1 + qtd_cnc_5 + qtd_cnc_8 + qtd_cnc_20 + qtd_cnc_10 + qtd_cnc_3  
    
    valores_atualizados = {
        "corte": corte,
        "furo_dob": furo_dob,
        "canal": canal,
        "fitagem": fitagem,
        "furos_cnc": furos_cnc
    }
    print(valores_atualizados)
    return json.dumps(valores_atualizados)

@app.route('/')
def index():
    corte = qtd_ser_corte
    furo_dob = qtd_cnc_35
    canal = qtd_usi_rebaixo_4 + qtd_usi_rasgo_7
    fitagem = qtd_servs_lam_est + qtd_servs_lam_lar + qtd_serv_lam_topo + qtd_ser_corte_lam_45
    furos_cnc = qtd_cnc_15 + qtd_cnc_1 + qtd_cnc_5 + qtd_cnc_8 + qtd_cnc_20 + qtd_cnc_10 + qtd_cnc_3  
    return render_template('index.html', corte=corte, furo_dob=furo_dob, canal=canal, fitagem=fitagem, furosist=furos_cnc)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)