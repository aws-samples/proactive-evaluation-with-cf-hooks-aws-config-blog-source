import logging
from typing import Any, MutableMapping, Optional
from cloudformation_cli_python_lib import (
    HandlerErrorCode,
    Hook,
    HookInvocationPoint,
    OperationStatus,
    ProgressEvent,
    SessionProxy
)
from time import sleep
import json
 
from .models import HookHandlerRequest, TypeConfigurationModel
 
# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
 
TYPE_NAME = "Demo::Testing::ConfigRuleHook"
 
hook = Hook(TYPE_NAME, TypeConfigurationModel)
test_entrypoint = hook.test_entrypoint
 
# Same code will be invoked for create and update operations
@hook.handler(HookInvocationPoint.CREATE_PRE_PROVISION)
@hook.handler(HookInvocationPoint.UPDATE_PRE_PROVISION)
def pre_create_update_handler(session: Optional[SessionProxy],
        request: HookHandlerRequest,
        callback_context: MutableMapping[str, Any],
        type_configuration: TypeConfigurationModel
) -> ProgressEvent:
    target_model = request.hookContext.targetModel
    target_name = request.hookContext.targetName
    target_logical_id = request.hookContext.targetLogicalId
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS
    )
    try:
        # Reading the Resource Hook's target properties
 
        resource_properties = target_model.get("resourceProperties")
 
        LOG.info(request)
        resource_configuration = json.dumps(resource_properties)
        resource_configuration = resource_configuration.replace(": \"true\"", ": true")
        resource_configuration = resource_configuration.replace(": \"false\"", ": false")
        client = session.client("config")
        result = client.start_resource_evaluation(
            ResourceDetails={
                'ResourceId': target_logical_id,
                'ResourceType': target_name,
                'ResourceConfiguration': resource_configuration,
                'ResourceConfigurationSchemaType': 'CFN_RESOURCE_SCHEMA'
            },
            EvaluationMode='PROACTIVE',
            EvaluationTimeout=30
        )
 
        resource_eval_id = result['ResourceEvaluationId']
        LOG.info("Started evaluation, evaluation_id:" + resource_eval_id)
 
        eval_status = 'IN_PROGRESS'
        compliance = 'NON_COMPLIANT'
 
        while eval_status == 'IN_PROGRESS':
            result = client.get_resource_evaluation_summary(
                ResourceEvaluationId=resource_eval_id
            )
            eval_status = result['EvaluationStatus']['Status']
            LOG.info("Checking evaluation status: " + eval_status)
 
            if eval_status != 'IN_PROGRESS':
                compliance = result['Compliance']
                LOG.info(result)
            else:
                LOG.info("Sleeping")
                sleep(1)
 
                
        # Setting Status to success will signal to cfn that the hook operation is complete
        if compliance == 'NOT_APPLICABLE':
            progress.status = OperationStatus.SUCCESS
            progress.message = f"No Config rule is enabled in proactive mode for the given resource type {target_name}. Resource is NOT_APPLICABLE"
        elif compliance == 'COMPLIANT':
            progress.status = OperationStatus.SUCCESS
            progress.message = f"Successfully invoked HookHandler for target {target_name}. Resource is COMPLIANT"
        else: 
            progress.status = OperationStatus.FAILED
            progress.errorCode = HandlerErrorCode.NonCompliant
            progress.message = f"Resource is NON-COMPLIANT"
 
    except Exception as e:
        progress.status = OperationStatus.FAILED
        progress.message = f"Resource is NON-COMPLIANT"
        LOG.error(f"Error: {e}")
        return progress
  
    return progress
