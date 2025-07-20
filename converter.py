import cloudconvert
import os

CLOUDCONVERT_API_KEY = os.environ.get("CLOUDCONVERT_API_KEY")

cloudconvert.configure(api_key=CLOUDCONVERT_API_KEY)

def convert_file(input_path, output_format):
    job = cloudconvert.Job.create(payload={
        "tasks": {
            "import-my-file": {
                "operation": "import/upload"
            },
            "convert-my-file": {
                "operation": "convert",
                "input": "import-my-file",
                "output_format": output_format,
            },
            "export-my-file": {
                "operation": "export/url",
                "input": "convert-my-file"
            }
        }
    })

    upload_task = job['tasks'][0]
    upload_url = upload_task['result']['form']['url']
    upload_params = upload_task['result']['form']['parameters']

    with open(input_path, 'rb') as f:
        files = {'file': (os.path.basename(input_path), f)}
        response = cloudconvert.helpers.request("post", upload_url, data=upload_params, files=files)

    job_id = job['id']
    cloudconvert.Job.wait(id=job_id)
    job = cloudconvert.Job.get(id=job_id)

    export_task = [task for task in job['tasks'] if task['name'] == 'export-my-file'][0]
    file_url = export_task['result']['files'][0]['url']
    file_name = export_task['result']['files'][0]['filename']

    # Download the file
    converted_file_path = f"converted_{file_name}"
    cloudconvert.helpers.download(file_url, converted_file_path)

    return converted_file_path
