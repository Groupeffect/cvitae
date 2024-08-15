from django.core import exceptions
import logging

logger = logging.getLogger(__name__)


class PrefacePromptGenerator:
    def __init__(self, instance) -> None:
        self.instance = instance
        self.prefaces = self.instance.prefaces
        self.template = """\n"""

    def get_many(self, key="jobpostings__document", meta="SYSTEM CONTEXT JOBPOSTING"):
        """return list of items from many to many fields"""
        result = []
        for i in enumerate(self.prefaces.values_list(key, flat=True)):
            if i[1]:
                result.append(f"""\n{meta}  ITEM NUMBER {i[0]}:\n{i[1]}\n""")
        return result

    def write_template(self):
        """keep the alignment(linebreaks between multiline stings)
        of this method to create clean template with python"""
        logger.warning(self.prefaces.values(*self.instance.preface_fields))
        content = []
        for field in self.instance.preface_fields:
            is_nested = False
            for i in ["text", "description"]:
                try:
                    content += self.get_many(
                        key=f"{field}__{i}",
                        meta=f"SYSTEM CONTEXT {field}".upper(),
                    )
                    is_nested = True
                except exceptions.FieldError as e:
                    logger.warning(["##### E000", type(e), e])
                    pass

            if not is_nested:
                try:

                    content += list(self.prefaces.values_list(field, flat=True))
                    logger.warning(content)
                except exceptions.FieldError as e:
                    logger.warning(["##### E001", type(e), e])
                    pass

        for i in content:
            self.template += str(i)
        self.template += f"""\nUSER:\n{self.instance.prompt}\n"""
        self.instance.template = self.template
        return self.instance
