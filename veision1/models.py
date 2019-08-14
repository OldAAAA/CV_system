from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

# Create your models here.
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, username
         and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    # email
    email = models.EmailField(unique=True)

    objects = MyUserManager()

    # creation date
    created_at = models.DateTimeField('Creation Time', auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []
    is_admin = models.BooleanField(default=False)

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class ManageInfo(models.Model):
    realname = models.CharField(max_length=30, null=False, default='null')
    phone_number = models.CharField(max_length=30, null=False, default='null')
    sex = models.CharField(max_length=4, null=False, default='null')
    age = models.CharField(max_length=3, null=False, default='null')
    address = models.CharField(max_length=30, null=False, default='null')
    email = models.CharField(max_length=30, null=False, default='null')
    photo = models.ImageField(upload_to='user_photo/',default='null')
    user_email = models.CharField(max_length=30, null=False, default='null')


class elderlyInfo(models.Model):
    photo = models.ImageField(upload_to='user_photo/', default='null')
    name = models.CharField(max_length=30, null=False, default='null')
    sex = models.CharField(max_length=4, null=False, default='null')
    phone_number = models.CharField(max_length=30, null=False, default='null')
    id_card = models.CharField(max_length=30, null=False, default='null')
    age = models.CharField(max_length=3, null=False, default='null')
    admission_date = models.DateField(blank=True)

class staffInfo(models.Model):
    photo = models.ImageField(upload_to='user_photo/', default='null')
    name = models.CharField(max_length=30, null=False, default='null')
    sex = models.CharField(max_length=4, null=False, default='null')
    phone_number = models.CharField(max_length=30, null=False, default='null')
    id_card = models.CharField(max_length=30, null=False, default='null')
    age = models.CharField(max_length=3, null=False, default='null')
    admission_date = models.DateField(auto_now_add=True, blank=True)

class volunteerInfo(models.Model):
    photo = models.ImageField(upload_to='user_photo/', default='null')
    name = models.CharField(max_length=30, null=False, default='null')
    sex = models.CharField(max_length=4, null=False, default='null')
    phone_number = models.CharField(max_length=30, null=False, default='null')
    id_card = models.CharField(max_length=30, null=False, default='null')
    age = models.CharField(max_length=3, null=False, default='null')
    visit_date = models.DateField(auto_now_add=True, blank=True)
    depart_date = models.DateField(blank=True)

