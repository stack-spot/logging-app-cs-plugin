from templateframework.runner import run
from templateframework.template import Template
from templateframework.metadata import Metadata
import subprocess
import json
import os

def put_appsettings(project_name: str, target_path: str, file_name: str):
        os.chdir(f'{target_path}/src/{project_name}.Api/')
        print(f'Setting {file_name}...')

        with open(file=file_name, encoding='utf-8-sig', mode='r+') as appsettings_json_file:
            appsettings_json_content = json.load(appsettings_json_file)
            appsettings_json_content.update({
                                                "LogOptions": {
                                                    "LogLevel": "inputs.log_level"
                                                } 
                                            })                                         
            appsettings_json_file.seek(0)
            json.dump(appsettings_json_content, appsettings_json_file, indent=2)
        print(f'Setting {file_name} done.')   

class Plugin(Template):
    def post_hook(self, metadata: Metadata):
        project_name = metadata.global_inputs['project_name']
        using = f"using StackSpot.Logging;\n"
        service = f"services.AddLogger(configuration)\n"
        
        put_appsettings(project_name, metadata.target_path, 'appsettings.json')
        put_appsettings(project_name, metadata.target_path, 'appsettings.Development.json')   

        os.chdir(f'{metadata.target_path}/src/{project_name}.Domain/')
        subprocess.run(['dotnet', 'add', 'package', 'StackSpot.Logging'])

        if 'OpenTracing' in metadata.inputs['log_extension']:
            subprocess.run(['dotnet', 'add', 'package', 'StackSpot.Logging.OpenTracing'])
            using = f"{using}using StackSpot.Logging.OpenTracing;\n"
            service = f"{service}.WithOpenTracing()\n"
       
        if 'XRay' in metadata.inputs['log_extension']:
            subprocess.run(['dotnet', 'add', 'package', 'StackSpot.Logging.XRay'])             
            using = f"{using}\nusing StackSpot.Logging.XRay;\n"
            service = f"{service}.WithXRayTraceId()\n"

        if 'CorrelationId' in metadata.inputs['log_extension']:
            subprocess.run(['dotnet', 'add', 'package', 'StackSpot.Logging.Correlation'])  
            using = f"{using}\nusing StackSpot.Logging.Correlation;\n" 
            service = f"{service}.WithCorrelation()\n" 
        
        print('Setting Configuration...')

        os.chdir(f'{metadata.target_path}/src/{project_name}.Api/')
        configuration_file = open(file='ConfigurationStackSpot.cs', mode='r')
        content = configuration_file.readlines()
        index = [x for x in range(len(content)) if 'return services' in content[x].lower()]
        content[0] = using+content[0]
        content[index[0]] = f"{service};\n{content[index[0]]}"
        
        configuration_file = open(file='ConfigurationStackSpot.cs', mode='w')                     
        configuration_file.writelines(content)
        configuration_file.close()

        print('Setting Configuration done.')    

if __name__ == '__main__':
    run(Plugin())