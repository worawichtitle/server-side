from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=10)
    main_contact = models.CharField(max_length=200)
    address = models.TextField()
    def __str__(self):
        return self.username


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name


class Staff(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=10)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.username


class Province(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


# class CondoStatus(models.Model):
#     name = models.CharField(max_length=50)


class Condo(models.Model):
    deed_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    address = models.TextField()
    area_sqm = models.FloatField()
    deed_picture = models.FileField(upload_to="image/")
    description = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    class CondoStatus(models.TextChoices):
        NULL = "NUL", "NULL"
        CHECK = "CHK", "CHECK"
        FAIL = "FAL", "FAIL"
        PASS = "PAS", "PASS"
        BUY = "BUY", "BUY"
    status = models.CharField(max_length=3, choices=CondoStatus.choices, default=CondoStatus.NULL)
    # status = models.ForeignKey(CondoStatus, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name

def condo_image_upload_path(instance, filename):
    return f'image/{instance.condo.id}/{filename}'

class CondoImage(models.Model):
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE, related_name='images')
    image_url = models.FileField(upload_to=condo_image_upload_path)
    image_name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.image_name


class CondoReport(models.Model):
    # author = models.ForeignKey(Staff, on_delete=models.CASCADE)
    author = models.ManyToManyField(Staff) # M to M
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)
    report = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Report by {self.author.username} on {self.condo.name}"


class CondoListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)
    asking_price = models.DecimalField(max_digits=12, decimal_places=2)
    listed_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Listing of {self.condo.name} by {self.user.username}"
