# Salesforce Login Test Cases

## Understanding

The prompt requests an enterprise-level Selenium Java Maven TestNG framework for the Salesforce login page at `https://login.salesforce.com/?locale=in`.

The test scope includes:

- Username/email field
- Password field
- Login button
- Remember Me checkbox
- Valid credential login
- Invalid credential and validation behavior
- Page Object Model using PageFactory and `@FindBy`
- XPath-only element locators
- TestNG setup, test, and teardown annotations
- Explicit waits instead of `Thread.sleep()`
- Exception handling in both page objects and test scripts
- Two TestNG test scripts: valid login and invalid login

Real usernames and passwords must be supplied securely at execution time and must not be stored in source code.

## Preconditions

- Salesforce login URL is reachable.
- Supported browser and matching WebDriver are available.
- Test environment is available and not blocked by CAPTCHA, MFA, SSO, or network policy.
- Valid test credentials are supplied through a secure runtime mechanism.
- Invalid test data does not represent a real user's account.

## Test Case Matrix

| Test Case ID | Scenario | Test Data | Expected Result | Priority |
|---|---|---|---|---|
| SF-LOGIN-001 | Verify login page loads | Salesforce login URL | Username, password, Login, and Remember Me controls are visible and usable | High |
| SF-LOGIN-002 | Verify valid login | Valid username and valid password | User is authenticated and redirected to the expected Salesforce landing page | Critical |
| SF-LOGIN-003 | Verify invalid username and password | Invalid username and invalid password | Authentication fails and a clear login error is displayed | Critical |
| SF-LOGIN-004 | Verify valid username with invalid password | Valid username and invalid password | Authentication fails and a clear login error is displayed | High |
| SF-LOGIN-005 | Verify invalid username with valid password | Invalid username and valid password | Authentication fails and a clear login error is displayed | High |
| SF-LOGIN-006 | Verify blank username validation | Blank username and non-empty password | Login is blocked and username validation feedback is displayed | High |
| SF-LOGIN-007 | Verify blank password validation | Non-empty username and blank password | Login is blocked and password validation feedback is displayed | High |
| SF-LOGIN-008 | Verify both fields blank | Blank username and blank password | Login is blocked and required-field feedback is displayed | High |
| SF-LOGIN-009 | Verify Remember Me can be selected | Valid or invalid credentials, Remember Me selected | Checkbox changes to selected state and login request can be submitted | Medium |
| SF-LOGIN-010 | Verify Remember Me can be cleared | Remember Me selected, then cleared | Checkbox changes to unselected state and login request can be submitted | Medium |
| SF-LOGIN-011 | Verify password is masked | Any password value | Password characters are not displayed as readable text | Medium |
| SF-LOGIN-012 | Verify username field accepts email format | `test.user@example.com` | Username value is accepted by the field without UI corruption | Medium |
| SF-LOGIN-013 | Verify leading and trailing username spaces | Username with surrounding spaces | Application handles spaces according to Salesforce validation rules and does not authenticate unexpectedly | Medium |
| SF-LOGIN-014 | Verify login controls remain stable after failure | Invalid credentials submitted repeatedly | Login page remains usable, fields remain available, and no stale-element failure occurs | Medium |
| SF-LOGIN-015 | Verify browser refresh behavior after failed login | Invalid credentials, then refresh | Login page reloads correctly and no authenticated session is created | Medium |
| SF-LOGIN-016 | Verify unauthenticated access is not granted | Invalid credentials | User is not redirected to an authenticated Salesforce page | Critical |

## Detailed Test Cases

### SF-LOGIN-001: Login Page Loads

**Steps**

1. Open `https://login.salesforce.com/?locale=in`.
2. Wait for the login form to become visible.
3. Check the username field.
4. Check the password field.
5. Check the Login button.
6. Check the Remember Me checkbox.

**Expected Result**

All required controls are visible, enabled where applicable, and usable. The page URL and title correspond to the Salesforce login page.

### SF-LOGIN-002: Valid Login

**Steps**

1. Open the Salesforce login page.
2. Enter the approved valid username.
3. Enter the approved valid password.
4. Select Remember Me when the scenario requires it.
5. Click Login.
6. Wait for the authenticated landing page or authenticated UI indicator.

**Expected Result**

Authentication succeeds and the user reaches the expected authenticated Salesforce page. No login error is displayed.

### SF-LOGIN-003: Invalid Login

**Steps**

1. Open the Salesforce login page.
2. Enter an intentionally invalid username.
3. Enter an intentionally invalid password.
4. Leave Remember Me unselected.
5. Click Login.
6. Wait for the login error or validation message.

**Expected Result**

Authentication fails. A meaningful error or validation message is displayed, and the user remains unauthenticated on the login flow.

### SF-LOGIN-006: Blank Username

**Steps**

1. Open the Salesforce login page.
2. Leave the username field blank.
3. Enter a non-empty password.
4. Click Login.

**Expected Result**

The request is rejected. Username validation feedback is displayed or the form prevents submission. No authenticated page is opened.

### SF-LOGIN-007: Blank Password

**Steps**

1. Open the Salesforce login page.
2. Enter a non-empty username.
3. Leave the password field blank.
4. Click Login.

**Expected Result**

The request is rejected. Password validation feedback is displayed or the form prevents submission. No authenticated page is opened.

### SF-LOGIN-009: Remember Me Selection

**Steps**

1. Open the Salesforce login page.
2. Select Remember Me.
3. Verify the checkbox selected state.
4. Submit the login form with test credentials.

**Expected Result**

The checkbox is selected before submission. The login flow behaves normally and does not bypass authentication.

### SF-LOGIN-011: Password Masking

**Steps**

1. Open the Salesforce login page.
2. Enter any non-sensitive test password.
3. Inspect the password field type through the UI behavior.

**Expected Result**

The password is visually masked and is not readable in the field.

## Automation Acceptance Criteria

- Only XPath locators are used in page objects.
- PageFactory initializes all page elements.
- Page methods expose reusable user actions and verification methods.
- TestNG annotations manage setup, execution, and teardown.
- Explicit waits are used for dynamic UI synchronization.
- `Thread.sleep()` is not used.
- Exceptions are handled with useful failure context.
- Credentials are passed securely at runtime and are never committed.
- Tests assert both positive and negative outcomes.
- The Maven build can compile and execute the TestNG suite.
