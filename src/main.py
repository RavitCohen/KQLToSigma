from src.Query import Query
import re


def main():
    query_input = input("Enter a query: ")
    query_input.replace("\n", "")
    re.sub(r"\s+", " ", query_input).strip()
    rule_to_print = Query(query_input).parse_to_rule()
    print(rule_to_print)

if __name__ == "__main__":
    main()