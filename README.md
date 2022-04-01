- **Descrição:** O plugin logging-app-cs-plugin adiciona em uma stack a capacidade de padronizar a escrita de logs. 

- **Categoria:** Observability. 
- **Stack:** dotnet.
- **Criado em:** 03/02/2022. 
- **Última atualização:** 03/02/2022.
- **Download:** https://github.com/stack-spot/logging-app-cs-plugin.git.


## **Visão Geral**
### **logging-app-cs-plugin**

O **logging-app-cs-plugin** adiciona em uma stack a capacidade de padronizar a escrita de logs, reduzindo a verbosidade de códigos, proporcionando celeridade e observações mais precisas.

## **Uso**

### **Pré-requisitos**
Para utilizar esse plugin, é necessário ter uma stack dotnet criada pelo cli.

### **Instalação**
Para fazer o download do **logging-app-cs-plugin**, siga os passos abaixo:

**Passo 1.** Copie e cole a URL abaixo no seu navegador/terminal:
```
https://github.com/stack-spot/logging-app-cs-plugin.git
```

## **Configuração**

### **Inputs**
Os inputs necessários para utilizar o plugin são:
| **Campo** | **Valor** | **Descrição** |
| :--- | :--- | :--- |
| Log Level| Padrão: "INFO" | level de log, valores: DEBUG, INFO, WARN, ERROR, FATAL. |
| Log Extension |  |  Complemta com informações de contexto, valores: OpenTracing, XRay, CorrelationId |

### **Exemplo de uso**
- [**Nuget**](https://www.nuget.org/packages/StackSpot.Logging/)
