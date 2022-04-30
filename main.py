
from PIL import Image, ImageDraw, ImageFont
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import csv
import arabic_reshaper

# The mail addresses and password
my_email = 'sender123@gmail.com'
my_password = 'xxxxxxxx'
#   Load preferable font
font = ImageFont.truetype('Font/calibri.ttf', size=36)
# font color
default_color = (38, 255, 223)  # blue
degree_color = (255, 40, 0)  # red
black_colr = (0, 0, 0)  # black


def make_certificatet(templet, student_name, degree, email, school, manger):
    img = Image.open(templet)
    draw = ImageDraw.Draw(img)
    # write student name
    reshaped_student_name = arabic_reshaper.reshape(student_name)
    draw.text((350, 350), reshaped_student_name, fill=default_color, font=font)
    # write school name
    reshaped_school = arabic_reshaper.reshape(school)
    draw.text((400, 230), reshaped_school, fill=default_color, font=font)
    # write manger name
    reshaped_manger = arabic_reshaper.reshape(manger)
    draw.text((190, 700), reshaped_manger, fill=(255, 0, 255), font=font)
    # write degree
    draw.text((340, 490), degree, fill=degree_color, font=font)
    # save file
    img.save(f'Resulting_Image/{email}.png')
    # return path of file to send it
    return f'Resulting_Image/{email}.png'


def send_certificatet(from_email, to_email, msg, file_path):
    # TODO: write full code hear
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = message
    message.attach(MIMEText(msg, 'plain'))
    attach_file_name = file_path
    # Open the file as binary mode
    attach_file = open(attach_file_name, 'rb')
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment
    # add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(my_email, my_password)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(my_email, to_email, text)
    session.quit()
    print('Mail Sent')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    csvfile = "Studentes_data.csv"
    templeat = "Templet/Certificate.png"
    # this is a fack data
    msag = "ممبروك النجاح"
    school = "المدائن"
    manger = "محمد موسى"

    with open(csvfile) as students_data:
        reader = csv.DictReader(students_data)
        for row in reader:
            if int(row['Degree']) >= 90:
                a = make_certificatet(templeat, row["Name"], row["Degree"], row["Email"], school, manger)
                try:
                    send_certificatet(my_email, row["Email"], msag, a)
                except:
                    print("No network Avalable")
            print(row["Name"] + "is complet")
