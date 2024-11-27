from src.Query import Query


def main():
    query_input = input("Enter a query: ")
    rule_to_print = Query(query_input).parse_to_rule()
    print(rule_to_print)

if __name__ == "__main__":
    main()