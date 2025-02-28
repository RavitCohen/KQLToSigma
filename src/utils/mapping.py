from config.fields import kql_field_mapping
from config.products import kql_product_mapping
from config.services import kql_service_mapping


#-----------------------Mapping Functions---------------------#
#TODO: what description more suitable: map or handle?
def map_projects(projects: list) -> list:
    fields = set()

    for project in projects:
        column = kql_field_mapping.get(project, None)
        if column is None:
            raise ValueError(f'ERROR: column : {project} does not exist.')
        fields.add(column)

    return list(fields)


def map_log_source(data_source):
    products = set()
    services = set()

    for num in data_source:

        collected_products = {kql_product_mapping[num]} if num in kql_product_mapping else set()

        if num in kql_service_mapping:
            value = kql_service_mapping[num]
            collected_services = set(value) if isinstance(value, list) else {value}
        else:
            collected_services = set()

        if not collected_products and not collected_services:
            print(f"ERROR: the number {num} did not match any key in either mapping!")  #TODO: should be an error?
            break

        products = products.union(collected_products)
        services = services.union(collected_services)
    return list(products), list(services)


def map_field(data):
    if isinstance(data, dict):
        return {key: map_field(value) if key == 'operands' else value
                for key, value in data.items()}
    elif isinstance(data, list):
        return [map_field(item) for item in data]
    elif isinstance(data, tuple):
        if data[0] in kql_field_mapping:
            return kql_field_mapping[data[0]], *data[1:]
    return data



# def map_field(self, detection):
#         for t in detection["operands"]:
#             if type(t) is tuple:
#                 detection["operands"].append((kql_field_mapping.get(t[0], t[0]), t[1], t[2]))
#             else:
#                 self.map_field(t)
#         return detection