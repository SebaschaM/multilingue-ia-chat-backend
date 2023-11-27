import boto3

translate = boto3.client(
    service_name="translate", region_name="us-east-2", use_ssl=True
)

result = translate.translate_text(
    Text="hi just wanted to know how you are",
    SourceLanguageCode="auto",
    TargetLanguageCode="es",
)
print("TranslatedText: " + result.get("TranslatedText"))
print("SourceLanguageCode: " + result.get("SourceLanguageCode"))
print("TargetLanguageCode: " + result.get("TargetLanguageCode"))
