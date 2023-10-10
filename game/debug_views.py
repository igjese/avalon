from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import yaml
import re

from .models import Resource, ShipSystem, SubSystem, Component, InstalledComponent, StorageType, StorageUnit, InstalledStorageUnit, StoredResource, World
from .game_logging  import parse_logs # Import the new game_logging file

def debug_page(request):
    return render(request,'game/debug.html')

def get_logs(request):
    log_data = parse_logs()
    return JsonResponse({'data': log_data})


def export_data(request):
    # Get config data
    storage_types = list(StorageType.objects.all().values('name', 'info'))
    resources = list(Resource.objects.all().values('name','storage_type__name', 'info'))
    storage_units = list(StorageUnit.objects.all().values('name', 'capacity','storage_type__name', 'info'))
    components = list(Component.objects.all().values('name', 'ticks_per_cycle', 'consumes', 'produces', 'info'))
    
    # Get ship data
    systems = ShipSystem.objects.all()
    systems_data = []
    
    for system in systems:
        subsystems = system.subsystems.all()
        subsystems_data = []
        
        for subsystem in subsystems:
            installed_storage_units = subsystem.installed_storage_units.all()
            installed_components = subsystem.components.all()

            subsystems_data.append({
                'name': subsystem.name,
                'InstalledComponents': list(installed_components.values('id','component__name')),
                'InstalledStorageUnits': list(installed_storage_units.values('id','storage_unit__name', 'assigned_resource__name')),  
            })

        systems_data.append({
            'name': system.name,
            'SubSystems': subsystems_data
        })

    all_data = {
        'ShipSystems': systems_data,
        'StorageType': storage_types,
        'Resource': resources,
        'StorageUnit': storage_units,
        'Component': components
    }

    yaml_data = yaml.dump(all_data, default_flow_style=False, sort_keys=False)
    # Add empty lines between tables for better readability
    yaml_data = re.sub(r'^(?=\S)(?![\-])', r'\n', yaml_data, flags=re.MULTILINE)

    return HttpResponse(yaml_data, content_type="application/x-yaml")

@transaction.atomic
def import_data(request):
    yaml_data = request.POST.get('yaml_data')  # Assuming you send YAML data as a POST parameter
    data = yaml.safe_load(yaml_data)
    
    for item in data['StorageType']:
        name = item.get('name')
        info = item.get('info')
        
        # Update or create new record
        StorageType.objects.update_or_create(
            name=name,
            defaults={'info': info}
        )

    for item in data['Resource']:
        name = item.get('name')
        storage_type_name = item.get('storage_type__name')
        info = item.get('info')

        # Look up the StorageType by name
        try:
            storage_type = StorageType.objects.get(name=storage_type_name)
        except ObjectDoesNotExist:
            return HttpResponse(f"StorageType {storage_type_name} does not exist.")
        
        # Update or create new record
        Resource.objects.update_or_create(
            name=name,
            defaults={'storage_type': storage_type, 'info': info}
        )

    for item in data['StorageUnit']:
        name = item.get('name')
        capacity = item.get('capacity')
        storage_type_name = item.get('storage_type__name')
        info = item.get('info')

        # Look up the StorageType by name
        try:
            storage_type = StorageType.objects.get(name=storage_type_name)
        except ObjectDoesNotExist:
            return HttpResponse(f"StorageType {storage_type_name} does not exist.")
        
        # Update or create new record
        StorageUnit.objects.update_or_create(
            name=name,
            defaults={'capacity': capacity, 'storage_type': storage_type, 'info': info}
        )

    for item in data['Component']:
        name = item.get('name')
        ticks_per_cycle = item.get('ticks_per_cycle')
        info = item.get('info')

        # Update or create new record
        Component.objects.update_or_create(
            name=name,
            defaults={'ticks_per_cycle': ticks_per_cycle, 'info': info}
        )

    # Import ShipSystems
    # ShipSystems and SubSystems can have temporary IDs, since they can be referenced from InstalledComponents and InstalledStorageUnits
    temp_id_mapping = {}

    for system_data in data['ShipSystems']:
        temp_id = system_data.get('id', None)
        system_name = system_data['name']
        
        system, _ = ShipSystem.objects.update_or_create(
            name=system_name
        )
        
        if temp_id:
            temp_id_mapping[temp_id] = system.id  # Map the temporary ID to the actual ID

        for subsystem_data in system_data['SubSystems']:
            temp_id = subsystem_data.get('id', None)
            subsystem_name = subsystem_data['name']
            
            subsystem, _ = SubSystem.objects.update_or_create(
                name=subsystem_name,
                parent_system=system
            )
            
            if temp_id:
                temp_id_mapping[temp_id] = subsystem.id  # Map the temporary ID to the actual ID

            # Importing InstalledComponents
            for component_data in subsystem_data['InstalledComponents']:
                component_id = component_data.get('id', None)
                component_name = component_data['component__name']
                component = Component.objects.get(name=component_name)
                
                InstalledComponent.objects.update_or_create(
                    id=component_id,
                    defaults={
                        'component': component,
                        'parent_subsystem': subsystem
                    }
                )

            # Importing InstalledStorageUnits
            for storage_unit_data in subsystem_data['InstalledStorageUnits']:
                storage_unit_id = storage_unit_data.get('id', None)
                storage_unit_name = storage_unit_data['storage_unit__name']
                storage_unit = StorageUnit.objects.get(name=storage_unit_name)
                assigned_resource_name = storage_unit_data.get('assigned_resource__name', None)
                
                if assigned_resource_name:
                    assigned_resource = Resource.objects.get(name=assigned_resource_name)
                else:
                    assigned_resource = None
                
                InstalledStorageUnit.objects.update_or_create(
                    id=storage_unit_id,
                    defaults={
                        'storage_unit': storage_unit,
                        'subsystem': subsystem,
                        'assigned_resource': assigned_resource
                    }
                )

    return HttpResponse("Data Imported Successfully")
