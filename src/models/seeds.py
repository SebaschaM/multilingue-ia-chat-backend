from src.database.db_pg import db
from src.models import *


def create_seed():
    # INSERT TAGS
    tags = [
        {"name_tag": "query"},
        {"name_tag": "complaint"},
        {"name_tag": "suggestion"},
        {"name_tag": "tracking"},
        {"name_tag": "other"},
    ]

    for tag_data in tags:
        tag = Tags.query.filter_by(name_tag=tag_data["name_tag"]).first()
        if tag is None:
            tag = Tags(**tag_data)
            db.session.add(tag)

    db.session.commit()

    # INSERT TYPE REQUEST
    type_requests = [
        {"request_type_name": "typification", "description": "Typification request"},
        {"request_type_name": "scheduling", "description": "Scheduling request"},
    ]

    for type_request_data in type_requests:
        type_request = Request_Types.query.filter_by(
            request_type_name=type_request_data["request_type_name"]
        ).first()
        if type_request is None:
            type_request = Request_Types(**type_request_data)
            db.session.add(type_request)

    db.session.commit()

    # INSERT STATUS
    status = [
        {
            "name_status": "attended",
            "description": "Attended request",
            "background_color": "#00FF00",
            "color": "#ffffff",
        },
        {
            "name_status": "pending",
            "description": "Pending request",
            "background_color": "#FFFF00",
            "color": "#ffffff",
        },
        {
            "name_status": "canceled",
            "description": "Canceled request",
            "background_color": "#FF0000",
            "color": "#ffffff",
        },
    ]

    for status_data in status:
        status = Statuses.query.filter_by(
            name_status=status_data["name_status"]
        ).first()
        if status is None:
            status = Statuses(**status_data)
            db.session.add(status)

    db.session.commit()

    # INSERT ROLES
    roles = [{"name_role": "manager"}, {"name_role": "agent"}, {"name_role": "bot"}]

    for role_data in roles:
        role = Roles.query.filter_by(name_role=role_data["name_role"]).first()
        if role is None:
            role = Roles(**role_data)
            db.session.add(role)

    db.session.commit()

    # INSERT LANGUAGES
    languages = [
        {
            "code_language": "en",
            "name_language": "English",
            "flag_img": "https://www.countryflags.io/us/flat/64.png",
        },
        {
            "code_language": "es",
            "name_language": "Spanish",
            "flag_img": "https://www.countryflags.io/es/flat/64.png",
        },
        {
            "code_language": "zh",
            "name_language": "Chinese",
            "flag_img": "https://www.countryflags.io/cn/flat/64.png",
        },
        {
            "code_language": "ru",
            "name_language": "Russian",
            "flag_img": "https://www.countryflags.io/ru/flat/64.png",
        },
        {
            "code_language": "ar",
            "name_language": "Arabic",
            "flag_img": "https://www.countryflags.io/ae/flat/64.png",
        },
        {
            "code_language": "qu",
            "name_language": "Quechua",
            "flag_img": "https://www.countryflags.io/pe/flat/64.png",
        },
        {
            "code_language": "ja",
            "name_language": "Japanese",
            "flag_img": "https://www.countryflags.io/jp/flat/64.png",
        },
        {
            "code_language": "pt",
            "name_language": "Portuguese",
            "flag_img": "https://www.countryflags.io/pt/flat/64.png",
        },
        {
            "code_language": "fr",
            "name_language": "French",
            "flag_img": "https://www.countryflags.io/fr/flat/64.png",
        },
        {
            "code_language": "ko",
            "name_language": "Korean",
            "flag_img": "https://www.countryflags.io/kr/flat/64.png",
        },
    ]

    for language_data in languages:
        language = Languages.query.filter_by(
            code_language=language_data["code_language"]
        ).first()
        if language is None:
            language = Languages(**language_data)
            db.session.add(language)

    db.session.commit()
