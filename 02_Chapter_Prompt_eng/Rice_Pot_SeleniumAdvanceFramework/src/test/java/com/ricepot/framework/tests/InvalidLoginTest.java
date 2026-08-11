package com.ricepot.framework.tests;

import java.time.Duration;
import com.ricepot.framework.pages.LoginPage;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.testng.Assert;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

public class InvalidLoginTest {

    private WebDriver driver;
    private LoginPage loginPage;

    @BeforeTest
    public void setUp() {
        try {
            ChromeOptions options = new ChromeOptions();
            options.addArguments("--start-maximized");
            driver = new ChromeDriver(options);
            driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(5));
            loginPage = new LoginPage(driver);
        } catch (Exception e) {
            throw new RuntimeException("Failed to initialize WebDriver for invalid login test.", e);
        }
    }

    @DataProvider(name = "invalidCredentials")
    public Object[][] invalidCredentials() {
        return new Object[][]{
                {"invalid.user@example.com", "WrongPassword123"},
                {"", "WrongPassword123"},
                {"invalid.user@example.com", ""}
        };
    }

    @Test(dataProvider = "invalidCredentials")
    public void verifyInvalidLogin(String username, String password) {
        try {
            loginPage.open();
            loginPage.typeUsername(username);
            loginPage.typePassword(password);
            loginPage.setRememberMe(false);
            loginPage.clickLogin();

            String errorText = loginPage.getInvalidLoginMessage();
            Assert.assertTrue(
                    errorText.toLowerCase().contains("please check")
                            || errorText.toLowerCase().contains("enter your password")
                            || errorText.toLowerCase().contains("enter your username"),
                    "Unexpected error message for invalid login. Actual: " + errorText
            );
            Assert.assertFalse(loginPage.isLoginSuccessful(), "Login succeeded unexpectedly with invalid credentials.");
        } catch (Exception e) {
            Assert.fail("Invalid login test failed due to exception: " + e.getMessage(), e);
        }
    }

    @AfterTest(alwaysRun = true)
    public void tearDown() {
        try {
            if (driver != null) {
                driver.quit();
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to close WebDriver in invalid login test.", e);
        }
    }
}
