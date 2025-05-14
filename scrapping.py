from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as pd
import time
from selenium.common.exceptions import TimeoutException

caminho_driver = "C:\Program Files\chromedriver-win64\chromedriver.exe"

service = Service(caminho_driver)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=service, options=chrome_options)

url_base = "https://masander.github.io/AlimenticiaLTDA-financeiro/"

driver.get(url_base)

time.sleep(5)

dic_despesas = {
    "id_despesa": [],
    "data": [],
    "tipo": [],
    "setor": [],
    "valor": [],
    "fornecedor": []
}

dic_orcamentos = {
    "setor": [],
    "mes": [],
    "ano": [],
    "valor_previsto": [],
    "valor_realizado": []
}

while True:
    print(f"Coletando dados das despesas")

    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((
                By.XPATH, "//tr[contains(@style, 'border-bottom: 1px solid rgb(221, 221, 221)')]"
            )))
    except TimeoutException as te:
        print("Tempo de espera excedido!", te)
    
    despesas = driver.find_elements( By.XPATH, "//tr[contains(@style, 'border-bottom: 1px solid rgb(221, 221, 221)')]")
    
    for despesa in despesas:
        try:
            id_despesa = despesa.find_element(By.CLASS_NAME, "td_id_despesa").text.strip()
            data = despesa.find_element(By.CLASS_NAME, "td_data").text.strip()
            tipo = despesa.find_element(By.CLASS_NAME, "td_tipo").text.strip()
            setor = despesa.find_element(By.CLASS_NAME, "td_setor").text.strip()
            valor = despesa.find_element(By.CLASS_NAME, "td_valor").text.strip()
            fornecedor = despesa.find_element(By.CLASS_NAME, "td_fornecedor").text.strip()
            
            print(f"""
                  id: {id_despesa}
                  data: {data}
                  tipo: {tipo}
                  setor: {setor}
                  valor: {valor}
                  fornecedor: {fornecedor}
                  """)
            
            dic_despesas["id_despesa"].append(id_despesa)
            dic_despesas["data"].append(data)
            dic_despesas["tipo"].append(tipo)
            dic_despesas["setor"].append(setor)
            dic_despesas["valor"].append(valor)
            dic_despesas["fornecedor"].append(fornecedor)
        except Exception as e:
            print("Erro ao coletar dados", e)
    
    try:
        botao_orcamento = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Orçamentos')]"))
        )
        
        if botao_orcamento:
            driver.execute_script("arguments[0].click();", botao_orcamento)
            time.sleep(5)
    except Exception as e:
        print("Erro ao encontrar botão")
    
    print(f"Coletando dados dos orcamentos")

    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((
                By.XPATH, "//tr[contains(@style, 'border-bottom: 1px solid rgb(221, 221, 221)')]"
            )))
        
    except TimeoutException as te:
        print("Tempo de espera excedido!", te)
    
    orcamentos = driver.find_elements(By.XPATH, "//tr[contains(@style, 'border-bottom: 1px solid rgb(221, 221, 221)')]")
    
    for orcamento in orcamentos:
        try:
            setor_orc = orcamento.find_element(By.CLASS_NAME, "td_setor").text.strip()
            mes = orcamento.find_element(By.CLASS_NAME, "td_mes").text.strip()
            ano = orcamento.find_element(By.CLASS_NAME, "td_ano").text.strip()
            valor_previsto = orcamento.find_element(By.CLASS_NAME, "td_valor_previsto").text.strip()
            valor_realizado = orcamento.find_element(By.CLASS_NAME, "td_valor_realizado").text.strip()
            
            print(f"""
                  setor orcamento: {setor_orc}
                  mes: {mes}
                  ano: {ano}
                  valor_previsto: {valor_previsto}
                  valor_realizado: {valor_realizado}
                """)
            
            dic_orcamentos["setor"].append(setor_orc)
            dic_orcamentos["mes"].append(mes)
            dic_orcamentos["ano"].append(ano)
            dic_orcamentos["valor_previsto"].append(valor_previsto)
            dic_orcamentos["valor_realizado"].append(valor_realizado)
        except Exception as e:
            print("Erro ao coletar dados", e)
    
    break

driver.quit()

df_despesas = pd.DataFrame(dic_despesas)
df_orcamentos = pd.DataFrame(dic_orcamentos)

df_despesas.to_excel("despesas.xlsx", index=False)

print(f"Arquivo 'despesas' salvo com sucesso! {len(df_despesas)} produtos armazenados")

df_orcamentos.to_excel("orcamentos.xlsx", index=False)

print(f"Arquivo 'orcamentos' salvo com sucesso! {len(df_orcamentos)} produtos armazenados")
    
    
    
