from django.db import models


class Class(models.Model):
    CLASS_SESSION_CHOICES = [
        ('current', 'Current'),
        ('previous', 'Previous'),
    ]

    classname = models.CharField(max_length=9)
    semester = models.PositiveIntegerField()
    excel_file = models.FileField(upload_to='static/class_files/')
    session = models.CharField(max_length=10, choices=CLASS_SESSION_CHOICES, default='current')

    def __str__(self):
        return f"{self.classname} - Semester {self.semester} - {self.get_session_display()}"
    def archive_class(self):
        if self.session == 'current':
            self.session = 'previous'
            self.save()