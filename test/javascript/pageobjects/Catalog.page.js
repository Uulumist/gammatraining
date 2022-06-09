const Page = require('./Page');
const allure = require('wdio-allure-reporter');
const utilObj = require( '../helper/WaitActions')


class CatalogPage extends Page {

    //get CatalogLink() { return $('#hp > div.main > div.header.box > div.slogan > ul > li:nth-child(3) > a""]'); }
    get cart() { return $('#cart')};
    get firstItem() { return $('#content > table > tbody > tr:nth-child(4) > td:nth-child(1) > a > b')};
    get addToCartButton() { return $('#content > div.product-list > div > div.right > div > input')};
    get cartWithItem() { return $('#cart-total')};
    get checkoutLink() { return $('#cart > div.content > div.checkout > a:nth-child(2)')};
    get topLoginButton() { return $('#welcome > table > tbody > tr > td:nth-child(1) > a > input')};
    get userNameField() { return $('#content > div.login-content > div.right > form > div > input[type=text]:nth-child(4)')};
    get passwordField() { return $('#content > div.login-content > div.right > form > div > input[type=password]:nth-child(9)')};
    get bottomLoginButton() { return $('#content > div.login-content > div.right > form > div > input.button')}
    get userName() { return $('#welcome > a:nth-child(1)')}
    
    /**
     * Method to click first item
     */
    clickFirstItem() {
        utilObj.waitForDefaultTimeOut()
        this.firstItem.click();
    }

    clickTopLoginButton() {
        utilObj.waitForDefaultTimeOut()
        this.topLoginButton.click();
    }

    clickOpenCartTotal() {
        utilObj.waitForDefaultTimeOut();
        this.cartWithItem.click();
        utilObj.waitForDefaultTimeOut();
        browser.pause(1000);
        this.checkoutLink.click();
        browser.pause(5000);
    }

    fillUserNameField() {
        utilObj.waitForDefaultTimeOut();
        this.userNameField.click();
        this.userNameField.clearValue();
        this.userNameField.setValue('uulu1@gmail.com');
    }
    fillPasswordField() {
        utilObj.waitForDefaultTimeOut();
        this.passwordField.click();
        this.passwordField.clearValue();
        this.passwordField.setValue('123456');
    }

    clickBottomLoginButton() {
        utilObj.waitForDefaultTimeOut();
        this.bottomLoginButton.click();
    }

  /*  verifyCheckoutLinkVisible() {
     // utilObj.waitForDefaultTimeout();
        this.checkoutLink.click();
    } */
    /**
     * Method add to cart item
     */
     clickAddToCartButton() {
        utilObj.waitForDefaultTimeOut();
        this.addToCartButton.click();
    }

    clickUserName() {
        utilObj.waitForDefaultTimeOut();
        this.userName.click();
    }

    /**
     * Method to verify visible menu links
     */
    verifyVisibleMenuList(allowedMenuItemList, dataTable) {
        browser.pause(3000);
        if (allowedMenuItemList == "Organization") {
            //expect(super.organizationMenuLink.isDisplayed(), "Organization menu is not visible").to.be.true;
            super.organizationMenuLink.click();
            utilObj.waitForDefaultTimeOut();
            var List = dataTable.raw();
            //console.log(List)
            List.forEach(element => {
                element.forEach(item => {
                    if (item == "Users and devices") {
                        //browser.saveScreenshot();
                        //expect(super.userDeviceMenuLink.isDisplayed(), "Users and devices menu is not visible").to.be.true;
                        //allure.createStep("Admin has access of user and device page")
                    }
                    else if (item == "Hierarchies and groups") {
                        //browser.saveScreenshot();
                        //expect(super.hieGroupMenuLink.isDisplayed(), "Hierarchies and groups menu is not visible").to.be.true;
                        //allure.createStep("Admin has access of user and device page")
                    }
                    else if (item == "User assignment") {
                        //browser.saveScreenshot();
                        //expect(super.userAssignmentLink.isDisplayed(), "User assignment menu is not visible").to.be.true;
                        //allure.createStep("Admin has access of user and device page")
                    }
                    else if (item == "Device pool") {
                        //browser.saveScreenshot();
                        //expect(super.devicePoolLink.isDisplayed(), "Device pool menu is not visible").to.be.true;
                        //allure.createStep("Admin has access of user and device page")
                    } else {
                        //browser.saveScreenshot();
                        throw "Invalid menu item"
                    }
                });
            });
        }
        // else if (allowedMenuItemList == "Dashboard") {

        // }
    }

    /**
     * Method to verofy if current page is dashboard else navigate to dashboard
     */
    verifyCurrentPage() {
        let currentPage = browser.getTitle();
        if (currentPage.includes("Dashboard")) {
            allure.createStep('User is on Dashboard');
        }
        else {
           // super.dashboardLink.scroll();
            super.dashboardLink.click();
            //allure.addDescription("open the server instance");
        }
    }

    verifyUserLoggedIn() {
        utilObj.waitForDefaultTimeOut()
        if (this.logOutLink.isDisplayed()==1 ) 
        {
           this.logOutLink.click();
        }
        else
        {
            throw "Link does not exist"
        }
    }

    /**
     * Method to navigate to home page
     */
    navigateToHomepage() {
        utilObj.waitForDefaultTimeOut()
        if (super.homePageLink.isDisplayed()) {
            super.homePageLink.click()
            utilObj.waitForPageToLoad()
        }
        else {
            utilObj.waitForDefaultTimeOut()
            super.reportsLink.waitForExist(utilObj.defaultwait)
            super.reportsLink.click()
            utilObj.waitForDefaultTimeOut()
            super.homePageLink.waitForExist(utilObj.defaultwait)
            super.homePageLink.click()
            browser.pause(5000);
        }
    }

    /**
     * Verify admin can changes its password
     */
    verifyAdminCanChangeCredentials(){
        utilObj.waitForDefaultTimeOut();
        super.adminNameClass.click();
        super.adminDivModel.waitForExist(30000);
    }

    verifyCatalogPage() {
                
        if (this.cart.isDisplayed()) {
            allure.createStep('User is on catalog');
        }
        else {
           // super.dashboardLink.scroll();
           utilObj.waitForDefaultTimeOut(); 
           //super.dashboardLink.click();
           //allure.addDescription("open the server instance");
        }
    }

}
//module.exports = new HomePage();
module.exports = new CatalogPage();