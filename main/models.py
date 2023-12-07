from django.db import models
# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=50)
    rahbar = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return str(self.name) 
    


class Worker(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=70)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="workers")


    def __str__(self):
        return str(f'{self.last_name} {self.first_name}')

class Attendance(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField()#auto_now_add=True)

    def __str__(self):
        return f"{str(self.team.name)} jamoasining {str(self.date)} sanadagi davomadi."
    


class Mark(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='marks')
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="marks")
    dt = models.DateField(auto_now_add=True,null=True,blank=True)
    s = "ko`k"
    db = "yashil"
    dy = "qizil"
    the_price=(
        (s,"ko`k"),
        (db,"yashil"),
        (dy,"qizil"),
    )
    is_attended = models.CharField(choices=the_price,max_length=500,default='yashil')
    
    class Meta:
        unique_together = ['attendance', 'worker']