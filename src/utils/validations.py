from email_validator import validate_email, EmailNotValidError


class Validations:
    @classmethod
    def validateEmail(cls, email):
        try:
            isValidEmail = validate_email(email)
            if isValidEmail:
                return True
            else:
                return False
        except EmailNotValidError as e:
            return False
