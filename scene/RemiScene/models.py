from django.db import models
from django.contrib.auth.models import User

# initial push version
class Scene(models.Model):
    scene_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=240)
    description = models.TextField()
    occur_time = models.DateTimeField()
    image_loc = models.CharField(max_length=240)
    tag = models.ForeignKey(Tag)
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return self.title
    
class PersonScene(models.Model):
    comment = models.ForeignKey(Comment)
    video_loc = models.CharField(max_length=240)
    music_loc = models.CharField(max_length=240)
    photo_loc = models.CharField(max_length=240)
    scene = models.ForeignKey(Scene)
    user = models.ForeighKey(User)
    def __unicode__(self):
        return self.user.username+" in "+self.scene.title

class Comment(models.Model):
    content = models.TextField()
    time = models.DateTimeField()
    person_scene = models.ForeignKey(PersonScene)
    def __unicode__(self):
        return self.content

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

class Location(models.Model):
    longitude = models.IntegerField()
    latitude = models.IntegerField()
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=240)

class Privilege(models.Model):
    user = models.ForeignKey(User)
    scene = models.ForeignKey(Scene)
    level = models.IntegerField()

class Friends(models.Model):
    user = models.ForeignKey(User)
    friends = models.ManyToManyField(User)

class Message(models.Model):
    create_time = models.DateTimeField()
    content = models.TextField()
    from_user = models.ForeignKey(User)
    to_user = models.ForeignKey(User)

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

