from django.db import models

class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Sport(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='sports')  # 💡 link to Group

    def __str__(self):
        return f"{self.name} ({self.group.name})"



class Student(models.Model):
    name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=50, unique=True)
    father_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Boys'), ('Female', 'Girls')])
    image = models.ImageField(upload_to='students/')
    sports = models.CharField(max_length=200)  # comma-separated
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    chest_number = models.CharField(max_length=10, blank=True, null=True) 

    def __str__(self):
        return f"{self.name} ({self.id_number})"

