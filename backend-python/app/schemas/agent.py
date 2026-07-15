"""Agent API schemas."""

from typing import Any

from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """AI model configuration."""

    api_key: str | None = Field(None, alias="apiKey")
    base_url: str | None = Field(None, alias="baseUrl")
    model: str | None = None

    class Config:
        populate_by_name = True


class SandboxConfig(BaseModel):
    """Sandbox configuration."""

    enabled: bool = False
    provider: str | None = None  # codex, native, docker


class SkillsConfig(BaseModel):
    """Skills configuration."""

    enabled: bool = False
    user_dir_enabled: bool = Field(False, alias="userDirEnabled")
    app_dir_enabled: bool = Field(False, alias="appDirEnabled")
    skills_path: str | None = Field(None, alias="skillsPath")

    class Config:
        populate_by_name = True


class MCPConfig(BaseModel):
    """MCP configuration."""

    enabled: bool = False
    user_dir_enabled: bool = Field(False, alias="userDirEnabled")
    app_dir_enabled: bool = Field(False, alias="appDirEnabled")
    mcp_config_path: str | None = Field(None, alias="mcpConfigPath")

    class Config:
        populate_by_name = True


class ImageAttachment(BaseModel):
    """Image attachment for agent requests."""

    data: str
    mime_type: str = Field(..., alias="mimeType")

    class Config:
        populate_by_name = True


class ConversationMessage(BaseModel):
    """A message in the conversation history."""

    role: str
    content: str | list[Any]


class AgentPlanRequest(BaseModel):
    """Request for creating a plan."""

    prompt: str
    model_config_data: ModelConfig | None = Field(None, alias="modelConfig")

    class Config:
        populate_by_name = True


class AgentExecuteRequest(BaseModel):
    """Request for executing an approved plan."""

    plan_id: str = Field(..., alias="planId")
    prompt: str = ""
    work_dir: str | None = Field(None, alias="workDir")
    task_id: str | None = Field(None, alias="taskId")
    model_config_data: ModelConfig | None = Field(None, alias="modelConfig")
    sandbox_config: SandboxConfig | None = Field(None, alias="sandboxConfig")
    skills_config: SkillsConfig | None = Field(None, alias="skillsConfig")
    mcp_config: MCPConfig | None = Field(None, alias="mcpConfig")

    class Config:
        populate_by_name = True


class AgentRequest(BaseModel):
    """Request for direct agent execution."""

    prompt: str
    conversation: list[ConversationMessage] | None = None
    work_dir: str | None = Field(None, alias="workDir")
    task_id: str | None = Field(None, alias="taskId")
    model_config_data: ModelConfig | None = Field(None, alias="modelConfig")
    sandbox_config: SandboxConfig | None = Field(None, alias="sandboxConfig")
    images: list[ImageAttachment] | None = None
    skills_config: SkillsConfig | None = Field(None, alias="skillsConfig")
    mcp_config: MCPConfig | None = Field(None, alias="mcpConfig")

    class Config:
        populate_by_name = True

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for JSON serialization."""
        data = {"prompt": self.prompt}
        if self.conversation:
            data["conversation"] = [m.model_dump() for m in self.conversation]
        if self.work_dir:
            data["workDir"] = self.work_dir
        if self.task_id:
            data["taskId"] = self.task_id
        if self.model_config_data:
            data["modelConfig"] = self.model_config_data.model_dump(exclude_none=True, by_alias=True)
        if self.sandbox_config:
            data["sandboxConfig"] = self.sandbox_config.model_dump(exclude_none=True, by_alias=True)
        if self.images:
            data["images"] = [img.model_dump(by_alias=True) for img in self.images]
        if self.skills_config:
            data["skillsConfig"] = self.skills_config.model_dump(exclude_none=True, by_alias=True)
        if self.mcp_config:
            data["mcpConfig"] = self.mcp_config.model_dump(exclude_none=True, by_alias=True)
        return data
