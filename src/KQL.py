import re
from dataclasses import dataclass
from src.utils.helper import clean_unnecessary_data, build_fields_dict


@dataclass
class KQL:

    table : str
    projects: list
    data_sources: list
    fields: str

    @classmethod
    def parse(cls, query: str) -> "KQL":
        """
        Generate a query object from query string.
        """

        table = cls.extract_table(query)
        projects = cls.extract_project(query)
        data_sources = cls.extract_data_source(query)
        fields = cls.extract_field(query)
        return cls(
            table=table,
            projects=projects,
            data_sources=data_sources,
            fields=fields
        )

    @classmethod
    def extract_table(cls, query) -> str:  #TODO: do we need to make sure table == "events_all"?
        match = re.match(r"^(\S+)\s*\r?\n?\|", query)
        if match:
            return match.group(1)
        else : raise ValueError("Illegal input: Expected a table.")

    @classmethod
    def extract_project(cls, query) -> list:
        matches = re.findall(r"(?<=\|)\s*project\s+([^\|]+)", query)
        projects = []

        for match in matches:
            columns = [column.strip() for column in match.split(',')]
            # if "" in col_to_check:
            #     raise ValueError("Illegal input: Expected a project.")  TODO: (shira) to my opinion these line are not necessary
            projects.extend(columns)                                     #TODO:  (QUESTION) is it ok to have multiple columns with same names?(legal)

        return projects

    @classmethod
    def extract_data_source(cls, query) -> list:
        pattern = r"data_source_type_id\s*==\s*(\d+)|data_source_type_id\s+in\s*\(\s*(\d+(?:\s*,\s*\d+)*)\s*\)"
        matches = re.findall(pattern, query)
        numbers = []

        for match in matches:
            if match[0]:
                numbers.append(int(match[0]))
            if match[1]:
                numbers.extend(map(int, match[1].split(',')))

        return numbers

    @classmethod
    def extract_field(cls, query) -> str:
        fields = clean_unnecessary_data(query)
        fields = build_fields_dict(fields)
        return fields
