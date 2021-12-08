
# Sumário

[__Bases de Dados (CC2005), DCC/FCUP__](https://www.dcc.fc.up.pt/~edrdo/aulas/bd)

[Eduardo R. B. Marques](https://www.dcc.fc.up.pt/~edrdo/), DCC/FCUP

Aplicação Python demonstrando o acesso à BD MovieStream

#  Referência

- [PyMySQL](https://pymysql.readthedocs.io/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Jinja templates](https://jinja.palletsprojects.com/en/3.0.x/)


# Instalação de dependências

## Python 3 e pip 

Deve ter o Python 3 e o gestor de pacotes pip instalado. Pode
instalar os mesmos em Ubuntu por exemplo usando:

```
sudo apt-get install python3 python3-pip
```

## Bibliotecas Python

```
pip3 install --user Flask==1.1.4 PyMySQL==1.0.2 cryptography==36.0.0
```


# Configuração da BD

Edite o ficheiro `db.py` no que se refere à configuração da sua BD, modificando os parâmetros `DB` (nome da base de dados), `USER` (nome do utilizador) e `PASSWORD` (senha do utilizador).

Teste o acesso executando:

```
python3 test_db_connection.py NOME_DE_UMA_TABELA
```

Se a configuração do acesso à BD estiver correcto, deverá ser listado o conteúdo da tabela `NOME_DE_UMA_TABELA`, por ex. a tabela `REGION` da BD MovieStream:

```
$ python3 test_db.py REGION
SELECT * FROM REGION
5 results ...
{'RegionId': 6, 'Name': 'Other countries', 'RegionManager': 17}
{'RegionId': 7, 'Name': 'America', 'RegionManager': 16}
{'RegionId': 8, 'Name': 'Asia', 'RegionManager': 15}
{'RegionId': 9, 'Name': 'Europe', 'RegionManager': 17}
{'RegionId': 10, 'Name': 'Africa', 'RegionManager': 15}
```

# Execução

Inicie a aplicação executando `python3 server.py` e interaja com a mesma
abrindo uma janela no seu browser  com o endereço [__http://localhost:9001/__](http://localhost:9001/) 

```
$ python3 server.py
2021-11-27 15:07:33 - INFO - Connected to database movie_stream
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
2021-11-27 15:07:33 - INFO -  * Running on http://0.0.0.0:9001/ (Press CTRL+C to quit)
SELECT COUNT(*) AS movies FROM MOVIE
2021-11-27 15:07:37 - INFO - SQL: SELECT COUNT(*) AS movies FROM MOVIE Args: None
SELECT COUNT(*) AS actors FROM ACTOR
2021-11-27 15:07:37 - INFO - SQL: SELECT COUNT(*) AS actors FROM ACTOR Args: None
```



