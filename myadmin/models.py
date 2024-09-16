from django.db import models

class State(models.Model):
	state_name=models.CharField(max_length=50)

	def __str__(self):
		return self.state_name

	class Meta:
		db_table="state"
            
class City(models.Model):
	city_name=models.CharField(max_length=50)
	state=models.ForeignKey(State,on_delete=models.CASCADE)

	def __str__(self):
		return self.city_name

	class Meta:
		db_table="city"
		
class Area(models.Model):
	area_name=models.CharField(max_length=50)
	city=models.ForeignKey(City,on_delete=models.CASCADE)
	state=models.ForeignKey(State,on_delete=models.CASCADE)

	def __str__(self):
		return self.area_name

	class Meta:
		db_table="area"

class Notice(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField()
	date = models.DateField()
	pdf = models.CharField(max_length=255)

	class Meta():
		db_table = 'notice'