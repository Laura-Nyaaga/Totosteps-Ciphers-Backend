from django.test import TestCase
from assessment.models import Assessment
from milestones.models import Milestone

class AssessmentTestCase(TestCase):

    def setUp(self):
        self.milestone = Milestone.objects.create(
            age=24,
            category='Cognitive',
            summary='Basic cognitive abilities'
        )
        
        self.assessment_data = {
            'milestone': self.milestone,
            'question': {"text": "Can the child count to 10?", "options": ["YES", "NO"]},  # JSON data structure
            'correct_answer': 'YES',
            'question_type': 'multiple choice',
            'category': 'Cognitive'
        }
        
        self.assessment = Assessment.objects.create(**self.assessment_data)

    def test_create_assessment(self):
        self.assertEqual(Assessment.objects.count(), 1)
        self.assertEqual(self.assessment.milestone, self.milestone)
        self.assertEqual(self.assessment.question["text"], "Can the child count to 10?")
        self.assertEqual(self.assessment.correct_answer, 'YES')

    def test_update_assessment(self):
        new_question = {"text": "Can the child identify colors?", "options": ["YES", "NO"]}
        self.assessment.question = new_question
        self.assessment.save()
        self.assertEqual(self.assessment.question["text"], "Can the child identify colors?")

    def test_update_non_existent_assessment(self):
        non_existent_id = 999
        updated_data = {
            'question': {"text": "Is the child able to speak in full sentences?", "options": ["YES", "NO"]},
            'correct_answer': 'YES',
            'question_type': 'open-ended',
            'category': 'Language'
        }
        with self.assertRaises(Assessment.DoesNotExist):
            Assessment.objects.get(pk=non_existent_id).update(**updated_data)
