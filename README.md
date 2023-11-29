# API Controle de Presença
Este é um projeto de reconhecimento facial utilizando a biblioteca OpenCV em conjunto com o framework Flask. O objetivo principal é reconhecer rostos em tempo real a partir de uma câmera, associar esses rostos a diretórios específicos e registrar essas informações em uma planilha do Google Sheets.

# Autores
- Samuel Rodrigues
- Daniel Brisch
- Vinicius Lourenzoni
- João Goroncy
- Gilhermy 

## Estrutura do Projeto

- **`datasets/`:** Contém os diretórios de treinamento para cada pessoa.
- **`APIKEY/`:** Armazena a chave de API necessária para acessar a API do Google Sheets.
- **`templates/`:** Contém os arquivos HTML para a interface web.

## Endpoints da API

- **`/start-face-recognition`:** Inicia o reconhecimento facial.
- **`/clear-sheet`:** Limpa a planilha no Google Sheets.
- **`/get-sheet-data`:** Obtém os dados da planilha.
- **`/stop-camera`:** Para a câmera e interrompe o reconhecimento facial.

