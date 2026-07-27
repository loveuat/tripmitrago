from pydantic import BaseModel, EmailStr, Field, field_validator


class ContactCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: EmailStr

    phone: str

    subject: str

    message: str = Field(
        ...,
        min_length=10,
        max_length=2000
    )

    consent: bool

    turnstile_token: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Name is required")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        value = value.strip()

        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")

        if value[0] not in "6789":
            raise ValueError(
                "Please enter a valid Indian mobile number"
            )

        return value

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, value):
        allowed_subjects = {
            "outstation-trip",
            "local-city-travel",
            "airport-transfer",
            "wedding-car",
            "exam-center-drop",
            "custom-trip",
            "other",
        }

        if value not in allowed_subjects:
            raise ValueError("Please select a valid subject")

        return value

    @field_validator("consent")
    @classmethod
    def validate_consent(cls, value):
        if value is not True:
            raise ValueError(
                "Please accept the terms before submitting"
            )

        return value

    @field_validator("turnstile_token")
    @classmethod
    def validate_turnstile_token(cls, value):
        if not value.strip():
            raise ValueError("Turnstile verification is required")

        return value


class ContactResponse(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True