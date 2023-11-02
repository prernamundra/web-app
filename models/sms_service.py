import boto3, os
from models import lognRes

client = boto3.client('sns', aws_access_key_id= 'AKIAXOW7QE3OUDGNUP5C', aws_secret_access_key='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', region_name='ap-south-1')

def send_otp(phone):
    response = client.create_sms_sandbox_phone_number(
    PhoneNumber=str(phone),
    LanguageCode='en-US'
)
    print(phone, response , " otp sent")
    return response
def verify_otp(phone, otp):
    response = client.verify_sms_sandbox_phone_number(
    PhoneNumber=str(phone),
    OneTimePassword=str(otp)
)
    print(phone, otp, response, ' verification done')
    return response

def send(phone, message):
    response = client.publish(
    PhoneNumber="+91"+str(phone),
    Message=str(message)
)   
    lognRes.successful([phone, message],"OTP SENT")
    return response

def delete_phone(phone):
    response = client.delete_sms_sandbox_phone_number(
    PhoneNumber=str(phone)
)
    return response

def get_sms_attributes():
    response = client.get_sms_attributes(
    attributes=[
        'MonthlySpendLimit',
        'DeliveryStatusIAMRole',
        'DefaultSMSType'
    ]
)
    return response

def set_sms_attributes():
    response = client.set_sms_attributes(
    attributes={
        'MonthlySpendLimit': '10'
    }
)
    return response

# print(get_sms_attributes())
# print(publish("+916376886480"))

# x = input("OTP is : ")
# print(verify_otp("+918769632421", "x"))
# print(send_otp("+918769632421"))
