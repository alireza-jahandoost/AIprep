import os
import re

from correction.models import QuestionTypeData, QuestionType

TPO_DIR = "correction/data/TPO"
NEO_DIR = "correction/data/NEO"

# COMMAND:  python manage.py shell < correction/initial_data.py

print('start')

TOEFLIntegrated = QuestionType(name="TOEFL Integrated")
# TOEFLIndependent = QuestionType(name="TOEFL Independent")
TOEFLIntegrated.save()
# TOEFLIndependent.save()

for file in os.listdir(TPO_DIR):
    f = open(os.path.join(TPO_DIR, file), "r", encoding="utf-8")
    x = re.findall(r"\[(?P<section>\w+)]\n(?P<content>.*?)(?=\n\[|$)", f.read(), re.DOTALL)
    reading = x[0][1]
    listening = x[1][1]
    QuestionTypeData.objects.create(question_type=TOEFLIntegrated,
                                        type_name=QuestionTypeData.TYPE_CHOICES[0][0],
                                        type_number=file.split(".")[0],
                                        data={"reading": reading, "listening": listening})

for file in os.listdir(NEO_DIR):
    f = open(os.path.join(NEO_DIR, file), "r", encoding="utf-8")
    x = re.findall(r"\[(?P<section>\w+)]\n(?P<content>.*?)(?=\n\[|$)", f.read(), re.DOTALL)
    reading = x[0][1]
    listening = x[1][1]
    QuestionTypeData.objects.create(question_type=TOEFLIntegrated,
                                        type_name=QuestionTypeData.TYPE_CHOICES[1][0],
                                        type_number=file.split(".")[0],
                                        data={"reading": reading, "listening": listening})

print('end')