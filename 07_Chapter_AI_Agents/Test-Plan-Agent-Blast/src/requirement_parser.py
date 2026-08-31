import re
from typing import Any, Dict, List


class RequirementParser:
    def parse(self, jira_issue: Dict[str, Any]) -> Dict[str, Any]:
        fields = jira_issue.get("fields", {})
        description = self._clean_text(fields.get("description", ""))
        criteria = self._extract_acceptance_criteria(description)

        issue_key = jira_issue.get("key", "UNKNOWN")
        project = fields.get("project", {}).get("key", "UNKNOWN")
        summary = fields.get("summary", "")
        status = fields.get("status", {}).get("name", "")
        priority = fields.get("priority", {}).get("name", "")
        issue_type = fields.get("issuetype", {}).get("name", "")

        return {
            "issue_key": issue_key,
            "project": project,
            "summary": summary,
            "description": description,
            "acceptance_criteria": criteria,
            "status": status,
            "priority": priority,
            "issue_type": issue_type,
            "labels": [item.get("name", "") for item in fields.get("labels", [])],
            "assignee": fields.get("assignee", {}).get("displayName", "Unassigned"),
        }

    def parse_local_text(self, text: str, summary: str = "Local requirement") -> Dict[str, Any]:
        description = self._clean_text(text)
        criteria = self._extract_acceptance_criteria(description)

        if not criteria:
            criteria = self._extract_fallback_requirements(description)

        return {
            "issue_key": "LOCAL",
            "project": "LOCAL",
            "summary": summary,
            "description": description,
            "acceptance_criteria": criteria,
            "status": "Local",
            "priority": "Medium",
            "issue_type": "Local Requirement",
            "labels": [],
            "assignee": "Local User",
        }

    def _clean_text(self, raw: Any) -> str:
        if isinstance(raw, str):
            return raw.strip()
        if isinstance(raw, dict):
            return str(raw)
        return ""

    def _extract_acceptance_criteria(self, description: str) -> List[str]:
        if not description:
            return []

        criteria: List[str] = []
        in_functional_section = False
        current_heading = ""

        for raw_line in description.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            heading_match = re.match(r"^(?:h[1-3]\.|#{1,6})\s*(.+)$", line, re.IGNORECASE)
            if heading_match:
                current_heading = heading_match.group(1).strip()
                in_functional_section = any(
                    keyword in current_heading.lower()
                    for keyword in [
                        "functional requirements",
                        "authentication system",
                        "login process",
                        "user input validation",
                        "password management",
                        "user experience",
                        "interface design",
                        "accessibility",
                        "security",
                        "error handling",
                        "access control",
                        "password recovery",
                    ]
                )
                continue

            item_match = re.match(r"^(?:\*\s+|-\s+|\d+\.\s+)(.+)$", line)
            if item_match:
                item = self._normalize_requirement_item(item_match.group(1).strip())
                if not item:
                    continue

                if self._is_non_requirement_context(current_heading, item):
                    continue

                if in_functional_section or self._looks_like_requirement(item):
                    criteria.append(item)

        return self._deduplicate(criteria)

    def _normalize_requirement_item(self, item: str) -> str:
        item = re.sub(r"\{\{[^}]+\}\}", "", item)
        item = re.sub(r"\s+", " ", item).strip()
        return item.strip()

    def _looks_like_requirement(self, item: str) -> bool:
        keywords = [
            "authentication",
            "login",
            "validation",
            "password",
            "recovery",
            "security",
            "error",
            "responsive",
            "focus",
            "label",
            "loading",
            "sso",
            "2fa",
            "session",
            "remember",
            "access",
            "input",
            "email",
            "reset",
            "checkbox",
            "button",
            "workflow",
        ]
        lower = item.lower()
        return any(keyword in lower for keyword in keywords)

    def _is_non_requirement_context(self, heading: str, item: str) -> bool:
        lower_heading = heading.lower()
        lower_item = item.lower()

        if "target users" in lower_heading or "business objectives" in lower_heading:
            return True

        if lower_item.startswith("primary users") or lower_item.startswith("secondary users"):
            return True

        if lower_item.startswith("ensure ") or lower_item.startswith("minimize "):
            return True

        if "user base" in lower_item:
            return True

        return False

    def _extract_fallback_requirements(self, description: str) -> List[str]:
        items: List[str] = []
        for line in description.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if re.match(r"^(?:#|h[1-3]\.|\*|-|\d+\.)", stripped, re.I):
                stripped = re.sub(r"^(?:#|h[1-3]\.|\*|-|\d+\.)\s*", "", stripped, flags=re.I)
            if len(stripped) > 10 and any(keyword in stripped.lower() for keyword in ["must", "should", "validate", "allow", "reject", "show", "support"]):
                items.append(stripped)
        return self._deduplicate(items)

    def _deduplicate(self, items: List[str]) -> List[str]:
        seen = set()
        result: List[str] = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
