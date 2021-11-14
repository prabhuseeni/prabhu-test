import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        u = self.create_user(username,
                        password=password,
                        date_of_birth=date_of_birth
                    )
        u.is_admin = True
        u.save(using=self._db)
        return u


class MyUser(AbstractBaseUser):
    email = models.EmailField(
                        verbose_name='email address',
                        max_length=255,
                        unique=True,
                    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'


    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Query(models.Model):
    query_uuid = models.UUIDField(default=uuid.uuid1, editable=False)
    query_message = models.TextField(blank=True, null=True)
    mentor_response = models.TextField(blank=True, null=True)
    creation_timestamp = models.DateTimeField('created', default=datetime.now, blank=True)
    modify_timestamp = models.DateTimeField('modified', default=datetime.now, blank=True)

    def __str__(self):
        return str(self.query_uuid)

    class Meta:
        db_table = 'query'