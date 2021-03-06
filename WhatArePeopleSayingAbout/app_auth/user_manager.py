from django.contrib.auth.base_user import BaseUserManager

## Custom user manager to perform actions such as creating
class User_Manager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self, 
        username,
        email,
        password,
        is_staff, 
        is_admin, 
        **extra_fields
    ):

        ## Creates and saves a User with the given email and password.
        if not email:
            raise ValueError('Email must be set')
        if not username:
            raise ValueError('Username must be set')

        email = self.normalize_email(email)

        ## carefull, here we are giving superuser status to all admins
        ##
        user = self.model(
            username=username,
            email=email,
            is_active=True,
            is_staff=is_staff,
            is_admin=is_admin,
            is_superuser=is_admin,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(extra_fields.get('username'), email, password, False, False)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(extra_fields.get('username'), email, password, True, True)