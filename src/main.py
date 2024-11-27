from parso.normalizer import Rule
from src.Query import Query

def main():
    query = input("Enter a query: ")
    query_to_parse = Query(query)

    # Handle all query components
    project_after_mapped = query_to_parse.handle_project()
    logsource_after_mapped = query_to_parse.handle_logsource()
    fields_after_mapped = query_to_parse.handle_fields()

    # Create sigma rule
    #TODO: rule_to_print = Sigma_rule(project_after_mapped, logsource_after_mapped, fields_after_mapped)

    # Print sigma rule
    #TODO: rule_to_print.print_rule()
















if __name__ == "__main__":
    main()