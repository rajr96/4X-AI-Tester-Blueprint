package com.ricepot.framework.pages;

import java.time.Duration;
import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class LoginPage {

    private final WebDriver driver;
    private final WebDriverWait wait;

    @FindBy(xpath = "//input[@id='username']")
    private WebElement usernameInput;

    @FindBy(xpath = "//input[@id='password']")
    private WebElement passwordInput;

    @FindBy(xpath = "//input[@id='rememberUn']")
    private WebElement rememberMeCheckbox;

    @FindBy(xpath = "//input[@id='Login']")
    private WebElement loginButton;

    @FindBy(xpath = "//span[contains(@id,'idcard-identity')]")
    private WebElement loggedInUserBadge;

        private static final String INVALID_LOGIN_MESSAGE_XPATH =
            "//div[@id='error' or contains(@class,'loginError') or @role='alert']";

    public LoginPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(20));
        PageFactory.initElements(driver, this);
    }

    public void open() {
        try {
            driver.get("https://login.salesforce.com/?locale=in");
            wait.until(ExpectedConditions.visibilityOf(usernameInput));
            wait.until(ExpectedConditions.visibilityOf(passwordInput));
            wait.until(ExpectedConditions.elementToBeClickable(loginButton));
        } catch (Exception e) {
            throw new RuntimeException("Unable to open Salesforce login page.", e);
        }
    }

    public void typeUsername(String username) {
        try {
            WebElement element = wait.until(ExpectedConditions.visibilityOf(usernameInput));
            element.clear();
            element.sendKeys(username);
        } catch (Exception e) {
            throw new RuntimeException("Unable to type username.", e);
        }
    }

    public void typePassword(String password) {
        try {
            WebElement element = wait.until(ExpectedConditions.visibilityOf(passwordInput));
            element.clear();
            element.sendKeys(password);
        } catch (Exception e) {
            throw new RuntimeException("Unable to type password.", e);
        }
    }

    public void setRememberMe(boolean shouldBeChecked) {
        try {
            WebElement checkbox = wait.until(ExpectedConditions.elementToBeClickable(rememberMeCheckbox));
            if (checkbox.isSelected() != shouldBeChecked) {
                checkbox.click();
            }
        } catch (Exception e) {
            throw new RuntimeException("Unable to update Remember Me state.", e);
        }
    }

    public void clickLogin() {
        try {
            wait.until(ExpectedConditions.elementToBeClickable(loginButton)).click();
        } catch (Exception e) {
            throw new RuntimeException("Unable to click Login button.", e);
        }
    }

    public String getInvalidLoginMessage() {
        try {
            wait.until(ExpectedConditions.or(
                    ExpectedConditions.visibilityOfElementLocated(By.xpath("//div[@id='error']")),
                    ExpectedConditions.visibilityOfElementLocated(By.xpath("//div[contains(@class,'loginError')]")),
                    ExpectedConditions.visibilityOfElementLocated(By.xpath("//div[@role='alert']"))
            ));

            List<WebElement> messageElements = driver.findElements(By.xpath(INVALID_LOGIN_MESSAGE_XPATH));
            for (WebElement messageElement : messageElements) {
                String messageText = messageElement.getText();
                if (messageText != null && !messageText.trim().isEmpty()) {
                    return messageText.trim();
                }
            }

            throw new RuntimeException("Invalid login error container was found but had no readable text.");
        } catch (TimeoutException e) {
            throw new RuntimeException("Invalid login message not displayed in expected time.", e);
        } catch (Exception e) {
            throw new RuntimeException("Unable to fetch invalid login message.", e);
        }
    }

    public boolean isLoginSuccessful() {
        try {
            wait.until(ExpectedConditions.or(
                    ExpectedConditions.urlContains("/home/home.jsp"),
                    ExpectedConditions.visibilityOf(loggedInUserBadge)
            ));
            return driver.getCurrentUrl().contains("/home/home.jsp") || loggedInUserBadge.isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }
}
