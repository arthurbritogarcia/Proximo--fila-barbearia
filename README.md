# Próximo! - Fila virtual para barbearias

Trabalho de Engenharia de Software (3º período).

## O problema

Muitas barbearias atendem por ordem de chegada. O cliente chega, encontra várias pessoas na frente e precisa ficar esperando lá, sem poder sair, para não perder a vez.

## A solução

O cliente entra na fila pelo celular, acompanha a posição e o tempo de espera e só vai para a barbearia quando estiver perto da vez dele. O barbeiro controla a fila, chama o próximo e consegue adicionar clientes que chegaram sem o app.

## Funcionalidades

**Cliente**
- Entrar na fila escolhendo o serviço
- Ver a posição e o tempo estimado de espera
- Sair da fila

**Barbeiro**
- Ver a fila e quem está na cadeira
- Finalizar o atendimento e chamar o próximo
- Adicionar cliente que chegou no balcão (sem app)
- Remover cliente da fila
- Ver quantos foram atendidos e o faturamento do dia

## Serviços (valores de exemplo)

| Serviço | Tempo | Preço |
| --- | --- | --- |
| Corte | 30 min | R$ 45 |
| Barba | 20 min | R$ 30 |
| Sobrancelha | 10 min | R$ 15 |
| Corte + barba | 45 min | R$ 70 |
| Corte + sobrancelha | 35 min | R$ 55 |
| Corte + barba + sobrancelha | 55 min | R$ 80 |

## Como rodar

Precisa ter o Python 3 instalado. No terminal:

```
python proximo.py
```

## Limitações do protótipo

Os dados ficam guardados em listas, na memória, e se perdem quando o programa fecha. Numa versão real, a fila ficaria em um banco de dados num servidor, para que o cliente e o barbeiro vejam a mesma fila, cada um no seu celular.
