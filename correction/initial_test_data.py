import os
import re

from django.contrib.auth.models import User

from correction.models import Correction, QuestionTypeData

user = User.objects.create_user(username="admin", email="admin@admin.com", password="password")

toefl_integrated_tpo_64_file = open("correction/test_data/toefl_integrated_tpo_64.txt")
toefl_integrated_tpo_64 = toefl_integrated_tpo_64_file.read()
toefl_integrated_tpo_64_file.close()

toefl_integrated_tpo_73_file = open("correction/test_data/toefl_integrated_tpo_73.txt")
toefl_integrated_tpo_73 = toefl_integrated_tpo_73_file.read()
toefl_integrated_tpo_73_file.close()

dummy_text_file = open("correction/test_data/dummy.txt")
dummy_text = dummy_text_file.read()
dummy_text_file.close()

# Same question type data
correction1 = Correction.objects.create(
    question_type_data=QuestionTypeData.objects.get(type_name=QuestionTypeData.TYPE_CHOICES[0][0],
                                                    type_number=73),
    user=user,
    answer=toefl_integrated_tpo_73)
correction2 = Correction.objects.create(
    question_type_data=QuestionTypeData.objects.get(type_name=QuestionTypeData.TYPE_CHOICES[0][0],
                                                    type_number=64),
    user=user,
    answer=toefl_integrated_tpo_64)

# Different question type data
correction3 = Correction.objects.create(
    question_type_data=QuestionTypeData.objects.get(type_name=QuestionTypeData.TYPE_CHOICES[0][0],
                                                    type_number=70),
    user=user,
    answer=toefl_integrated_tpo_73)
correction4 = Correction.objects.create(
    question_type_data=QuestionTypeData.objects.get(type_name=QuestionTypeData.TYPE_CHOICES[0][0],
                                                    type_number=65),
    user=user,
    answer=toefl_integrated_tpo_64)

# Wrong text
correction5 = Correction.objects.create(
    question_type_data=QuestionTypeData.objects.get(type_name=QuestionTypeData.TYPE_CHOICES[0][0],
                                                    type_number=73),
    user=user,
    answer=dummy_text)
