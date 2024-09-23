import os
import re

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from correction.models import Correction, QuestionTypeData

class Command(BaseCommand):
    help = "Makes some test data"

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            user = User.objects.filter(username='admin').get()
        else:
            user = User.objects.create_user(username="admin", email="admin@admin.com", password="password")

        toefl_integrated_tpo_64_file = open("correction/data/test_data/toefl_integrated_tpo_64.txt")
        toefl_integrated_tpo_64 = toefl_integrated_tpo_64_file.read()
        toefl_integrated_tpo_64_file.close()

        toefl_integrated_tpo_73_file = open("correction/data/test_data/toefl_integrated_tpo_73.txt")
        toefl_integrated_tpo_73 = toefl_integrated_tpo_73_file.read()
        toefl_integrated_tpo_73_file.close()

        toefl_independent_neo_1_file = open('correction/data/test_data/toefl_independent_neo_1.txt')
        toefl_independent_neo_1 = toefl_independent_neo_1_file.read()
        toefl_independent_neo_1_file.close()

        dummy_text_file = open("correction/data/test_data/dummy.txt")
        dummy_text = dummy_text_file.read()
        dummy_text_file.close()

        # Same question type data
        correction1 = Correction.objects.create(
            question_type_data=QuestionTypeData.objects.get(exam_db_name=QuestionTypeData.EXAM_DB_TPO,
                                                            exam_db_number=73,
                                                            exam_type=QuestionTypeData.EXAM_TYPE_TOEFL_TASK1),
            user=user,
            answer=toefl_integrated_tpo_73)
        correction2 = Correction.objects.create(
            question_type_data=QuestionTypeData.objects.get(exam_db_name=QuestionTypeData.EXAM_DB_TPO,
                                                            exam_db_number=64,
                                                            exam_type=QuestionTypeData.EXAM_TYPE_TOEFL_TASK1),
            user=user,
            answer=toefl_integrated_tpo_64)

        correction3 = Correction.objects.create(
            question_type_data=QuestionTypeData.objects.get(exam_db_name=QuestionTypeData.EXAM_DB_NEO,
                                                            exam_db_number=1,
                                                            exam_type=QuestionTypeData.EXAM_TYPE_TOEFL_TASK2),
            user=user,
            answer=toefl_independent_neo_1)

        # Different question type data
        correction4 = Correction.objects.create(
            question_type_data=QuestionTypeData.objects.get(exam_db_name=QuestionTypeData.EXAM_DB_TPO,
                                                            exam_db_number=70,
                                                            exam_type=QuestionTypeData.EXAM_TYPE_TOEFL_TASK1),
            user=user,
            answer=toefl_integrated_tpo_73)
        correction5 = Correction.objects.create(
            question_type_data=QuestionTypeData.objects.get(exam_db_name=QuestionTypeData.EXAM_DB_TPO,
                                                            exam_db_number=65,
                                                            exam_type=QuestionTypeData.EXAM_TYPE_TOEFL_TASK1),
            user=user,
            answer=toefl_integrated_tpo_64)

        correction6 = Correction.objects.create(
            question_type_data=QuestionTypeData.objects.get(exam_db_name=QuestionTypeData.EXAM_DB_NEO,
                                                            exam_db_number=5,
                                                            exam_type=QuestionTypeData.EXAM_TYPE_TOEFL_TASK2),
            user=user,
            answer=toefl_independent_neo_1)

        # Wrong text
        correction7 = Correction.objects.create(
            question_type_data=QuestionTypeData.objects.get(exam_db_name=QuestionTypeData.EXAM_DB_TPO,
                                                            exam_db_number=73,
                                                            exam_type=QuestionTypeData.EXAM_TYPE_TOEFL_TASK1),
            user=user,
            answer=dummy_text)
