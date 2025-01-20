from src.Query import Query
import re
import yaml


def main():
    query_input = input("Enter a query: ")
    rule_to_print = Query(query_input).parse_to_rule()
    print(rule_to_print)
    print(yaml.dump(rule_to_print, default_flow_style=False))

if __name__ == "__main__":
    main()

