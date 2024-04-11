import boto3
import os
from botocore.exceptions import ClientError

class StopInstances:
    """
    Esta clase maneja la detención de instancias EC2 y el envío de correos electrónicos.
    """

    def __init__(self) -> None:
        """
        Inicializa la clase con las variables de entorno y los clientes de AWS.
        """
        self.region: str = os.environ.get('REGION')
        self.instances: list[str] = [os.environ.get('INSTANCE_TO_STOP')]
        self.ec2: boto3.client = boto3.client('ec2', region_name=self.region)
        self.ses: boto3.client = boto3.client('ses', region_name=self.region)
        self.sender_email: str = os.environ.get('SENDER_EMAIL')
        self.recipient_email: str = os.environ.get('RECIPIENT_EMAIL')

    def send_email(self, subject: str, body: str) -> None:
        """
        Envía un correo electrónico utilizando Amazon SES.

        Args:
            subject (str): El asunto del correo electrónico.
            body (str): El cuerpo del correo electrónico.

        Returns:
            None
        """
        try:
            response = self.ses.send_email(
                Destination={
                    'ToAddresses': [
                        self.recipient_email,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': 'UTF-8',
                            'Data': body,
                        },
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': subject,
                    },
                },
                Source=self.sender_email
            )
        except ClientError as e:
            print("Error al enviar el correo electrónico: ", e)
        else:
            print("Correo electrónico enviado correctamente.")

    def lambda_handler(self, event: dict, context: object) -> None:
        """
        Maneja el evento de Lambda.

        Args:
            event (dict): El evento recibido por la función Lambda.
            context (object): El contexto de la función Lambda.

        Returns:
            None
        """
        if self.region is None:
            print("No se ha definido la variable de entorno 'REGION'")
            return

        if self.instances[0] is None:
            print("No se ha definido la variable de entorno 'INSTANCE_TO_STOP'")
            return

        try:
            self.ec2.stop_instances(InstanceIds=self.instances)
            print('Stopped your instances: ' + str(self.instances))
            subject: str = 'Instancias detenidas correctamente'
            body: str = 'Se han detenido las instancias correctamente: ' + str(self.instances)
        except ClientError as e:
            print("Error al detener las instancias: ", e)
            subject: str = 'Error al detener las instancias'
            body: str = 'Hubo un error al detener las instancias: ' + str(e)

        self.send_email(subject, body)
