import io
import json
import oci

 

from fdk import response
rps = oci.auth.signers.get_resource_principals_signer()
ds = oci.data_science.DataScienceClient(config={}, signer=rps)

 

def stopNotebook(notebook_session_id, data_science_client=ds):
    try:
        deactivate_notebook_session_response = data_science_client.deactivate_notebook_session(
        notebook_session_id=notebook_session_id,)
        print(deactivate_notebook_session_response.headers, flush=True)
    except Exception as ex:
        print(f'ERROR: cannot stop notebook session {notebook_session_id}', flush=True)
        raise
    return f"The notebook session {notebook_session_id} is stoped..."

 

def handler(ctx, data: io.BytesIO=None):
    alarm_msg = {}
    message_id = func_response = ""
    try:
        headers = ctx.Headers()
        message_id = headers["x-oci-ns-messageid"]
    except Exception as ex:
        print('ERROR: Missing Message ID in the header', ex, flush=True)
        raise
    print("INFO: Message ID = ", message_id, flush=True)
    # the Message Id can be stored in a database and be used to check for duplicate messages
    try:
        alarm_msg = json.loads(data.getvalue())
        print("INFO: Alarm message: ")
        print(alarm_msg, flush=True)
    except (Exception, ValueError) as ex:
        print(str(ex), flush=True)

 

    if alarm_msg["type"] == "OK_TO_FIRING":
        if alarm_msg["alarmMetaData"][0]["dimensions"]:
            alarm_metric_dimension = alarm_msg["alarmMetaData"][0]["dimensions"][0]   #assuming the first dimension matches the instance to resize
            print("INFO: Notebook to stop: ", alarm_metric_dimension["resourceId"], flush=True)
            func_response = stopNotebook(alarm_metric_dimension["resourceId"])
            print("INFO: ", func_response, flush=True)
        else:
            print('ERROR: There is no metric dimension in this alarm message', flush=True)
            func_response = "There is no metric dimension in this alarm message"
    else:
        print('INFO: Nothing to do, alarm is not FIRING', flush=True)
        func_response = "Nothing to do, alarm is not FIRING"

 

    return response.Response(
        ctx, 
        response_data=func_response,
        headers={"Content-Type": "application/json"}
    )
