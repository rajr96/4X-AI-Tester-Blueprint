# Test Case Generation Request

Create concise, executable QA test cases for Jira issue `{{key}}`.

## Jira Summary
{{summary}}

## Description
{{description}}

## Acceptance Criteria
{{acceptance_criteria}}

## Required Scenario Coverage

Review every category below against the Jira requirements. Generate test cases for categories supported by the ticket. For categories that are not supported, add a short `Not applicable` note with the reason; do not invent product behavior.

1. User Authentication & Authorization: login, logout, password reset, session timeout, and role-based access such as admin versus regular user.
2. Form Validation & Input Fields: required fields, email/phone/date formats, character limits, and inline validation errors.
3. CRUD Lifecycle: create, read, update, delete, and deletion confirmation prompts.
4. Business Logic & Workflows: domain rules, checkout, tax, discounts/coupons, and multi-step wizards where applicable.
5. State Transitions: valid and invalid object-state changes, such as Order Placed -> Processing -> Shipped -> Delivered -> Returned/Cancelled.
6. Navigation & Deep Linking: menus, breadcrumbs, browser back/forward, redirects, and broken links.
7. Search, Filter & Sorting: exact/partial matches, multiple filters, ascending/descending sort, and zero-result messages.
8. Pagination & Infinite Scroll: page splits, items-per-page, navigation controls, and lazy loading.
9. Data Persistence & Session Management: refresh, duplicate tabs, network reconnect, and cross-device synchronization.
10. File Upload & Export/Download: allowed types, size limits, corrupted files, PDF/CSV/Excel output, and download integrity.
11. Notifications & Communication: email, SMS, push, in-app badges, and template variables.
12. Error Handling & Exceptions: timeouts, HTTP 500/404 responses, unavailable services, and lost database connections.
13. Concurrency & Race Conditions: simultaneous edits and competing actions, such as booking the last seat.
14. Time & Timezone Behavior: scheduled jobs, expiry timers, daylight-saving changes, and timezone conversion.

## Output Rules

Return only valid JSON. Do not wrap the JSON in Markdown fences or add commentary. Use exactly this structure:

{
	"scenario_coverage": [
		{
			"scenario": "User Authentication & Authorization",
			"applicable": true,
			"reason": "Why this category applies or does not apply",
			"test_cases": [
				{
					"id": "TC-001",
					"title": "Short test title",
					"priority": "High|Medium|Low",
					"type": "Functional|Negative|Boundary|Security|Usability|Recovery",
					"preconditions": "Required setup",
					"test_data": "Data used",
					"steps": ["Step 1", "Step 2"],
					"expected_result": "Expected result for the complete case",
					"overall_expected_result": "Overall outcome",
					"assumptions_coverage_gaps": "Unknowns or gaps"
				}
			]
		}
	]
}

For every applicable scenario, generate at least 2 and at most 5 test cases. The total response must contain at least 2 and at most 70 test cases. For a non-applicable scenario, set `applicable` to false, explain why in `reason`, and return an empty `test_cases` array. Include positive, negative, boundary, authorization, and recovery cases when supported. Keep expected results specific to the ticket. Do not invent requirements, credentials, limits, roles, states, integrations, or error messages.