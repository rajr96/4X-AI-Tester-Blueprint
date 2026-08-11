package com.ricepot.framework.tests;

import java.time.Duration;
import com.ricepot.framework.pages.LoginPage;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.testng.Assert;
import org.testng.SkipException;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Test;

public class ValidLoginTest {

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
            throw new RuntimeException("Failed to initialize WebDriver for valid login test.", e);
        }
    }

    @Test
    public void verifyValidLogin() {
        String username = System.getProperty("sf.username", "").trim();
        String password = System.getProperty("sf.password", "").trim();
        if (username.isEmpty() || password.isEmpty()) {
            throw new SkipException("Provide -Dsf.username and -Dsf.password to execute valid login.");
        }

        try {
            loginPage.open();
            loginPage.typeUsername(username);
            loginPage.typePassword(password);
            loginPage.setRememberMe(true);
            loginPage.clickLogin();
            Assert.assertTrue(loginPage.isLoginSuccessful(), "Login was not successful for valid credentials.");
        } catch (Exception e) {
            Assert.fail("Valid login test failed due to exception: " + e.getMessage(), e);
        }
    }

    @AfterTest(alwaysRun = true)
    public void tearDown() {
        try {
            if (driver != null) {
                driver.quit();
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to close WebDriver in valid login test.", e);
        }
    }
}
