import boto3
import json
from fpdf import FPDF

s3 = boto3.client('s3')

# Create a new PDF with Reportlab
def lambda_handler(event, context):
    print(event)
    json_data_body = json.loads(event["body"])

    pdf = FPDF("P", "mm", "Letter")
    pdf.add_page()
    pdf.set_font("Times", "B", 18)
    pdf.cell(40, 10, "Ticket Seller Entrada Validada")
    pdf.ln()
    pdf.set_font("Times", "", 14)
    pdf.cell(0, 8, f"Grupo: {json_data_body['group_name']}")
    pdf.ln()
    pdf.cell(0, 8, f"ID Entrada: {json_data_body['request_id']}")
    pdf.ln()
    pdf.cell(0, 8, f"Nombre del Evento: {json_data_body['event_name']}")
    pdf.ln()
    pdf.cell(0, 8, f"Fecha del evento: {json_data_body['event_date']}")
    pdf.ln()
    pdf.cell(0, 8, f"Ubicación: {json_data_body['event_location']}")
    pdf.ln()
    pdf.ln()
    pdf.cell(0, 8, f"Nombre del cliente: {json_data_body['name']}")
    pdf.ln()
    pdf.cell(0, 8, f"Correo del cliente: {json_data_body['email']}")
    pdf.ln()
    pdf.cell(0, 8, f"Cantidad de personas: {json_data_body['quantity']}")
    pdf.output(f"/tmp/entrada_{json_data_body['request_id']}.pdf", "F")

    try:
        s3.upload_file(
            Filename=f"/tmp/entrada_{json_data_body['request_id']}.pdf",
            Bucket="pdf-entradas-g1",
            Key=f"entrada_{json_data_body['request_id']}.pdf"
        )
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket":"pdf-entradas-g1",
                "Key": f"entrada_{json_data_body['request_id']}.pdf"
            },
            ExpiresIn= 7 * 24 * 3600
        )
        data = {"link": url}
        data_json_ret = json.dumps(data)
        print("Upload Successful")
        #return data_json_ret
    
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': 'https://www.iic2173g1.me',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': data_json_ret
        }

    except FileNotFoundError:
        print("The file was not found")
        return None