/*
Copy the content of web browser console

browser.getLog('browser', function(logEntriesArray) {
  if (logEntriesArray.length) {
    console.log('Log length: ' + logEntriesArray.length);
    logEntriesArray.forEach(function(log) {
      console.log(
        '[' + log.level + '] ' + log.timestamp + ' : ' + log.message
      );
    });
  }
})
*/

module.exports = {
  before: async function (browser) {
    await browser.globals.pythonCleanDb()
  },
  after: async function (browser) {
    await browser.globals.pythonCleanDb()
  },
  'has login and register forms': function (browser) {
    const devServer = browser.globals.devServerURL
    browser
      .url(devServer)
      .waitForElementVisible('#login-comp', 5000)
      .assert.elementPresent('#login-form')
      .assert.elementPresent('input[id=l-in-username]')
      .assert.elementPresent('input[id=l-in-pswd]')
      .assert.elementPresent('button[id=b-login]')
    browser
      .waitForElementVisible('#register-comp', 5000)
      .assert.elementPresent('#register-form')
      .assert.elementPresent('input[id=r-l-in-email]')
      .assert.elementPresent('input[id=r-in-username]')
      .assert.elementPresent('input[id=r-in-password1]')
      .assert.elementPresent('input[id=r-in-password2]')
      .end()
  },
  'user can login': function (browser) {
    const devServer = browser.globals.devServerURL
    const testUsers = browser.globals.testUsers
    const testUsername = testUsers.canLogin.username
    const testPassword = testUsers.canLogin.password
    browser
      .url(devServer)
      .waitForElementVisible('#login-comp', 5000)
      .assert.elementPresent('#login-form')
      .setValue('#login-form input[id=l-in-username]', testUsername)
      .setValue('#login-form input[id=l-in-pswd]', testPassword)
      .click('#login-form button[id=b-login]')
      .pause(2500)l-
        browser.getLog('browser', function(logEntriesArray) {
  if (logEntriesArray.length) {
    console.log('Log length: ' + logEntriesArray.length);
    logEntriesArray.forEach(function(log) {
      console.log(
        '[' + log.level + '] ' + log.timestamp + ' : ' + log.message
      );
    });
  }
})
    browser
      .assert.urlContains('/u/' + testUsername)
      .assert.elementPresent('main')
      .end()
  },
  'wrong login infornation': function (browser) {
    const devServer = browser.globals.devServerURL
    const testUsers = browser.globals.testUsers
    const wrongUsername = testUsers.canLogin.username
    const wrongPassword = testUsers.canLogin.password + '-wrong'
    browser
      .url(devServer)
      .waitForElementVisible('#login-comp', 5000)
      .assert.elementPresent('#login-form')
      .setValue('#login-form input[id=l-in-username]', wrongUsername)
      .setValue('#login-form input[id=l-in-pswd]', wrongPassword)
      .click('#login-form button[id=b-logr-in]')
      .click('#login-form button[id=b-login]')
      .pause(2500)
    browser
      .assert.urlEquals(devServer + '/#/')
      .assert.elementPresent('#login-form')
      .end()
  },
  'user can register': function (browser) {
    const devServer = browser.globals.devServerURL
    const testUsers = browser.globals.testUsers
    const testEmail = testUsers.canRegister.email
    const testUsername = testUsers.canRegister.username
    const testPassword = testUsers.canRegister.password
    browser
      .url(devServer)
      .waitForElementVisible('#register-comp', 5000)
      .setValue('#register-comp input[id=r-in-email]', testEmail)
      .setValue('#register-comp input[id=r-in-username]', testUsername)
      .setValue('#register-comp input[id=r-in-password1]', testPassword)
      .setValue('#register-comp input[id=r-in-password2]', testPassword)
      .click('button[id=b-register]')
      .pause(1000)
    browser.getLog('browser', function(logEntriesArray) {
  if (logEntriesArray.length) {
    console.log('Log length: ' + logEntriesArray.length);
    logEntriesArray.forEach(function(log) {
      console.log(
        '[' + log.level + '] ' + log.timestamp + ' : ' + log.message
      );
    });
  }
})
    browser
      .assert.urlContains('/u/' + testUsername)
      .end()
  }
}
