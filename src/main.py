import yaml
from src.KQL import KQL
from src.SigmaRuleGenerator import SigmaRuleGenerator


def main():
    query_input = input("Enter a query: ")
    parsed_query = KQL.parse(query_input)
    rule_generator = SigmaRuleGenerator()
    rule = rule_generator.from_query(parsed_query)
    print(rule)
    print(yaml.dump(rule, default_flow_style=False))

if __name__ == "__main__":
    main()

