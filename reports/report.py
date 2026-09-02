from datetime import datetime
import uuid


def create_report(
    command,
    action,
    target=None,
    status="completed",
    result=None,
    execution_time_ms=None,
    warnings=None,
    errors=None,
):
    return {
        "report_id": f"JCK-{uuid.uuid4().hex[:8].upper()}",
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "action": action,
        "target": target,
        "status": status,
        "execution_time_ms": execution_time_ms,
        "result": result or {},
        "warnings": warnings or [],
        "errors": errors or [],
    }