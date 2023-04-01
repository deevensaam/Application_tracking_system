# Generated by Django 4.1.7 on 2023-03-31 08:51

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Recruiter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[("objects", django.contrib.auth.models.UserManager()),],
        ),
        migrations.CreateModel(
            name="Candidate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "firstname",
                    models.CharField(max_length=50, verbose_name="First name"),
                ),
                (
                    "lastname",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Last name"
                    ),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="Email id")),
                (
                    "phonenumber",
                    models.IntegerField(null=True, verbose_name="Phone number"),
                ),
                (
                    "designation",
                    models.CharField(
                        max_length=15, null=True, verbose_name="Designation"
                    ),
                ),
                (
                    "currentctc",
                    models.IntegerField(null=True, verbose_name="Current ctc"),
                ),
                (
                    "expectedctc",
                    models.IntegerField(null=True, verbose_name="Expected ctc"),
                ),
                ("skypeid", models.URLField(null=True, verbose_name="Skype id")),
                (
                    "linkedin_url",
                    models.URLField(null=True, verbose_name="Linkedin_url"),
                ),
                ("Github_url", models.URLField(null=True, verbose_name="Github_url")),
                (
                    "portfolio_url",
                    models.URLField(null=True, verbose_name="Portfolio_url"),
                ),
                (
                    "resume",
                    models.FileField(upload_to="uploads/", verbose_name="Resume/CV"),
                ),
                (
                    "street",
                    models.CharField(max_length=15, null=True, verbose_name="Street"),
                ),
                (
                    "landmark",
                    models.CharField(max_length=50, null=True, verbose_name="Landmark"),
                ),
                ("pincode", models.IntegerField(null=True, verbose_name="Pincode")),
                (
                    "city",
                    models.CharField(max_length=20, null=True, verbose_name="City"),
                ),
                (
                    "state",
                    models.CharField(max_length=20, null=True, verbose_name="State"),
                ),
                ("exp", models.IntegerField(null=True, verbose_name="Years Exp")),
                ("event_time", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "stage",
                    models.CharField(
                        choices=[
                            ("screening", "screening"),
                            ("telephone", "telephone"),
                            ("coding", "coding"),
                            ("F2F", "F2F"),
                            ("Make offer", "Make offer"),
                            ("selected", "selected"),
                        ],
                        default="screening",
                        max_length=25,
                        null=True,
                        verbose_name="Stage",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("role", models.CharField(max_length=25)),
                (
                    "jobtype",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Full Time", "Full Time"),
                            ("Part Time", "Part Time"),
                            ("Internship", "Internship"),
                            ("Remote", "Remote"),
                        ],
                        default="Full time",
                        max_length=15,
                    ),
                ),
                ("salary", models.IntegerField(default=0)),
                (
                    "select_template",
                    models.CharField(
                        choices=[
                            ("01", "01"),
                            ("02", "02"),
                            ("03", "03"),
                            ("04", "04"),
                        ],
                        default="01",
                        max_length=20,
                    ),
                ),
                (
                    "experience_min",
                    models.CharField(
                        choices=[
                            ("0", "0"),
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                            ("5", "5"),
                            ("6", "6"),
                        ],
                        default="1",
                        max_length=2,
                    ),
                ),
                (
                    "experience_max",
                    models.CharField(
                        choices=[
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4", "4"),
                            ("5", "5"),
                            ("6", "6"),
                        ],
                        default="1",
                        max_length=2,
                    ),
                ),
                ("description", models.TextField(max_length=300)),
                ("requirements", models.TextField(max_length=300)),
                ("about_company", models.TextField(max_length=300)),
                ("event_time", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="JobApplication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("feedback_note", models.CharField(max_length=200)),
                ("user_note", models.CharField(max_length=200)),
                (
                    "status",
                    models.CharField(
                        choices=[("ACCEPTED", "accepted"), ("REJECTED", "rejected")],
                        max_length=20,
                    ),
                ),
                (
                    "applied_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.candidate"
                    ),
                ),
                (
                    "jobId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.job"
                    ),
                ),
            ],
        ),
    ]
