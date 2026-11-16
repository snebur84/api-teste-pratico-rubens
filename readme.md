# API teste Utilizando fastAPI

## Descrição
Esta API foi criada como demonstração básica de criação de API com consumo de dados remotos e conexão com bando de dados

## Stacks envolvidas
- python
    - fastAPI, uvicorn, sqlalchemy, pydantic
- postgres
- docker e docker compose

---

## Arquitetura da Solução

A solução foi desenhada para rodar em conteiners (db: postgres e api: python fastAPI), orquestrado por docker compose.
No diretório raiz da aplicação encontram-se os arquivos Dockerfile (necessário para a api) e docker-compose.yml (responsável pelo build e orquestração dos conteiners).

### Configuração do ambiente

Existe um arquivo .env_exemplo que deve ser alterado de acordo com as configurações desejadas pela aplicação, segue abaixo o conteúdo de exemplo do arquivo e as variáveis que precisam ser ajustadas:

```text
# Chave de acesso à API
API_KEY=minha-chave-super-secreta-producao-987
APP_NAME="Minha API Segura"

# Configurações do banco de dados
DB_HOST=localhost
DB_PORT=5432
DB_USER=meu_usuario
DB_PASSWORD=minha_senha_super_secreta
DB_NAME=meu_banco_de_dados
```

### Build e Deploy

Acesse o diretório raiz da aplicação e executar os comandos abaixo para buildar e deploiar a aplicação:

```bash
docker compose build && docker compose up -d

```

Após a finalização a aplicação estará acessível pelo endereço:

[http://ip_do_servidor:8000](http://ip_do_servidor:8000)

Para verificar se o deploy ocorreu corretamente, execute:

```bash
docker ps

```

Para verificar possíveis falhas, utilize:
- Para API:

```bash
docker logs api

```

- Para DB:
```bash
docker logs db

```



## Arquitetura da API
A aplicação foi escrita em uma arquitura MVC simplificada, conforme diagrama.

```text
app/
├── controllers/
│   └── controllers.py # Camada de controle simplificada
├── models/            
│   ├── models.py # Modelos para o ORM SqlAlchemy
│   └── schemas.py # Configurações de visualizações e padrão de requests e responses das rotas
├── database.py # Script de conexão com o banco de dados
├── config.py # Arquivo para carregamento das configurações
├── client_api.py # Script de conexão com a API open-meteo
└── app.py # Script de inicialização da aplicação
```

---

## Entidades e Relacionamentos

### Cidade
* `id` (Chave Primária, numérico)
* `nome` (Obrigatório, Único, máximo de 100 caracteres)
* `latitude` (Obrigatório, numérico real)
* `longitude` (Obrigatório, numérico real)
* `elevation` (Opcional, numérico real)
* `timezone` (Obrigatório, Único, máximo de 50 caracteres)
* `timezone_abbreviation` (Opcional, Único, máximo de 10 caracteres)
* `utc_offset_seconds` (Obrigatório, numérico)
* `atualizado_em` (Preenchida automaticamente)
* `previsoes` (Preenchida automaticamente)

### PrevisaoHoraria
* `id` (Chave Primária, numérico)
* `cidade_id` (Obrigatório, chave estrangeira de Cidade existente)
* `data_hora` (Obrigatório, Data)
* `temperature_2m` (Opcional, numérico)
* `relative_humidity_2m` (Opcional, numérico)
* `surface_pressure` (Opcional, numérico real)
* `wind_speed_10m` (Opcional, numérico real) 
* `wind_direction_10m` (Opcional, numérico)
* `precipitation` (Opcional, numérico real)
* `cidade` (Preenchida automaticamente)

---

## Endpoints da API

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| **GET** | `/api/tempo` | Devolve um json contendo os dados climáticos de uma cidade de acordo com os filtros enviados |
| **POST** | `/api/tempo` | Insere/Atualiza os dados climáticos de determinada cidade |

---

## Documentação
A documentação da API encontra-se no endpoint abaixo

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| **GET** | `/docs#` | Abre uma página web com a documentação e permite executar os endpoints |

---