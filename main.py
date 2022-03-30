from templateframework.runner import run
from templateframework.template import Template
from templateframework.metadata import Metadata
import subprocess
import json
import os

def put_appsettings(target_path: str, log_level: str, file_name: str):
        os.chdir(target_path)
        print(f'Setting {file_name}...')

        with open(file=file_name, encoding='utf-8-sig', mode='r+') as appsettings_json_file:
            appsettings_json_content = json.load(appsettings_json_file)
            appsettings_json_content.update({
                                                "LogOptions": {
                                                    "LogLevel": f"{log_level}"
                                                } 
                                            })                                         
            appsettings_json_file.seek(0)
            json.dump(appsettings_json_content, appsettings_json_file, indent=2)
        print(f'Setting {file_name} done.')   

class Plugin(Template):
    def post_hook(self, metadata: Metadata):
        project_name = metadata.global_inputs['project_name']
        log_level = metadata.inputs['log_level']
        using = f"using StackSpot.Logging;"
        service = f"services.AddLogger(configuration)"
        
        put_appsettings(f'{metadata.target_path}/src/{project_name}.Api/', log_level, 'appsettings.json')
        put_appsettings(f'{metadata.target_path}/src/{project_name}.Api/', log_level, 'appsettings.Development.json')   
        put_appsettings(f'{metadata.target_path}/tests/{project_name}.Api.IntegrationTests/', log_level, 'appsettings.json')

        os.chdir(f'{metadata.target_path}/src/{project_name}.Application/')
        subprocess.run(['dotnet', 'add', 'package', 'StackSpot.Logging'])

        if 'OpenTracing' in metadata.inputs['log_extension']:
            subprocess.run(['dotnet', 'add', 'package', 'StackSpot.Logging.OpenTracing'])
            using = f"{using}using StackSpot.Logging.OpenTracing;"
            service = f"{service}.WithOpenTracing()"
       
        if 'XRay' in metadata.inputs['log_extension']:
            subprocess.run(['dotnet', 'add', 'package', 'StackSpot.Logging.XRay'])             
            using = f"{using}using StackSpot.Logging.XRay;"
            service = f"{service}.WithXRayTraceId()"

        if 'CorrelationId' in metadata.inputs['log_extension']:
            subprocess.run(['dotnet', 'add', 'package', 'StackSpot.Logging.Correlation'])  
            using = f"{using}using StackSpot.Logging.Correlation;" 
            service = f"{service}.WithCorrelation()" 
        
        print('Setting Configuration...')

        os.chdir(f'{metadata.target_path}/src/{project_name}.Application/Common/StackSpot/')
        configuration_file = open(file='DependencyInjection.cs', mode='r')
        content = configuration_file.readlines()
        index_using = [x for x in range(len(content)) if 'using' in content[x].lower()]
        index = [x for x in range(len(content)) if 'return services' in content[x].lower()]
        content[index_using[0]] = f"{using}\n{content[index_using[0]]}"
        content[index[0]] = f"{service};\n{content[index[0]]}"
        
        configuration_file = open(file='DependencyInjection.cs', mode='w')                     
        configuration_file.writelines(content)
        configuration_file.close()

        print('Setting Configuration done.') 

        print('Apply dotnet format...')
        os.chdir(f'{metadata.target_path}/')
        subprocess.run(['dotnet', 'dotnet-format', f'src/{project_name}.Application/{project_name}.Application.csproj', '--include-generated'])   
        print('Apply dotnet format done...')

if __name__ == '__main__':
    run(Plugin())