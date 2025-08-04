from collections.abc import Generator
from typing import Any
import time

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from agentsphere import Sandbox


class RunCommandTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        sandbox_id = tool_parameters.get("sandbox_id", "")

        args = {
            "api_key": self.runtime.credentials["api_key"],
            "timeout": tool_parameters.get("timeout", 120),
            "domain": "agentsphere.run",
        }

        if sandbox_id:
            args["sandbox_id"] = sandbox_id

        sandbox = Sandbox(**args)

        time.sleep(5)

        execution = sandbox.commands.run(tool_parameters["command"])

        yield self.create_json_message({
            "stdout": execution.stdout,
            "stderr": execution.stderr,
            "exit_code": execution.exit_code,
            "error": execution.error,
            "sandbox_id": sandbox.sandbox_id,
        })
