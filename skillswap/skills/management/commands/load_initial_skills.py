from django.core.management.base import BaseCommand
from skills.models import Skill

class Command(BaseCommand):
    help = 'Loads initial skills into the database'

    def handle(self, *args, **kwargs):
        skills = [
            {'name': 'Python Programming', 'description': 'Python programming language skills'},
            {'name': 'Web Development', 'description': 'Building websites and web applications'},
            {'name': 'Graphic Design', 'description': 'Creating visual content and designs'},
            {'name': 'Photography', 'description': 'Taking and editing photographs'},
            {'name': 'Cooking', 'description': 'Preparing and cooking food'},
            {'name': 'Music', 'description': 'Playing musical instruments or singing'},
            {'name': 'Language Teaching', 'description': 'Teaching foreign languages'},
            {'name': 'Fitness Training', 'description': 'Personal fitness and exercise training'},
            {'name': 'Writing', 'description': 'Creative and technical writing'},
            {'name': 'Video Editing', 'description': 'Editing and producing video content'},
        ]

        for skill_data in skills:
            skill, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults={'description': skill_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created skill: {skill.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skill already exists: {skill.name}')) 