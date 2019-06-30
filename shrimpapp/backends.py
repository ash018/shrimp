from .models import UserManager
import logging


class MyAuthBackend(object):
    def authenticate(self, email, password):
        try:
            user = UserManager.objects.get(UserId=email)
            if user.check_password(password):
                return user
            else:
                return None
        except UserManager.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists " )
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self, user_id):
        try:
            user = UserManager.objects.get(Id=user_id)
            if user.Status.Id :
                return user
            return None
        except UserManager.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(user_id)d not found")
            return None