import boto3

translate = boto3.client(
    service_name="translate", region_name="us-east-2", use_ssl=True
)


def translate_text(text, source="auto", target="es"):
    # El source es el idioma de origen, si no se especifica se detecta automaticamente
    result = translate.translate_text(
        Text=text, SourceLanguageCode=source, TargetLanguageCode=target
    )
    return result.get("TranslatedText")
