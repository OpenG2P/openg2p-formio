from odoo import http
from odoo.http import request
import logging
import boto3
import warnings
import json



warnings.filterwarnings("ignore", category=DeprecationWarning)
_logger = logging.getLogger(__name__)

# This controller only use for storing file on minio  
class DiffFileUpload(http.Controller):
    @http.route('/v1/selfservice/uploadDocument', type='http', auth='public', method=['POST'], csrf=False)
    def add_file(self, **kwargs):
        _logger.info("-------------file received-----------")

        if 'file' not in request.httprequest.files:
            return request.make_response("-------no file selected-------", status=400)
        
        file = request.httprequest.files['file']

        if file.filename == '':
            return request.make_response("--------no file selected--------", status=400)

        # Fetch minio config from db
        backend = request.env['storage.backend'].search([('name', '=', 'Default S3 Document Store')], limit=1)
        
        if not backend:
            return request.make_response("Error: MinIO backend configuration not found", status=500)
        
        aws_host = backend.aws_host
        aws_access_key_id = backend.aws_access_key_id
        aws_secret_access_key = backend.aws_secret_access_key
        aws_bucket = backend.aws_bucket
       
        s3_client = boto3.client(
            's3',
            endpoint_url= aws_host,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='other',  
        )

        try:
            s3_client.upload_fileobj(
                Fileobj=file.stream,
                Bucket=aws_bucket,
                Key=file.filename
            )
            response_status = 200
            return request.make_response("------------Successfully file uploaded-----------", status=200)
        except Exception as e:
            response_status = 500
            return request.make_response(f"Error: {e}", status=500)
        finally:
            _logger.info(f"-----------File upload request completed with status: {response_status}------------")

    