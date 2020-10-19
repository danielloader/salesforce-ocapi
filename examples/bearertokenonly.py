from salesforce_ocapi.auth import CommerceCloudClientSession, EnvParser

with EnvParser(path="examples/.env"):
    session = CommerceCloudClientSession()

print(session.Token)
print(session.AuthHeader)
print(session.RawToken)
