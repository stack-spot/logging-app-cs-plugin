#### **Inputs**

Os inputs necessários para utilizar o plugin são:
| **Campo** | **Valor** | **Descrição** |
| :--- | :--- | :--- |
| AppName |  |  Nome da Aplicação |
| Log Level| Padrão: "INFO" | level de log, valores: DEBUG, INFO, WARN, ERROR, FATAL. |

* APP_NAME - nome da aplicação - Campo Obrigatório
* LOG_LEVEL - level de log, valores: DEBUG, INFO, WARN, ERROR, FATAL. 

Você pode configurar as variáveis no arquivo `appsettings.json`.

```json
{
  "AppName": "MyAppName",  
  "LogOptions": {
    "LogLevel": "INFO"
  }
}
```
Quando executar na máquina local, você pode configurar as variáveis de ambientes no arquivo `launchSettings.json`.

```json
{
  "$schema": "http://json.schemastore.org/launchsettings.json",
  "profiles": {
    "Sample.WebApi": {
      "commandName": "Project",
      "launchBrowser": true,
      "launchUrl": "sample",
      "environmentVariables": {
        "APP_NAME": "MyAppName",
        "LOG_LEVEL": "INFO",
        "ASPNETCORE_ENVIRONMENT": "Development"
      },
      "applicationUrl": "http://localhost:5000"
    }
  }
}
```
#### **Configurações**
Adicione ao seu `IServiceCollection` via `services.AddLogger()` no `Startup` da aplicação ou `Program`. 

Utilizando váriavel de ambiente

```csharp
services.AddLogger();
```

Utilizando `appsettings.json`

```csharp
services.AddLogger(Configuration);
```

Caso precise de um log completo com informações de contexto, instale os pacotes adicionais e utilize a configuração abaixo:

Exemplo OpenTracing:

```csharp
services.AddLogger()
        .WithOpenTracing()
        .WithCorrelation();
```

Exemplo XRay:

```csharp
services.AddLogger()
        .WithXRayTraceId()
        .WithCorrelation();
```

Estendemos os métodos do `ILogger<>` transformado o output, adicionalmente estamos provendo duas sobrecargas novas para suportar TAGs e log de Objetos no campo Data.

```csharp
[ApiController]
[Route("[controller]")]
public class SampleController : ControllerBase
{
    private readonly ILogger<SampleController> _logger;

    public SampleController(ILogger<SampleController> logger)
    {
        _logger = logger;
    }

    [HttpGet()]
    public async Task<IActionResult> Get()
    {
        var someEntity = new SampleEntity();
        _logger.LogDebug("My DEBUG Log Message", someEntity, "Tag01", "Tag02");
        return Ok();
    }
}
```

#### Sobrecargas disponíveis

Debug

```csharp
_logger.LogDebug("My DEBUG Log Message");
_logger.LogDebug("My DEBUG Log Message", "Tag01", "Tag02");
_logger.LogDebug("My DEBUG Log Message", someEntity, "Tag01", "Tag02");
```

Info

```csharp
_logger.LogInformation("My INFO Log Message");
_logger.LogInformation("My INFO Log Message", "Tag01", "Tag02");
_logger.LogInformation("My INFO Log Message", someEntity, "Tag01", "Tag02");
```

Warning

```csharp
_logger.LogWarning("My WARNING Log Message");
_logger.LogWarning("My WARNING Log Message", "Tag01", "Tag02");
_logger.LogWarning("My WARNING Log Message", someEntity, "Tag01", "Tag02");
```

Error

```csharp
_logger.LogError("My ERROR Log Message");
_logger.LogError("My ERROR Log Message", "Tag01", "Tag02");
_logger.LogError("My ERROR Log Message", someEntity, "Tag01", "Tag02");
```

Fatal

```csharp
_logger.LogFatal("My ERROR Log Message");
_logger.LogFatal("My ERROR Log Message", "Tag01", "Tag02");
_logger.LogFatal("My ERROR Log Message", someEntity, "Tag01", "Tag02");
```

#### Output completo

Mostramos abaixo o output completo preenchido com informações do dotnet.

```json
{
    "timeStamp": "2021-04-06T14:50:33.6610795Z",
    "appName": "MyAppName",
    "message": "An unhandled exception has occurred while executing the request.",
    "logger": "Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware",
    "level": "ERROR",
    "tags": ["Tag01", "Tag02"],
    "data": {
        "field1": "Test01",
        "field2": "Test02"
    },
    "exception": {
        "name": "DivideByZeroException",
        "message": "Attempted to divide by zero.",
        "stackTrace": "   at Sample.WebApi.Controllers.SampleController.Get() in ..."
    },
    "context": {
        "spanId": "1af157b8bee48886",
        "traceId": "1af157b8bee48886",
        "correlationId": "614bc03a1eab685315a897fe1405a935"
    }
}
```