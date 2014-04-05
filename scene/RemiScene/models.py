from django.db import models
from django.db.models.signals import *
from django.contrib.auth.models import User

# initial push version
class Location(models.Model):
    longitude = models.IntegerField()
    latitude = models.IntegerField()
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=240)

class Scene(models.Model):
    title = models.CharField(max_length=240)
    description = models.TextField()
    occur_time = models.DateTimeField()
    image_loc = models.CharField(max_length=240)
    happy = 'h'
    date = 'd'
    party = 'p'
    tag = (
        (happy, 'happy'),
        (date, 'date'),
        (party, 'party'),
            )
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return self.title

    
class PersonScene(models.Model):
    essay = models.TextField()
    video_loc = models.CharField(max_length=240)
    music_loc = models.CharField(max_length=240)
    photo_loc = models.CharField(max_length=240)
    scene = models.ForeignKey(Scene)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.username+" in "+self.scene.title

    @staticmethod
    def get_personScenes_from_scene(this_scene):
        return PersonScene.objects.filter(scene=this_scene)

class Comment(models.Model):
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    person_scene = models.ForeignKey(PersonScene)
    def __unicode__(self):
        return self.content

class Privilege(models.Model):
    user = models.ForeignKey(User)
    scene = models.ForeignKey(Scene)
    level = models.IntegerField()

class Friends(models.Model):
    user = models.ForeignKey(User, related_name='user')
    friends = models.ManyToManyField(User, related_name='friends')
   
    @staticmethod
    def get_friends(user):
        return Friends.objects.filter(user=user)

class Message(models.Model):
    create_time = models.DateTimeField()
    content = models.TextField()
    from_user = models.ForeignKey(User, related_name='fromWho')
    to_user = models.ForeignKey(User, related_name='toWho')
    def __unicode__(self):
        return self.content

    @staticmethod
    def get_messages(user):
        return Message.objects.filter(to_user=user).order_by('-create_time')
'''
class Profile(models.Model):
    user = models.ForeignKey(User,unique=True)
    id_photo_id = models.CharField(max_length=50)
    bg_pic_id = models.CharField(max_length=50)
    music_id = models.CharField(max_length=50)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
'''
