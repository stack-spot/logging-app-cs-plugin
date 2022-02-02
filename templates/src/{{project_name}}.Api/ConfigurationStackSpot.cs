using System.Diagnostics.CodeAnalysis;
using StackSpot.Logging;

namespace {{project_name}}.Api;

[ExcludeFromCodeCoverage]
public static class ConfigurationStackSpot
{
    public static IServiceCollection AddStackSpot(this IServiceCollection services, IConfiguration configuration, IWebHostEnvironment environment)
    {
        services.AddLogger();
        return services;
    }    

    public static IApplicationBuilder UseStackSpot(this IApplicationBuilder app, IConfiguration configuration, IWebHostEnvironment environment)
    {
        return app;
    }
}