from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import pandas as pd
import json

app = FastAPI()

# Mapa base — modelo padrão, nunca modificado diretamente
COLUMN_MAP = {
    "nome_estrela": ["nome"],
    "nome_planeta": ["planeta"],
    "distancia_luz_estrela": ["distancia_luz"],
    "temperatura_planeta": ["temperatura"],
    "discovery": ["discovery"]
}

@app.post("/upload_csv")
async def upload_csv(
    file: UploadFile = File(...),
    csv_map: Optional[str] = Form(None)  # JSON opcional: {"coluna_suja": "coluna_padrao"}
):
    try:
        df = pd.read_csv(file.file)

        # 🔹 Faz uma cópia local do mapa base para esta requisição
        column_map_local = {k: v.copy() for k, v in COLUMN_MAP.items()}

        # 🔹 Atualiza com o mapa enviado, se houver
        if csv_map:
            try:
                map_dict = json.loads(csv_map)
                for csv_col, std_col in map_dict.items():
                    if std_col in column_map_local:
                        column_map_local[std_col].append(csv_col)
                    else:
                        column_map_local[std_col] = [csv_col]
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="csv_map deve ser um JSON válido")

        # 🔹 Cria mapeamento reverso (nome sujo → nome padronizado)
        reverse_map = {}
        for std_name, variants in column_map_local.items():
            for var in variants:
                reverse_map[var] = std_name

        # 🔹 Renomeia as colunas e remove as desconhecidas
        df = df.rename(columns=lambda x: reverse_map.get(x, None))
        df = df[[col for col in df.columns if col is not None]]

        # 🔹 Converte pra JSON (aqui é o dado que você pode mandar pra IA)
        data_json = df.to_dict(orient="records")

# Chamar a IA aqui------------------------------------------Chamar a IA aqui-------------------------------------------Chamar a IA aqui-------------------------------------------Chamar a IA aqui

        print("Teste", json.dumps(data_json, indent=2))
        print(data_json[1]["nome_planeta"])

        # Retorna direto pro front... MÉTODO QUE VAI RETORNAR O RESULT DA IA
        """
        return {
            "filename": file.filename,
            "columns": df.columns.tolist(),
            "ia_result": resultado_ia
        }

        """

# Chamar a IA aqui------------------------------------------Chamar a IA aqui-------------------------------------------Chamar a IA aqui-------------------------------------------Chamar a IA aqui

        # 🔹 Retorno final (aqui depois entrará a chamada da IA)
        return {
            "filename": file.filename,
            "columns": df.columns.tolist(),
            "data": data_json
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar CSV: {str(e)}")

      # linha 47 EXEMPLO print("Teste", json.dumps(data_json, indent=2)) -> Exemplo de como usar o Json... ele fica armazenado dentro da variavel data_json,
    # remover a linha no projeto final. É só pra demonstração

