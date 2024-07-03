import time
import os

import google.generativeai as genai
from django.core.management import BaseCommand

from correction.models import Correction, QuestionTypeData


class Command(BaseCommand):
    help = "Corrects corrections"

    def make_prompt(self, correction):
        if correction.question_type_data.exam_type == QuestionTypeData.EXAM_TYPE_TOEFL_TASK1:
            check_template = open("correction/data/prompt_templates/TOEFLIntegratedTemplateForEvaluation.txt")
            main_template = open("correction/data/prompt_templates/TOEFLIntegratedTemplate.txt")

            check_template_text = check_template.read()
            main_template_text = main_template.read()

            check_template.close()
            main_template.close()

            check_template_text = ((check_template_text
                                    .replace("[READING]", correction.question_type_data.data['reading']))
                                   .replace("[MAIN TEXT]", correction.answer))
            main_template_text = (main_template_text
                                  .replace("[LISTENING]", correction.question_type_data.data['listening'])
                                  .replace("[READING]", correction.question_type_data.data['reading'])
                                  .replace("[MAIN TEXT]", correction.answer))

            return check_template_text, main_template_text
        elif correction.question_type_data.exam_type == QuestionTypeData.EXAM_TYPE_TOEFL_TASK2:
            check_template = open("correction/data/prompt_templates/TOEFLIndependentTemplateForEvaluation.txt")
            main_template = open("correction/data/prompt_templates/TOEFLIndependentTemplate.txt")

            check_template_text = check_template.read()
            main_template_text = main_template.read()

            check_template.close()
            main_template.close()

            check_template_text = ((check_template_text
                                    .replace("[READING]", correction.question_type_data.data['reading']))
                                   .replace("[MAIN TEXT]", correction.answer))
            main_template_text = (main_template_text
                                  .replace("[READING]", correction.question_type_data.data['reading'])
                                  .replace("[MAIN TEXT]", correction.answer))

            return check_template_text, main_template_text
        else:
            Exception("(prompt_name) is not a valid prompt name")

    def call_api(self, prompt):
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model.generate_content(prompt).text


    def handle(self, *args, **options):
        genai.configure(api_key=os.environ['GENAI_API_KEY'])
        request_limit = int(os.environ['MAX_NUMBER_OF_API_REQUESTS'])
        not_corrected_corrections = list(Correction.objects.filter(status=Correction.STATUS_PENDING).order_by(
            'created_at'))

        if len(not_corrected_corrections) == 0:
            return

        t_end = time.time() + 50
        iter = 0

        while time.time() < t_end:
            current_correction = not_corrected_corrections[iter]
            iter = iter + 1

            check_prompt, main_prompt = self.make_prompt(current_correction)

            check_output = self.call_api(check_prompt)

            if "yes" in check_output.lower():
                correction = self.call_api(main_prompt)
                current_correction.correction = correction
                current_correction.status = Correction.STATUS_CORRECTED
            else:
                current_correction.correction = check_output
                current_correction.status = Correction.STATUS_INVALID
            current_correction.save()
            request_limit -= 2

            if request_limit < 2 or iter >= len(not_corrected_corrections):
                break
