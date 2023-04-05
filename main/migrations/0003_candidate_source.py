# Generated by Django 4.1.7 on 2023-04-04 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_rename_exp_candidate_experience_candidate_skills_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="source",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Linkedin", "Linkedin"),
                    ("Dribble", "Dribble"),
                    ("Self", "Self"),
                    ("Angellist", "Angellist"),
                    ("Career Page", "Career Page"),
                ],
                default="Full time",
                max_length=15,
            ),
        ),
    ]