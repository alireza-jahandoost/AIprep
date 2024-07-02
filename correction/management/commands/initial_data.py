import os
import re
import string
import sys

from django.core.management import BaseCommand

from correction.models import QuestionTypeData, QuestionType


class Command(BaseCommand):
    help = "Adds exams' data to the database."

    def handle(self, *args, **options):
        TPO_DIR = "correction/data/TPO"
        NEO_DIR = "correction/data/NEO"

        sys.stdout.write('start\n')
        sys.stdout.flush()
        TOEFLIntegrated = QuestionType(name="TOEFL Integrated")
        # TOEFLIndependent = QuestionType(name="TOEFL Independent")
        TOEFLIntegrated.save()
        # TOEFLIndependent.save()

        printable_chars = set(string.printable)

        for file in os.listdir(TPO_DIR):
            f = open(os.path.join(TPO_DIR, file), "r", encoding="utf-8")
            x = re.findall(r"\[(?P<section>\w+)]\n(?P<content>.*?)(?=\n\[|$)", f.read(), re.DOTALL)

            reading = ''.join(filter(lambda x: x in set(printable_chars), x[0][1]))
            listening = ''.join(filter(lambda x: x in set(printable_chars), x[1][1]))
            QuestionTypeData.objects.create(question_type=TOEFLIntegrated,
                                            type_name=QuestionTypeData.TYPE_CHOICES[0][0],
                                            type_number=file.split(".")[0],
                                            data={"reading": reading, "listening": listening})

        for file in os.listdir(NEO_DIR):
            f = open(os.path.join(NEO_DIR, file), "r", encoding="utf-8")
            x = re.findall(r"\[(?P<section>\w+)]\n(?P<content>.*?)(?=\n\[|$)", f.read(), re.DOTALL)
            reading = ''.join(filter(lambda x: x in set(printable_chars), x[0][1]))
            listening = ''.join(filter(lambda x: x in set(printable_chars), x[1][1]))
            QuestionTypeData.objects.create(question_type=TOEFLIntegrated,
                                            type_name=QuestionTypeData.TYPE_CHOICES[1][0],
                                            type_number=file.split(".")[0],
                                            data={"reading": reading, "listening": listening})

        sys.stdout.write('end\n')
