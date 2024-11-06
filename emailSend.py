from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import pathlib
BASE_DIR = pathlib.Path(__file__).parent.resolve()
# Configurações do envio de email
YOUR_GOOGLE_EMAIL = 'mateussmoura30@gmail.com'
passwordFilePath = BASE_DIR /'emailPassword.txt'
password = []
with open(passwordFilePath, "r") as file:
    password = [line.strip() for line in file.readlines()]
YOUR_GOOGLE_EMAIL_APP_PASSWORD = password[0]

smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
smtpserver.ehlo()
smtpserver.login(YOUR_GOOGLE_EMAIL, YOUR_GOOGLE_EMAIL_APP_PASSWORD)

# Montagem do texto
subject = "Teste envio de email"
text = "hello world"
msg = MIMEMultipart()
msg['Subject'] = subject
msg.attach(MIMEText(text))

# Caminho absoluto para input.txt baseado na localização do script
# BASE_DIR = pathlib.Path(__file__).parent.resolve()
input_file_path = BASE_DIR / "input.txt"

# Leitura dos destinatários do arquivo input.txt
to = []
with open(input_file_path, "r") as file:
    to = [line.strip() for line in file.readlines()]

# Enviar o email
smtpserver.sendmail(
    from_addr=YOUR_GOOGLE_EMAIL,
    to_addrs=to,
    msg=msg.as_string()
)

# Encerrar a conexão com o servidor SMTP
smtpserver.quit()





# usmp zsve hapr pgsk
