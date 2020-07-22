from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

JOURNALS_CHOICES = (
	('1', 'ACM Transactions on Privacy and Security (TOPS)'),
	('2', 'ACM Transactions on Information Systems (TOIS)'),
	('3', 'ACM Transactions on Management Information Systems'),
	('4', 'Business & Information Systems Engineering'),
	('5', 'Business Research'),
	('6', 'Business Strategy and the Environment'),
	('7', 'CIO'),
	('8', 'Computerwoche'),
	('9', 'Decision Sciences'),
	('10', 'DuD - Datenschutz und Datensicherheit'),
	('11', 'Electronic Markets'),
	('12', 'HMD Praxis der Wirtschaftsinformatik'),
	('13', 'IEEE Transactions on Engineering Management'),
	('14', 'Information Systems Journal'),
	('15', 'Journal of Business Economics'),
	('16', 'Management Science'),
	('17', 'Wirtschaftsinformatik & Management'),
	('18', 'Information Systems Research'),
	('19', 'Journal of Information Technology Theory and Application (JITTA)'),
	('20', 'Journal of the Association for Information Systems'),
	('21', 'Communications of the AIS'),
	('22', 'MIS Quarterly Executive'),
)

class Journal(models.Model):
	name = models.CharField(max_length=100)
	link = models.CharField(max_length=100)
	issue = models.CharField(max_length=20, blank=True)
	issOld = models.CharField(max_length=50, blank=True)
	date_latest_issue = models.CharField(max_length=100, blank=True)
	crawlable = models.IntegerField()

	def __str__(self):
		return f'{self.name}'


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	description = models.CharField(max_length=100, default='', blank=True, null=True)
	not_interested = models.ManyToManyField(Journal, blank=True)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, **kwargs):
		super().save(**kwargs)




def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)