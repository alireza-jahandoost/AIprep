import time
import os
from dbm import error

from django.core.management import BaseCommand
from openai import organization, OpenAI

from correction.models import Correction, QuestionTypeData
from subscriptions.helper_functions import get_current_plan_of_user
from subscriptions.models import Plan


class Command(BaseCommand):
    help = "Corrects corrections"
    client = None

    def make_prompt(self, correction):
        user_plan = get_current_plan_of_user(correction.user)
        if correction.question_type_data.exam_type == QuestionTypeData.EXAM_TYPE_TOEFL_TASK1:
            check_template = open("correction/data/prompt_templates/TOEFLIntegratedTemplateForEvaluation.txt")
            if user_plan.correction_type == Plan.CORRECTION_TYPE_NORMAL:
                main_template = open("correction/data/prompt_templates/TOEFLIntegratedTemplate.txt")
            elif user_plan.correction_type == Plan.CORRECTION_TYPE_PRO:
                main_template = open("correction/data/prompt_templates/TOEFLIntegratedTemplatePro.txt")
            else:
                raise "Not supported correction type (TOEFL TASK 1)"
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
            if user_plan.correction_type == Plan.CORRECTION_TYPE_NORMAL:
                main_template = open("correction/data/prompt_templates/TOEFLIndependentTemplate.txt")
            elif user_plan.correction_type == Plan.CORRECTION_TYPE_PRO:
                main_template = open("correction/data/prompt_templates/TOEFLIndependentTemplatePro.txt")
            else:
                raise "Not supported correction type (TOEFL TASK 2)"
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
        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
        )
        return response.choices[0].message.content


    def handle(self, *args, **options):
        # genai.configure(api_key=os.environ['GENAI_API_KEY'])
        request_limit = int(os.environ['MAX_NUMBER_OF_API_REQUESTS'])
        self.client = OpenAI(
            organization=os.environ['OPENAI_ORGANIZATION_ID'],
            project=os.environ['OPENAI_PROJECT_ID'],
            api_key=os.environ['OPENAI_API_KEY'],
        )
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
                request_limit -= 2
            else:
                current_correction.correction = check_output
                current_correction.status = Correction.STATUS_INVALID
                request_limit -= 1
            current_correction.save()

            if request_limit < 2 or iter >= len(not_corrected_corrections):
                break
