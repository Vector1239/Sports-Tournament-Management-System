from django.db import models

# Create your models here.

class userg(models.Model):
	userg_id = models.BigAutoField(primary_key=True)
	userg_nam = models.CharField(max_length=50,null=True,unique=True) 
	userg_email = models.CharField(max_length=50,null=True,unique=True) 
	def __str__(self):
		return str(self.userg_nam)

class Tournament(models.Model):
	tourney_id=models.BigAutoField(primary_key=True)
	user_t=models.ForeignKey(userg,on_delete=models.CASCADE)
	tourney_nam = models.CharField(max_length=50,null=True,unique=False)
	tourney_org = models.CharField(max_length=50,null=True,unique=False)
	date_created = models.DateField(null=True) 
	date_ended = models.DateField(null=True)
	# null=True, blank=True

	def __str__(self):
		return str(self.tourney_id)

class Event(models.Model):
	eve_id=models.BigAutoField(primary_key=True)
	tour_n=models.ForeignKey(Tournament,on_delete=models.CASCADE)
	eve_nam = models.CharField(max_length=50,null=True,unique=False)
	eve_sport = models.CharField(max_length=50,null=True,unique=False)
	eve_no_teams = models.IntegerField(null=True,unique=False)
	eve_date = models.DateField(null=True)
	eve_info = models.TextField(null=True,unique=False)
	eve_venue = models.CharField(max_length=50,null=True,unique=False)
	eve_mode = models.CharField(max_length=50,null=True,unique=False)
# tour_n=models.ForeignKey(Tournament,on_delete=models.CASCADE)  
	# tour_n=models.ForeignKey(Tournament,on_delete=models.CASCADE)  

	def __str__(self):
		return str(self.eve_id)

class Team(models.Model):
	tem_id = models.BigAutoField(primary_key=True)
	tem_name = models.CharField(max_length=50,null=True,unique=False)
	tem_pos= models.IntegerField(null=True,unique=False)
	tem_Round= models.IntegerField(null=True,unique=False)
	eve_n=models.ForeignKey(Event,on_delete=models.CASCADE) 

	def __str__(self):
		return str(self.tem_name)

class Bracket(models.Model):
	brac_id = models.BigAutoField(primary_key=True)
	brac_roun= models.IntegerField(null=True,unique=False)
	brac_sec= models.IntegerField(null=True,unique=False)
	breve_n=models.ForeignKey(Event,on_delete=models.CASCADE) 

	def __str__(self):
		return str(self.brac_id)

class Match(models.Model):
	mat_id = models.BigAutoField(primary_key=True)
	eve_n=models.ForeignKey(Event,on_delete=models.CASCADE) 
	tem_id_a=models.IntegerField(null=True,unique=False)
	tem_id_b=models.IntegerField(null=True,unique=False)
	score_a= models.IntegerField(null=True,unique=False)
	score_b= models.IntegerField(null=True,unique=False)
	mat_winner=models.IntegerField(null=True,unique=False)
	mat_round=models.IntegerField(null=True,unique=False)


	def __str__(self):
		return str(self.mat_id)